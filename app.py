from flask import Flask, render_template, request, send_from_directory, redirect, url_for
import os
import yt_dlp

app = Flask(__name__)
DOWNLOADS_DIR = "downloads"

if not os.path.exists(DOWNLOADS_DIR):
    os.makedirs(DOWNLOADS_DIR)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        try:
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best',
                'merge_output_format': 'mp4',
                'outtmpl': os.path.join(DOWNLOADS_DIR, '%(title)s.%(ext)s'),
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info).replace(".webm", ".mp4")
                filename = os.path.basename(filename)
            return redirect(url_for('download_file', filename=filename))
        except Exception as e:
            return f"<h3>Error: {str(e)}</h3>"
    return render_template('index.html')

@app.route('/downloads/<filename>')
def download_file(filename):
    return send_from_directory(DOWNLOADS_DIR, filename, as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Render sets PORT env variable
app.run(host='0.0.0.0', port=port)
