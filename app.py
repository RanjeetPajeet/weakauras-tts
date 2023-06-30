"""
app.py
~~~~~~


"""
import json
import requests
import streamlit as st
from io import BytesIO
from pydub import AudioSegment

st.set_page_config(
    layout     = "centered",
    page_icon  = ":speaker:",
    page_title = "Weakauras TTS",
)
st.markdown(body=\
    """ <style>
    section.main > div {max-width:65rem}
    </style> """, unsafe_allow_html=True
)

def hide_footer():
    st.markdown(body=\
        """ <style>
        footer {visibility:hidden}
        </style> """, unsafe_allow_html=True
    )


def get_mp3(phrase: str, speaker: str, modify: bool = True) -> bytes:
    headers = {
        "Accept": "*/*",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "Content-type": "application/x-www-form-urlencoded",
        "Cookie": "cookieconsent_status=deny",
        "Origin": "https://ttsmp3.com",
        "Referer": "https://ttsmp3.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-origin",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Google",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
    }
    response = requests.request("POST", "https://ttsmp3.com/makemp3_new.php", data=f"msg={phrase}&lang={speaker}&source=ttsmp3", headers=headers)
    url = json.loads(response.text)["URL"]
    response = requests.request("GET", url)
    if modify:
        audio = AudioSegment.from_mp3(BytesIO(response.content))
        silence = AudioSegment.silent(duration=10)
        audio_offset = silence + audio
        audio_left = audio.pan(-1.0)
        audio_right = audio_offset.pan(1.0)
        stereo_sound = audio_left.overlay(audio_right)
        return stereo_sound.export(format="mp3").read()
    return response.content


hide_footer()

st.title("Weakauras TTS")
st.markdown("---")


with st.container():
    st.markdown("### Parameters")
    st.markdown("### ")
    PHRASE = st.text_input(label="Phrase", value="Shatter")
    SPEAKER = st.selectbox(label="Speaker", options=["Joanna", "Justin", "Kendra", "Kimberly", "Matthew", "Joey", "Ivy", "Salli"])

st.markdown("---")

st.markdown("# ")
modify = st.checkbox("Enhance", value=True, help="Enhances the audio to make it sound more \"full\"")

st.markdown("## ")
submit = st.button("Submit")

st.markdown("## ")
preview = st.empty()


if submit:
    hide_footer()
    mp3 = get_mp3(PHRASE, SPEAKER, modify)
    preview.audio(mp3, format="audio/mp3")
