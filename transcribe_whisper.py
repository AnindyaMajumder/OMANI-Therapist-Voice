from faster_whisper import WhisperModel # type: ignore

def transcribe_audio(file_path):
    # model_size = "large-v3" 
    model_size = "large-v3"

    # Run on GPU with FP16
    # model = WhisperModel(model_size, device="cuda", compute_type="float16")

    # or run on GPU with INT8
    # model = WhisperModel(model_size, device="cuda", compute_type="int8_float16")
    # or run on CPU with INT8
    model = WhisperModel(model_size, device="cpu", compute_type="int8")

    segments, info = model.transcribe(
        file_path,
        beam_size=3,
        vad_filter=True,
        vad_parameters=dict(min_silence_duration_ms=500)
    )

    # print("Detected language '%s' with probability %f" % (info.language, info.language_probability))
    print(info)
    return segments