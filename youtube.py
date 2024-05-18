# app.py
from flask import Flask, request, jsonify
from local_lib.pytube.__main__ import YouTube as huggywuggywilleatyoucuzyouverytasty

class Developer:
    def __init__(self):
        self.name: str = "Nikita"
        self.nickname: str = "3verlaster"
        self.github_link: str = "https://github.com/3verlaster"

def download_video_max_res(video_url):
    try:
        yt = huggywuggywilleatyoucuzyouverytasty(video_url)
        stream = yt.streams.get_highest_resolution()
        if stream:
            video_title = stream.title
            print(f"Downloading ... [{video_url}] - [{video_title.strip()}]")
            stream.download()
            return f"Video downloaded successfully."
        else:
            return "Unable to find a suitable video stream."
    except Exception as e:
        return "An error occurred: {}".format(str(e))

app = Flask(__name__)

@app.route('/')
def index():
    developer = Developer()
    return jsonify({
        "developer": developer.name,
        "nickname": developer.nickname,
        "github_link": developer.github_link
    })

@app.route('/download', methods=['POST'])
def download():
    data = request.json
    video_url = data.get('video_url')
    if not video_url:
        return jsonify({"error": "No video URL provided"}), 400
    
    if not video_url.startswith("https://youtube.com/shorts/"):
        return jsonify({"error": "This is not a YouTube shorts link!"}), 400

    response = download_video_max_res(video_url)
    return jsonify({"message": response})

if __name__ == "__main__":
    app.run(debug=True)
