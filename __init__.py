from transcribe_whisper import transcribe_audio
from response import response

transcript = transcribe_audio("voice1.m4a")
text = ""

texts = [
            {
                "role": "system",
                "content": "You are a helpful assistant. Always respond in the natural Omani Arabic dialect. Keep your responses concise and empathetic as if you are a therapist."
            }
        ]

for segment in transcript:
        print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
        text += str(segment.text)
        
        if (segment.text == ""):
            texts.append({
                            "role": "user",
                            "content": text
                        } )
            # response = response(text)
            texts.append({
                            "role": "assistant",
                            "content": response
                        })