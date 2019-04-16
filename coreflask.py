from flask import Flask, request, render_template, make_response, send_file, redirect, url_for, session
from pydub import AudioSegment
from audioFunctions import convertTimestamps, trackSplit, trackCrop, trackSpeedUp
import zipfile, os, tempfile

app = Flask(__name__)
app.config['SECRET_KEY'] = 'some random arbitrary key value'

totalusers = 0

@app.route('/', methods=['GET','POST'])
def main():
    if 'dirname' not in session:
        global totalusers
        session['dirname'] = totalusers
        totalusers = totalusers + 1
        if not os.path.exists(session['dirname']):
            os.makedir(session['dirname'])
    tracks = {}
    for filename in os.listdir(session['dirname']):
        tracks[filename] = open(session['dirname']+filename)
    return render_template('home.html', tracks = tracks)

@app.route('/split', methods=['POST'])
def split():
    #processing input
    request_file = request.files['albumfile']
    mSong = AudioSegment.from_mp3(request_file)
    sTimestamps = request.form['timestamps']
    sTracknames = request.form['tracknames']
    sartist = request.form['artist']
    sAlbum = request.form['album']
    #converting raw input to lists
    lTracknames = sTracknames.splitlines()
    lTimestamps = convertTimestamps(sTimestamps)
    for key, value in trackSplit(mSong, lTimestamps, lTracknames, sArtist, sAlbum).items():
        tempfile = open(session['dirname'] + "/" + key)
        tempfile.write(value)
        os.remove(value)
    #unsure if this works, if not will need to improve.
    os.remove(request_file)
    return redirect(url_for('main'))

#havent implemented changes in these two methods yet:
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
    session['count'].append("test")
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
