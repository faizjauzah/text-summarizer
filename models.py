from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from heapq import nlargest
from PyPDF2 import PdfReader
import docx

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
