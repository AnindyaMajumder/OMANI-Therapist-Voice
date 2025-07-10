import sounddevice as sd
import numpy as np
import queue
import threading
from faster_whisper import WhisperModel  # type: ignore

samplerate = 16000
block_duration = 0.5  # seconds
chunk_duration = 1
channels = 1

frame_per_block = int(samplerate * block_duration)
frame_per_chunk = int(samplerate * chunk_duration)

audio_queue = queue.Queue()
audio_buffer = []

from faster_whisper import WhisperModel  # type: ignore

model_size = "large-v3"
model = WhisperModel(model_size, device="cpu", compute_type="int8")

def audio_callback(indata, frames, time, status):
    if status:
        print(status)
    audio_queue.put(indata.copy())
    
def recorder():
    with sd.InputStream(samplerate=samplerate, blocksize=frame_per_block, channels=channels, callback=audio_callback):
        print("Listening...")
        while True:
            sd.sleep(100)
            
def transcriber():
    global audio_buffer
    
    while True:
        block = audio_queue.get()
        audio_buffer.append(block)
        
        total_frames = sum(len(b) for b in audio_buffer)
        if total_frames >= frame_per_chunk:
            audio_data = np.concatenate(audio_buffer)[:frame_per_chunk]
            audio_buffer = []
            
            audio_data = audio_data.flatten().astype(np.float32)
            segments, info = model.transcribe(
                audio_data,
                beam_size=1,
                vad_filter=True,
                vad_parameters=dict(min_silence_duration_ms=500)
            )
            
            for segment in segments:
                print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text.strip()}")
                
threading.Thread(target=recorder, daemon=True).start()
transcriber()