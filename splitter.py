#methods in order to split a long audio track into several different audio tracks.
from pydub import AudioSegment

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
            tempSong=mSong[time*1000:]
        else:
            tempSong = mSong[lTimestamps[index]*1000:lTimestamps[index+1]*1000]
        dTracks[name] = tempSong.export(name + ".mp3", format="mp3", tags={"track": index, "artist": sArtist, "album" : sAlbum})
    print(dTracks.keys())
    return dTracks
