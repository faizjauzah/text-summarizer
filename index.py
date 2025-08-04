import streamlit as st
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from heapq import nlargest
import nltk
from PyPDF2 import PdfReader
import docx

@st.cache_resource
def setup_nltk():
    try:
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('punkt_tab', quiet=True)
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        st.error("NLTK 'punkt' data not found. Automatic download might have failed.")
        st.info("Please run the following command in your terminal to download the necessary data manually, and then refresh this page:")
        st.code("python -m nltk.downloader punkt stopwords")
        st.stop()
    except Exception as e:
        st.error(f"An error occurred while setting up NLTK data: {e}")
        st.info("Please ensure you have an internet connection and refresh the page.")
        st.stop()

# Run the setup
setup_nltk()

def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def extract_text_from_docx(file):
    doc = docx.Document(file)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text


def summarize_text(text, num_sentences):
   
    # --- 1. Tokenization & Preprocessing ---

    sentences = sent_tokenize(text)
    if not sentences:
        return "", {}

    words = word_tokenize(text.lower())

    stop_words = set(stopwords.words('english'))

    punctuation = set(['.', ',', '!', '?', ';', ':', '"', "'", '(', ')', '[', ']', '{', '}'])
    stop_words.update(punctuation)

    filtered_words = [word for word in words if word not in stop_words]

    # --- 2. Word Frequency Calculation ---

    word_frequencies = {}
    for word in filtered_words:
        if word not in word_frequencies:
            word_frequencies[word] = 1
        else:
            word_frequencies[word] += 1

    # --- 3. Sentence Scoring ---

    sentence_scores = {}
    for sentence in sentences:
        sentence_words = word_tokenize(sentence.lower())
        score = 0
        for word in sentence_words:
            if word in word_frequencies:
                score += word_frequencies[word]
        if len(sentence_words) > 0:
            sentence_scores[sentence] = score / len(sentence_words)
        else:
            sentence_scores[sentence] = 0


    # --- 4. Select Top Sentences ---

    summary_sentences = nlargest(num_sentences, sentence_scores, key=sentence_scores.get)

    # --- 5. Generate Summary ---

    original_sentence_order = [sent for sent in sentences if sent in summary_sentences]
    summary = ' '.join(original_sentence_order)

    # --- 6. Gather Statistics ---
    stats = {
        "original_char_count": len(text),
        "original_word_count": len(words),
        "original_sentence_count": len(sentences),
        "summary_char_count": len(summary),
        "summary_word_count": len(word_tokenize(summary)),
        "summary_sentence_count": len(summary_sentences),
    }

    return summary, stats

# --- Streamlit User Interface ---

st.set_page_config(
    page_title="Text Summarizer",
    page_icon="✍️",
    layout="wide"
)

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
    max_value=20,
    value=3,
    step=1
)


# Button to trigger the summarization
if st.button("Summarize", type="primary"):
    if text_input:
        with st.spinner("Summarizing..."):
            available_sentences = len(sent_tokenize(text_input))

            if available_sentences == 0:
                st.warning("Could not find any sentences in the provided text.")
            else:
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
