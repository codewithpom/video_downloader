import os.path
import glob
from flask import Flask, render_template
from flask import request
from pytube import YouTube
from flask_cors import CORS
app = Flask('app')

CORS(app)


@app.route("/")
def hello_world():
    print("One more visitor")
    return render_template("index.html")


@app.route("/download", methods=['POST'])
def download_video():
    print(request.form)
    if 'video_url' in dict(request.form).keys():
        url = request.form['video_url']
        print(url)

        try:
            video = YouTube(url)
            video.streams.get_highest_resolution().download(output_path="static/songs")

            folder_path = r'static/songs'
            file_type = '\*mp4'
            files = glob.glob(folder_path + file_type)
            max_file = max(files, key=os.path.getctime)
            print(max_file)
            code = open('templates/downloaded.html').read().replace("{{ src }}", max_file)
            return code

        except Exception as e:
            return open("templates/index.html").read() + "<script>\nalert('Video Not Available')\n</script>"

    elif 'video_url' in request.form and 'audio' in dict(request.form).keys():
        return "Hello World"


@app.route("/details", methods=['POST'])
def provide():
    print("One more person wants to know about a video")
    if 'url' in request.form:
        url = request.form['url']

        # noinspection PyBroadException
        try:
            video = YouTube(url)
            data = {'title': video.title, 'thumbnail': video.thumbnail_url}
            return data

        except Exception as e:
            return "Video Not Available", 200


app.run(host="localhost", port=80, debug=True)



