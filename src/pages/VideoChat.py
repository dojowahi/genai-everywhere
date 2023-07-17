import streamlit as st
from helpers.vidhelper import (
    palm_embedding,
    palm_ask_doc,
    get_text,
    get_video_transcript,
    streamlit_hide,
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
st.markdown("<h1>Converse with video</h1>", unsafe_allow_html=True)
st.markdown("""---""")


URL = st.text_input("Enter URL of YouTube video:")
user_input = get_text()


if str(URL) == "" or str(user_input) == "":
    st.warning("Awaiting URL and user input for chat.")

if str(URL) != "" or str(user_input) != "":
    if st.button("Submit"):
        with st.spinner(
            "Patience you must have, my young Padawan. Have patience and a Jedi will be assigned..."
        ):
            transcript_file, yt_err_msg = get_video_transcript(URL, bucket_name)
            try:
                t_index_file, embed_msg = palm_embedding(bucket_name, transcript_file)
                if embed_msg is None:
                    response, msg = palm_ask_doc(user_input, t_index_file)
                    st.write(response)
                    st.video(URL)

                else:
                    st.error("Embeddings failure {str(embed_msg)}")
            except Exception as e:
                st.error(
                    f"The greatest teacher, failure is...\n. Embedding creation failed:{str(e)}"
                )
