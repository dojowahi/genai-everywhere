import streamlit as st
from helpers.vidhelper import (
    streamlit_hide,
    get_video_transcript,
    langchain_summarize,
)
import logging
import os
from dotenv import load_dotenv

load_dotenv()

# Custom functions
bucket_name = os.getenv("bucket_name")
project_id = os.getenv("project_id")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
streamlit_hide()
st.markdown("<h1>Video Synopsis</h1>", unsafe_allow_html=True)
st.markdown("""---""")

st.sidebar.header("Input parameter")


with st.sidebar.form(key="my_form"):
    URL = st.text_input("Enter URL of YouTube video:")
    submit_button = st.form_submit_button(label="Summarize")


if str(URL) == "":
    st.warning(
        "Awaiting URL input or uploaded video file in the sidebar for transcription."
    )


# Run custom functions if file uploaded or URL is entered
if submit_button:
    if str(URL) != "":
        with st.spinner(
            "Patience you must have, my young Padawan. Have patience and all will be revealed..."
        ):
            st.sidebar.video(URL)
            transcript_file, yt_err_msg = get_video_transcript(URL, bucket_name)
            if transcript_file:
                summary, summary_err_msg = langchain_summarize(
                    bucket_name, transcript_file
                )
                # aud_nm, summary, yt_err_msg = download_youtube_audio(
                #     URL, bucket_name, project_id
                # )
                # st.sidebar.write(title)
                if summary:
                    logger.info(f"Summary of {URL} is {summary}")
                    st.markdown("### PaLM API Output")
                    st.success(summary)
                else:
                    st.error(
                        f"The greatest teacher, failure is...{URL} summarization failure {str(summary_err_msg)}!"
                    )
            else:
                st.error(
                    f"The greatest teacher, failure is...{URL} transcription failure {str(yt_err_msg)}!"
                )

    else:
        st.sidebar.warning("Please provide youtube URL")
        raise Exception("You must provide a youtube URL !")
