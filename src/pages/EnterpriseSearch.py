import streamlit as st
from helpers.searchhelper import search_with_summary, search_enterprise_search
from helpers.vidhelper import streamlit_hide
import logging
import os
from dotenv import load_dotenv

load_dotenv()

# Custom functions
location = os.getenv("region")
project_id = os.getenv("project_id")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
streamlit_hide()
st.markdown("<h1>Gen AI Enterprise Search - Movie Buff</h1>", unsafe_allow_html=True)
st.markdown("""---""")

with st.sidebar:
    usr_project_id = st.text_input("Project Id:")
    search_engine_id = st.text_input("Search Engine Id:", value="movie_1689531636605")
    temperature = st.slider("Temperature", 0.0, 1.0, 0.0, 0.01, format="%.2f")
    # prompt = st.text_area(
    #     "Prompt Template",
    #     value='Based on the following search results obtained from the query "{search_query}", generate a comprehensive and understandable summary that provides a relevant answer to the query. Please ensure to include only information present in the given data and refrain from citing external sources.',
    # )

query = st.text_input(
    "Ask a question", placeholder="Who were the actors in Squid Games?"
)
submit_button = st.button(label="Analyze")

if str(query) == "" or str(search_engine_id) == "" or str(usr_project_id) == "":
    st.warning("Awaiting URL and user input for chat.")

if submit_button:
    if str(query) != "" and str(search_engine_id) != "" and str(usr_project_id) != "":
        with st.spinner("Genie working..."):
            output, df = search_with_summary(
                usr_project_id, location, search_engine_id, temperature, query
            )
            (
                results,
                request_url,
                request_json,
                response_json,
            ) = search_enterprise_search(project_id, location, search_engine_id, query)
            st.caption("Output from ES")
            st.dataframe(df)
            st.caption("Output after summarization")
            st.write(output.text)
        # st.write(results)
        # st.write(response_json)
