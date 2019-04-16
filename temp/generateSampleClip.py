from pydub import AudioSegment

sound1 = AudioSegment.from_mp3("01 - MIDDLE CHILD [Explicit].mp3")

five_sec = 5 * 1000
clip = sound1[66000:66000 + five_sec]

clip.export("clip.mp3", format="mp3")
