import streamlit as st

st.set_page_config(layout="wide")

# Customize the sidebar
markdown = """
Web App URL: <https://ee-github-apps-rhvexdce7q-uc.a.run.app>
"""

# st.sidebar.title("About")
# st.sidebar.info(markdown)


hide_st_style = """
                <style>
                #MainMenu {visibility: hidden;}
                header {visibility: hidden;}
                footer:before {content : 'Developed by Ankur Wahi';
                        color: tomato;
                        padding: 5px;
                        top: 3px;
                        }
                footer {background-color: transparent;}
                """
st.markdown(hide_st_style, unsafe_allow_html=True)


# Customize page title
st.title("Gen AI Everywhere All at Once")
st.markdown("""---""")


st.markdown(
    """
    This multipage app template demonstrates various Gen AI web apps created using LLMs.
    The app uses PaLM, Chirp APIs and is deployed on GCE, and uses Github Actions for CI/CD
    """
)

st.header("Instructions")

markdown = """
1. ElephantBot is a conversation bot with an option to save conversations in memory and download them
2. Goldfishbot is a conversation bot with no memory, and can be used to calculate cost of calling the API
3. Video synopsis takes in a youtube URL and returns a five point bullet summary of the video.

"""


st.markdown(markdown)

st.markdown(
    f'<p style="color:#ff0000;font-size:10px;">{"Note: In case of any errors email ankurwahi@"}</p>',
    unsafe_allow_html=True,
)
