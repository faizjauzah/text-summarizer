WELCOME
# ✍️ Simple Text Summarizer

A web-based application built with Python and Streamlit that summarizes long pieces of text using Natural Language Processing (NLP).

## 📄 Description

This project provides a simple and interactive user interface to perform extractive text summarization. Users can paste any block of text or upload pdf or docx files, select the desired length of the summary in sentences, and get a condensed version of the original text instantly. The app also displays statistics, showing how much the text was reduced.

This is an excellent tool for quickly grasping the main points of a long article, document, or report.

## ✨ Features

* **Interactive UI:** A clean and simple web interface powered by Streamlit.
* **PDF/DOCX Files upload:** Users can upload PDF or DOCX files format to be summarized.
* **Adjustable Summary Length:** Users can control the number of sentences in the final summary using a slider.
* **Extractive Summarization:** Implements a classic NLP technique to identify and extract the most important sentences from the text.
* **Usage Statistics:** Provides metrics on the original vs. summary word/sentence counts and the overall percentage of text reduction.
* **Easy to Run:** Requires minimal setup to get started.

## ⚙️ How It Works

The summarization logic is **extractive**, meaning it selects the most relevant sentences directly from the source text. The process is as follows:

1.  **Tokenization:** The input text is broken down into individual sentences and words.
2.  **Preprocessing:** Common "stop words" (e.g., "the", "a", "is") and punctuation are removed to focus on meaningful words.
3.  **Word Frequency:** The frequency of each remaining word is calculated to identify the most common (and likely most important) terms.
4.  **Sentence Scoring:** Each sentence is scored based on the frequency of the words it contains. Sentences with more high-frequency words receive higher scores.
5.  **Selection:** The top-scoring sentences are selected based on the user's desired summary length.
6.  **Output:** The selected sentences are joined together in their original order to form the final summary.

## 🛠️ Technology Stack

* **Language:** Python 3
* **Web Framework:** Streamlit
* **NLP Library:** NLTK (Natural Language Toolkit)

## 🚀 Setup and Installation

Follow these steps to set up the project on your local machine.

### 1. Prerequisites

Ensure you have Python 3.8 or newer installed on your system.

### 2. Clone the Repository (Optional)

If you are using Git, you can clone the repository. Otherwise, simply save the `index.py` file to a local directory.

```bash
git clone https://github.com/faizjauzah/text-summarizer.git
cd <your-repository-directory>
```

### 3. Install Dependencies

Open your terminal and install the necessary Python libraries.

```
pip install streamlit nltk python-docx PyPDF2
```

### 4. Download NLTK Data

The application requires specific data packages from NLTK (punkt for sentence tokenization and stopwords for filtering). The application is designed to download these automatically. However, if you encounter issues, you can download them manually by running this command in your terminal:

```
python -m nltk.downloader punkt stopwords
```

## ▶️ How to Run the App
1. Navigate to the directory where you saved index.py in your terminal.

2. Run the following command:
```
streamlit run index.py
```
3. Your default web browser will open a new tab with the running application.
