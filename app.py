from flask import Flask, Response
import socket
from glob import glob
import os

song_list = sorted(glob(os.path.join('songs', '*.mp3')))

app = Flask(__name__)

def generate():
    for song_path in song_list:
        with open(song_path, 'rb') as f:
            data = f.read(1024)
            while data:
                yield data
                data = f.read(1024)

@app.route('/')
def stream():
    return Response(generate(), mimetype='audio/mp3')

if __name__ == '__main__':
    PORT = 5000

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(('8.8.8.8', 80))
        print('[*] Open http://%s:%s on your browser to enjoy music!' % (s.getsockname()[0], PORT))

    app.run(host='0.0.0.0', port=PORT)
