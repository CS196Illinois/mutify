import sys
from pydub import AudioSegment

def __main__(*args):
	combine_clips(*sys.argv[1:])

def combine_clips(*argv):
	clips = []
	for arg in argv:
		clips.append(arg)
	combined = AudioSegment.empty()
	for clip in clips:
		combined += AudioSegment.from_mp3(clip)
	combined.export("combined.mp3", format="mp3")

if __name__ == '__main__':
	__main__(sys.argv)
