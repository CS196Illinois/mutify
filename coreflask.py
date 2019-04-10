from flask import Flask, request, render_template, make_response, send_file, redirect, url_for, session
from pydub import AudioSegment
from audioFunctions import convertTimestamps, trackSplit, trackCrop, trackSpeedUp
import zipfile, os, tempfile

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def main():
    if session.get('directoryname') == False:
        #I don't think I should be saving large files in the individual user sessions...
        #pretty sure better way to do this is with temporary directories, or some db system
        session['tracks'] = {}
        #this needs to be unique per user...
        session['directoryname'] = 'directory1'
    return render_template('home.html', tracks = session['tracks'])

@app.route('/split', methods=['POST'])
def split():
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
    session['tracks'].update(trackSplit(mSong, lTimestamps, lTracknames, sArtist, sAlbum))
    return redirect(url_for('main'))

@app.route('/crop', methods=['POST'])
def crop():
    #processing input
    request_file = request.files['songfile']
    mSong = AudioSegment.from_mp3(request_file)
    sStartTime = request.form['start']
    sEndTime = request.form['end']
    sTitle = request.form['title']
    sArtist = request.form['artist']
    sAlbum = request.form['album']
    #converting time input to ints
    iStart = convertTimestamps(sStartTime)[0]
    iEnd = convertTimestamps(sEndTime)[0]
    session['tracks'].update(trackCrop(mSong, iStart, iEnd, sTitle, sArtist, sAlbum))
    return redirect(url_for('main'))

@app.route('/speedup', methods=['POST'])
def speedup():
    #processing input
    request_file = request.files['songfile']
    mSong = AudioSegment.from_mp3(request_file)
    iFactor = request.form['factor']
    sTitle = request.form['title']
    sArtist = request.form['artist']
    sAlbum = request.form['album']
    session['tracks'].update(trackSpeedUp(mSong, iFactor, sTitle, sArtist, sAlbum))
    return redirect(url_for('main'))

@app.route('/out/<trackname>', methods=['GET'])
def track(trackname):
    result = session['tracks'][trackname]
    return send_file(result, attachment_filename=trackname+".mp3")

@app.route('/outzip')
def outzip():
    zipout = zipfile.ZipFile("album.zip", 'w', zipfile.ZIP_DEFLATED)
    for key in session['tracks']: zipout.write(key + ".mp3")
    zipout.close()
    #need to delete the zip file.
    return send_file('album.zip', mimetype='zip', attachment_filename = "album.zip", as_attachment = True)

if __name__ == '__main__':
    app.run()
