from pydub import AudioSegment
song = AudioSegment.from_mp3("Welcome_to_VA-11_HALL-A.mp3")

#seconds are in milliseconds
first_minute = song[:60000]

#reversing song
backwards = first_minute.reverse()

#getting song length, accounting for default millisecond length
print(len(backwards) / 1000)

#exporting with tags
backwards.export("backwards.mp3", format="mp3", tags={'artist': 'Garoad', 'album': '什麼什麼什麼'})
