from flask import Flask, request, render_template, make_response, send_file, redirect, url_for
from pydub import AudioSegment
from audioFunctions import convertTimestamps, trackSplit
import zipfile
app = Flask(__name__)

tracks = {}

#TODO: add default location to save files, and automatically delete old ones
@app.route('/', methods=['GET','POST'])
def main():
    if request.method == 'POST':
        #processing input
        request_file = request.files['albumfile']
        mSong = AudioSegment.from_mp3(request_file)
        sTimestamps = request.form['timestamps']
        sTracknames = request.form['tracknames']
        sArtist = request.form['artist']
        sAlbum = request.form['album']
        #converting raw input to lists
        lTracknames = sTracknames.splitlines()
        lTimestamps = convertTimestamps(sTimestamps)
        #have to do this for scope issues, there's probably a better way though
        global tracks
        tracks = trackSplit(mSong, lTimestamps, lTracknames, sArtist, sAlbum)
        return redirect(url_for('out'))
    else:
        return render_template('upload.html')

@app.route('/out')
def out():
    return render_template('out.html', tracks = tracks)

@app.route('/out/<trackname>', methods=['GET'])
def track(trackname):
    result = tracks[trackname]
    return send_file(result, attachment_filename=trackname+".mp3")

@app.route('/outzip')
def outzip():
    zipout = zipfile.ZipFile("album.zip", 'w', zipfile.ZIP_DEFLATED)
    for key in tracks: zipout.write(key + ".mp3")
    zipout.close()
    return send_file('album.zip', mimetype='zip', attachment_filename = "album.zip", as_attachment = True)

if __name__ == '__main__':
    app.run()
