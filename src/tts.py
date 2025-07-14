from gtts import gTTS
import streamlit as st
import tempfile
import os
from io import BytesIO

def text_to_speech(text, lang='ar'):
    try:
        # Create gTTS object
        tts = gTTS(text=text, lang=lang, slow=False)
        
        # Save to BytesIO object
        audio_buffer = BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        
        return audio_buffer.getvalue()
    
    except Exception as e:
        st.error(f"Error generating speech: {str(e)}")
        return None