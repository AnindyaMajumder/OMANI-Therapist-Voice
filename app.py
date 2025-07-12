import streamlit as st
import tempfile

from audio_recorder_streamlit import audio_recorder
from src.transcribe_whisper import transcribe_audio  
from src.response import response

texts = [
            {
                "role": "system",
                "content": 
                    "أنت أخصائي صحة نفسية متعاطف. استمع بعناية لمشاعر المستخدم، ورد دائمًا باللهجة العمانية الطبيعية. "
                    "كن موجزًا، مشجعًا، وقدم دعمًا نفسيًا دافئًا في كل إجابة."
            }
        ]
text = ""

def recording():
    st.markdown("### 🎤 Record your voice below")
    audio_bytes = audio_recorder(
        text="Click to record",
        icon_size="2x",
        pause_threshold=2.0,
        sample_rate=16000
    )
    if audio_bytes:
        st.success("Audio recorded! 🎉")
        st.audio(audio_bytes, format="audio/wav")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            tmp_file.write(audio_bytes)
            st.session_state["temp_wav_path"] = tmp_file.name
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
            print(f"Transcribing audio from: {st.session_state['temp_wav_path']}")
            transcript = transcribe_audio(st.session_state["temp_wav_path"])
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
        
    print("Done with processing!")