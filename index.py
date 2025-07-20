import streamlit as st
from setup_nltk import setup_nltk
from models import extract_text_from_pdf, extract_text_from_docx, summarize_text
from nltk.tokenize import sent_tokenize

setup_nltk()


# --- Streamlit User Interface ---

# Set the page configuration for the app
st.set_page_config(
    page_title="Text Summarizer",
    page_icon="✍️",
    layout="wide"
)

# Main title of the app
st.title("✍️ Simple Text Summarizer")
st.markdown("""
This app uses an extractive summarization technique to create a summary of your text. 
Paste your text below, choose the desired summary length, and click 'Summarize'.
""")

# --- File Upload Section ---
uploaded_file = st.file_uploader("Upload a PDF or Word (.docx) file", type=["pdf", "docx"])

uploaded_text = ""
if uploaded_file is not None:
    if uploaded_file.type == "application/pdf":
        uploaded_text = extract_text_from_pdf(uploaded_file)
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        uploaded_text = extract_text_from_docx(uploaded_file)
    else:
        st.warning("Unsupported file type.")

# Text area for user input
if uploaded_text:
    st.info("Text extracted from file. You can still edit below if needed.")
    text_input = st.text_area("Extracted text:", value=uploaded_text, height=250)
else:
    text_input = st.text_area("Paste your text here:", height=250, placeholder="Enter a long piece of text you want to summarize...")

# Slider to select the number of sentences in the summary
num_sentences_slider = st.slider(
    "Select the desired number of sentences for the summary:",
    min_value=1,
    max_value=30,  
    value=3,
    step=1
)


# Button to trigger the summarization
if st.button("Summarize", type="primary"):
    if text_input:
        # The core logic is now safely inside the button-press event
        with st.spinner("Summarizing..."):
            available_sentences = len(sent_tokenize(text_input))

            if available_sentences == 0:
                st.warning("Could not find any sentences in the provided text.")
            else:
                # Ensure we don't ask for more sentences than are available
                num_to_summarize = min(num_sentences_slider, available_sentences)

                summary, stats = summarize_text(text_input, num_to_summarize)

                st.subheader("Summary")
                st.success(summary)

                st.subheader("Statistics")
                reduction_percentage = 100 - (stats['summary_word_count'] / stats['original_word_count'] * 100) if stats['original_word_count'] > 0 else 0

                col1, col2 = st.columns(2)
                with col1:
                    st.metric(label="Original Word Count", value=stats['original_word_count'])
                    st.metric(label="Summary Word Count", value=stats['summary_word_count'])
                with col2:
                    st.metric(label="Original Sentence Count", value=stats['original_sentence_count'])
                    st.metric(label="Summary Sentence Count", value=stats['summary_sentence_count'])

                st.metric(label="Text Reduction", value=f"{reduction_percentage:.2f}%")
    else:
        st.warning("Please paste some text into the text box above.")

st.markdown("---")