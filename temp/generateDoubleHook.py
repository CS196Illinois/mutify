from pydub import AudioSegment

sound1 = AudioSegment.from_mp3("01 - MIDDLE CHILD [Explicit].mp3")

sev_sec = 7 * 1000
first_7 = sound1[:sev_sec]
last_5 = sound1[-5000:]
beginning = first_7 + 6
end = last_5 - 3
cropped = beginning + end
cropped == 12.0
faded = beginning.append(end, crossfade=1500)
faded_x2 = faded * 2

double_hook = faded_x2.fade_in(2000).fade_out(3000)
double_hook.export("mashup.mp3", format="mp3")
