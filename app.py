import os
import subprocess
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        
        try:
            # yt-dlp options to download both audio and video and merge them
            ydl_opts = {
                'format': 'bestvideo+bestaudio/best',  # Best video and best audio
                'merge_output_format': 'mp4',          # Merge the audio and video into an mp4 file
                'outtmpl': '%(title)s.%(ext)s',        # Output file name format
                'noplaylist': True,                    # Avoid downloading playlist if given a playlist URL
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',  # Custom user-agent
            }
            
            # Build the command with the yt-dlp options
            command = ['yt-dlp']
            for key, value in ydl_opts.items():
                command.append(f'--{key}')
                command.append(str(value))

            # Add the URL to the command
            command.append(url)
            
            # Run the yt-dlp command and capture its output
            result = subprocess.run(command, capture_output=True, text=True)
            
            # Debug logs for stdout and stderr
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            
            if result.returncode == 0:
                # Check if the video file is downloaded
                filename = next((f for f in os.listdir('.') if f.endswith('.mp4') or f.endswith('.mkv')), None)
                if filename:
                    return render_template('index.html', success=True, filename=filename)
                else:
                    return render_template('index.html', error="Video not found after download.")
            else:
                return render_template('index.html', error=f"Download failed: {result.stderr.strip()}")
        
        except Exception as e:
            # Handle any unexpected errors
            print(f"Error occurred: {str(e)}")
            return render_template('index.html', error="An error occurred while processing your request.")
    
    # For GET request, just render the initial page with the form
    return render_template('index.html')


if __name__ == '__main__':
    # Ensure the app binds to the correct port as required by Render
    port = os.getenv('PORT', 5000)  # Render assigns the port dynamically
    app.run(debug=True, host='0.0.0.0', port=port)
