import streamlit as st
import nltk

@st.cache_resource
def setup_nltk():
    try:
        # Attempt to download the necessary packages quietly.
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('punkt_tab', quiet=True)
        # After downloading, explicitly verify that the 'punkt' tokenizer data can be found.
        # This is the crucial step to confirm the download was successful and accessible.
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        # This block runs if the verification fails, which is the cause of the error.
        st.error("NLTK 'punkt' data not found. Automatic download might have failed.")
        st.info("Please run the following command in your terminal to download the necessary data manually, and then refresh this page:")
        # Provide a clear, copyable command for the user.
        st.code("python -m nltk.downloader punkt stopwords")
        st.stop() # Stop the app from running further to prevent the error.
    except Exception as e:
        # Catch other potential errors during download (e.g., no internet connection).
        st.error(f"An error occurred while setting up NLTK data: {e}")
        st.info("Please ensure you have an internet connection and refresh the page.")
        st.stop()

