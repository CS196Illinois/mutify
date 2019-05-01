from flask import Flask, request, render_template, make_response, send_file, redirect, url_for, session
from pydub import AudioSegment
from audioFunctions import convertTimestamps, trackSplit, trackCrop, trackSpeedUp
import zipfile, uuid
app = Flask(__name__)
app.config['SECRET_KEY'] = 'some random arbitrary key value'
app.config['UPLOAD_FOLDER'] = 'userfiles'

users = {}

#TODO: add default location to save files, and automatically delete old ones
@app.route('/', methods=['GET','POST'])
def main():
    if 'uid' not in session:
        global users
        session['uid'] = str(uuid.uuid4)
        users[session['uid']] = {}
    return render_template('home.html', tracks =  users[session['uid']])

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
    global users
    users[session['uid']].update(trackSplit(mSong, lTimestamps, lTracknames, sArtist, sAlbum))
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
    global users
    users[session['uid']].update(trackCrop(mSong, iStart, iEnd, sTitle, sArtist, sAlbum))
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
    global users
    users[session['uid']].update(trackSpeedUp(mSong, iFactor, sTitle, sArtist, sAlbum))
    return redirect(url_for('main'))

@app.route('/catchyhook', methods=['POST'])
def catchyhook():
    #processing input
    request_file = request.files['songfile']
    mSong = AudioSegment.from_mp3(request_file)
    sTitle = request.form['title']
    sArtist = request.form['artist']
    sAlbum = request.form['album']
    #have to do this for scope issues
    global tracks
    tracks.update(getCatchyHook(mSong, sTitle, sArtist, sAlbum))
    return redirect(url_for('main'))

@app.route('/silence', methods=['POST'])
def silence():
    #processing input
    iDuration = request.form['duration']
    #have to do this for scope issues
    global tracks
    tracks.update(getSilence(iDuration * 1000))
    return redirect(url_for('main'))

@app.route('/combineclips', methods=['POST'])
def combineclips():
    #processing input
    mSongList = []
    numInputSongs = request.form['num']
    for i in range(numInputSongs):
        request_file = request.files['songfile']
        mSong = AudioSegment.from_mp3(request_file)
        mSongList.append(mSong)
    #need to test if this method works to receive multiple inputs
    #have to do this for scope issues
    tracks.update(combineClips(mSongList))
    return redirect(url_for('main'))

@app.route('/out/<trackname>', methods=['GET'])
def track(trackname):
    result = tracks[trackname]
    return send_file(result, attachment_filename=trackname+".mp3")

@app.route('/outzip')
def outzip():
    zipout = zipfile.ZipFile("album.zip", 'w', zipfile.ZIP_DEFLATED)
    for key in users[session['uid']]: zipout.write(key + ".mp3")
    zipout.close()
    return send_file('album.zip', mimetype='zip', attachment_filename = "album.zip", as_attachment = True)

if __name__ == '__main__':
    app.run()
