import os
import requests
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
    if 'video_url' in dict(request.form).keys() and len(dict(request.form).keys()) == 1:
        url = request.form['video_url']
        print(url)

        try:
            video = YouTube(url)
            
            files_to_be_del = os.listdir("static/songs")
            print(files_to_be_del)
            for file_to_be_del in files_to_be_del:
                    os.remove("static//songs//" + file_to_be_del)
            
            file_name = video.streams.get_highest_resolution().download(output_path="static/songs")
            max_file = "static/songs/" + str(file_name).split("/")[-1]
            code = open('templates/downloaded.html').read().replace("{{ src }}", max_file)
            return code

        except Exception as e:
            print(e)
            return open("templates/index.html").read() + "<script>\nalert('Video Not Available')\n</script>"

    elif 'video_url' in request.form  and 'audio' in dict(request.form).keys():
        url = request.form['video_url']
        try:
            yt = YouTube(url)
            video = yt.streams.filter(only_audio=True).first()
            files_to_be_del = os.listdir("static/music")
            for file_to_be_del in files_to_be_del:
                    os.remove(os.path.join("static/music", file_to_be_del))
            out_file = video.download(output_path="static/music")
            out_file = str(out_file).split("/")[-1]
            new_file = os.path.join("static/music", out_file)
            code = open('templates/downloaded.html').read().replace("{{ src }}", new_file)
            return code

        except Exception as e:
            print(e)
            return open("templates/index.html").read() + "<script>\nalert('Video Not Available')\n</script>"
       


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


app.run(host="0.0.0.0", port=8080, debug=True)



