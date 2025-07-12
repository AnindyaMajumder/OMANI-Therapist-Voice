import streamlit as st

from audio_recorder_streamlit import audio_recorder
from src.transcribe_whisper import transcribe_audio  
from src.response import response

texts = [
            {
                "role": "system",
                "content": "You are a helpful assistant. Always respond in the natural Omani Arabic dialect. Keep your responses concise and empathetic as if you are a therapist."
            }
        ]
text = ""

def recording():
    st.markdown("### 🎤 Record your voice below")
    audio_bytes = audio_recorder(
        text="Click to record",
        icon_size="2x",
        pause_threshold=1.0,
        sample_rate=16000
    )
    if audio_bytes:
        st.success("Audio recorded! 🎉")
        st.audio(audio_bytes, format="audio/wav")
        with open("temp.wav", "wb") as f:
            f.write(audio_bytes)
        st.session_state["audio_ready"] = True
    else:
        st.session_state["audio_ready"] = False

if __name__ == "__main__":
    st.set_page_config(page_title="OMANI Therapist Voice", page_icon="🧑‍⚕️", layout="centered")
    st.title("🧑‍⚕️ Therapist Voice")
    st.markdown(
        """
        <style>
        .stTabs [data-baseweb="tab"] { font-size: 1.2rem; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    tab1, = st.tabs(["🎙️ Audio Input"])
    with tab1:
        recording()

    if st.session_state.get("audio_ready", False):
        st.header("📝 Transcript")
        with st.spinner("Transcribing audio..."):
            transcript = transcribe_audio("temp.wav")
        for segment in transcript:
            st.write(f"**[{segment.start:.2f}s → {segment.end:.2f}s]** {segment.text.strip()}")
            text += str(segment.text)
            
        st.header("🤖 Response")
        with st.spinner("Generating response..."):
            texts.append({
                "role": "user",
                "content": text
            })
            response_text = response(texts)
            texts.append({
                "role": "assistant",
                "content": response_text
            })
            text = ""
        st.write(response_text)