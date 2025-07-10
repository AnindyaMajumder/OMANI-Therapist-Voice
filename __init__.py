from transcribe_whisper import transcribe_audio

transcript = transcribe_audio("voice1.m4a")
for segment in transcript:
        print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))