# 🇩🇪 German Grammar Assistant

An AI-powered German grammar analyser built with Groq and Streamlit. Paste any German sentence and choose exactly what you want to understand — no information overload.

🚀 **Live Demo:** 
[![german-grammar-assistant Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://german-grammar-assistant.streamlit.app)

---

## ✨ Features

Select only what you need — results appear cleanly without overwhelming you:

| Feature | What it does |
|---|---|
| 📖 Translation | Clean English translation of your German sentence |
| 🕐 Tense & Why | Identifies the tense with a colour-coded badge and a one-line explanation |
| 📋 Cases & Gender | Table showing each word's gender, case, article change and reason |
| ✏️ Fix My Grammar | Side-by-side view of your sentence vs corrected version with the rule broken |
| 🔤 Word-by-Word Breakdown | Each word's type, base form and usage note in a clean table |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| LLM | Groq API (Llama 3.3 70B) |
| Prompt Engineering | Structured JSON output prompts per feature |
| UI | Streamlit |
| Deployment | Streamlit Community Cloud |

---

## 💡 How It Works

1. User pastes a German sentence
2. Selects which features they want (translation, tense, cases, grammar fix, word breakdown)
3. Each selected feature makes a separate Groq API call with a tailored prompt
4. LLM responds in structured JSON format
5. App parses and displays results in a clean, readable UI

---

## 🚀 Run Locally

```bash
git clone https://github.com/yourusername/german-grammar-assistant
cd german-grammar-assistant
pip install -r requirements.txt
```

Add your Groq API key to `.streamlit/secrets.toml`:
```toml
GROQ_API_KEY = "your_key_here"
```

Then run:
```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
german-grammar-assistant/
├── app.py               # Main Streamlit app
├── requirements.txt     # Dependencies
└── README.md            # This file
```

---

## 🎯 Why I Built This

I am learning German and struggled with grammar cases, tenses and article changes. Most apps either give too little explanation or overwhelm you with information. This assistant lets you choose exactly what you need, one sentence at a time.

---

Built with [Groq](https://groq.com) and [Streamlit](https://streamlit.io)
