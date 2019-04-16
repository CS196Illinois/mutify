#methods in order to split a long audio track into several different audio tracks.
from pydub import AudioSegment
from pydub.effects import speedup

#converts timestamps, in the form HH:MM:SS, into a list of seconds (first being 0)
def convertTimestamps(sTimestamps):
    lTimestamps = sTimestamps.splitlines()
    lConvertedstamps = []
    for timestamp in lTimestamps:
        #its reversed because otherwise it doesn't support MM:SS type timestamps
        lConvertedstamps.append(sum(factor * int(t) for factor, t in zip([1, 60, 3600], reversed(timestamp.split(":")))))
    return lConvertedstamps


#splits an audio track passed to it, takes track names, timestamp list, song file, and tags
#must pass AudioSegment mp3 file type!
#exports dictionary with keys as song names
def trackSplit(mSong, lTimestamps, lTrackNames, sArtist, sAlbum):
    dTracks = {}
    trackCount = 1
    for index, (time, name) in enumerate(zip(lTimestamps, lTrackNames)):
        #multiplied by 1000 to convert to milliseconds
        #have to treat final song differently, as there is no timestamp for it's end.
        if (index + 1 == len(lTimestamps)):
            tempSong = mSong[time*1000:]
        else:
            tempSong = mSong[lTimestamps[index]*1000:lTimestamps[index+1]*1000]
        dTracks[name] = tempSong.export(name + ".mp3", format="mp3", tags={"track": index, "artist": sArtist, "album" : sAlbum})
    return dTracks


#Crops an audio track passed to it, does the same stuff as splitter otherwise
#pass AUdioSegment mp3 file type, and integer times in seconds.
#exports dictionary with key as song name.
def trackCrop(mSong, iStartTime, iEndTime, sTitle, sArtist, sAlbum):
    #multipled by 1000 for second to millisecond conversion
    tempSong = mSong[iStartTime*1000:iEndTime*1000]
    return { sTitle : tempSong.export(sTitle + ".mp3", format="mp3", tags={"artist" : sArtist, "album" : sAlbum}) }


#speeds up an audio track
def trackSpeedUp(mSong, iFactor, sTitle, sArtist, sAlbum):
    tempSong = speedup(mSong, float(iFactor))
    return { sTitle : tempSong.export(sTitle + ".mp3", format="mp3", tags={"artist" : sArtist, "album" : sAlbum}) }


#gets a catchy hook composed from the first seven seconds of a song and the last five seconds of a song, mixed together
#pass AudioSegment (mp3 file type), and its title, artist, and album
#exports dictionary with key as song name
def getCatchyHook(mSong, sTitle, sArtist, sAlbum):
	first_7 = tempSong[:7000]
	last_5 = tempSong[-5000:]
	beginning = first_7 + 6;
	end = last_5 - 3;
	cropped = beginning + end
	faded = beginning.append(end, crossfade=1500)
	faded_x2 = faded * 2
	catchy_hook = faded_x2.fade_in(2000).fade_out(3000)
	return { sTitle : catchy_hook.export(sTitle + ".mp3", format="mp3", tags={"artist" : sArtist, "album" : sAlbum})  }


#gets an audio clip of silence for a specified duration
#pass an integer value of milliseconds of silence to get
#exports dicitonary with key as iDuration_second_silence
def getSilence(iDuration):
	silence = AudioSegment.silent(duration=iDuration)
	return { "" + iDuration + "_second_silence" : silence.export("" + iDuration + "_second_silence.mp3", format="mp3") }


#combines a list of AudioSegments (file type mp3) into one audio file called mixtape.mp3
#pass a list of AudioSegments (file type mp3)
#exports dictionary with key as "mixtape"
def combineClips(*argv):
	clips = []
	for arg in argv:
		clips.append(arg)
	combined = AudioSegment.empty()
	for clip in clips:
		combined += AudioSegment.from_mp3(clip)
	return { "mixtape" : combined.export("mixtape.mp3", format="mp3") }
