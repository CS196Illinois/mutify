from pydub import AudioSegment

five_second_silence = AudioSegment.silent(duration=5000)
five_second_silence.export("five_second_silence.mp3", format="mp3")
