# 🌙 Luna — AI Text Summarizer

**Long text in, clear summary out.**

Luna is an AI-powered text summarization web app that turns long, complex text into short, clear, easy-to-read summaries using Google's Gemini AI. It is built with Python and Streamlit and has an animated dark "galaxy" interface.

**Live demo:** https://lunasummarizer-ufadbymqgqqmvc9rxwamol.streamlit.app/


## Features

- **AI-powered summaries** using Google Gemini
- **Three summary lengths:** Short, Balanced, Detailed
- **Three output formats:** Paragraph, Bullet points, Study notes
- **Paste text or upload a file** (`.txt` and `.md`)
- **Live statistics:** word count, character count, and estimated read time
- **Live streaming output** with a typing cursor
- **Download** the summary as a text file
- **Auto-retry and backup models** when the server is busy (503/429 errors)
- **Animated UI:** gradient background, twinkling stars, floating moon, glowing buttons

## Tech Stack

- Python
- Streamlit
- Google Gemini API
- Google Gen AI Python SDK (`google-genai`)
- python-dotenv

## Project Structure

```
LUNA/
├── .streamlit/
│   └── config.toml
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
└── .env            (local only, never commit this)
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Jascinth-Rhema/LUNASUMMARIZER.git
cd LUNASUMMARIZER
```

### 2. Create a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Mac/Linux
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Get a Gemini API key

Create a free key at [Google AI Studio](https://aistudio.google.com/apikey).

### 5. Configure environment variables

Create a `.env` file in the project folder:

```
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-3.5-flash-lite
```

`GEMINI_MODEL` is optional. If it is not set, Luna uses `gemini-3.5-flash-lite`.
Model names change over time, so check the
[Gemini models page](https://ai.google.dev/gemini-api/docs/models) for current names.

> **Security note:** Never upload your API key or `.env` file to GitHub.
> Make sure `.env` is listed in `.gitignore`.

### 6. Run the app

```bash
streamlit run app.py
```

The app opens in your default browser.

## Deployment (Streamlit Community Cloud)

1. Push the project to a GitHub repository (without the `.env` file).
2. Go to [share.streamlit.io](https://share.streamlit.io/) and click **Deploy an app**.
3. Select your repository, set the branch to `main`, and the main file to `app.py`.
4. Open **Advanced settings → Secrets** and add:

```toml
GEMINI_API_KEY = "your_gemini_api_key"
GEMINI_MODEL = "gemini-3.5-flash-lite"
```

5. Click **Deploy**.


## Use Cases

- Summarizing study notes and academic material
- Understanding long articles and documents
- Creating quick revision notes
- Extracting key points from large text

## Future Enhancements

- PDF and DOCX file support
- Multilingual summarization
- Summary history
- Keyword highlighting
- More output formats



This project is for learning and personal use. Add a license (for example MIT) if you plan to share or reuse it.
