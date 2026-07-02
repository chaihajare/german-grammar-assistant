import streamlit as st
from groq import Groq
import json

st.set_page_config(page_title="German Grammar Assistant", page_icon="🇩🇪", layout="centered")

client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ---------- HELPER ----------
def call_groq(prompt):
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        raise RuntimeError(f"Groq API error: {str(e)}")

def parse_json(text):
    try:
        text = text.replace("```json", "").replace("```", "").strip()
        return json.loads(text)
    except json.JSONDecodeError:
        raise ValueError("Could not parse response. Please try again.")

# ---------- FEATURE FUNCTIONS ----------
def get_meaning(sentence):
    prompt = f"""Translate this German sentence to English.
Return only the English translation, nothing else.
German: "{sentence}" """
    return call_groq(prompt)

def get_tense(sentence):
    prompt = f"""You are a German language teacher.
Identify the tense of this German sentence.
German sentence: "{sentence}"

Respond in this exact JSON format:
{{
  "tense": "tense name in German e.g. Perfekt",
  "explanation": "one simple sentence explaining why, max 15 words"
}}
Return only the JSON, nothing else."""
    return parse_json(call_groq(prompt))

def get_cases(sentence):
    prompt = f"""You are a German language teacher.
Analyse the grammatical cases in this German sentence.
German sentence: "{sentence}"

Respond in this exact JSON format:
{{
  "words": [
    {{
      "word": "the word as it appears",
      "base_form": "nominative form e.g. der Apfel",
      "gender": "masculine/feminine/neuter/none",
      "case": "Nominativ/Akkusativ/Dativ/Genitiv",
      "article_change": "e.g. der to einen or none",
      "why": "max 8 words why this case"
    }}
  ]
}}
Return only the JSON, nothing else."""
    return parse_json(call_groq(prompt))

def fix_grammar(sentence):
    prompt = f"""You are a German language teacher.
Check this German sentence for grammar mistakes.
Sentence: "{sentence}"

Respond in this exact JSON format:
{{
  "original": "the original sentence",
  "corrected": "the corrected sentence or same if correct",
  "has_error": true,
  "what_was_wrong": "max 10 words or No mistakes found",
  "rule": "the grammar rule in one line"
}}
Return only the JSON, nothing else."""
    return parse_json(call_groq(prompt))

def get_word_breakdown(sentence):
    prompt = f"""You are a German language teacher.
Break down this German sentence word by word.
German sentence: "{sentence}"

Respond in this exact JSON format:
{{
  "words": [
    {{
      "word": "word as it appears",
      "type": "Verb/Noun/Article/Pronoun/Adverb/Adjective/Preposition",
      "base_form": "dictionary/infinitive form",
      "note": "short useful note or empty string"
    }}
  ]
}}
Return only the JSON, nothing else."""
    return parse_json(call_groq(prompt))

# ---------- DISPLAY FUNCTIONS ----------
def show_meaning(sentence):
    st.markdown("### 📖 Translation")
    try:
        result = get_meaning(sentence)
        st.markdown(f"""
        <div style='background:#f0f7ff;padding:16px;border-radius:10px;border-left:4px solid #2196F3'>
            <span style='font-size:1.2em'>{result}</span>
        </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Translation failed: {str(e)}")

def show_tense(sentence):
    st.markdown("### 🕐 Tense")
    try:
        result = get_tense(sentence)
        tense_colors = {
            "Präsens": "#4CAF50",
            "Perfekt": "#FF9800",
            "Präteritum": "#9C27B0",
            "Futur": "#2196F3",
            "Plusquamperfekt": "#F44336"
        }
        color = next((v for k, v in tense_colors.items()
                     if k.lower() in result["tense"].lower()), "#607D8B")
        st.markdown(f"""
        <div style='background:#fafafa;padding:16px;border-radius:10px;border-left:4px solid {color}'>
            <span style='background:{color};color:white;padding:4px 12px;
                  border-radius:20px;font-weight:bold;font-size:1em'>
                {result["tense"]}
            </span>
            <p style='margin-top:10px;color:#444'>{result["explanation"]}</p>
        </div>
        """, unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Tense analysis failed: {str(e)}")

def show_cases(sentence):
    st.markdown("### 📋 Cases & Gender")
    try:
        result = get_cases(sentence)
        case_colors = {
            "Nominativ": "🔵", "Akkusativ": "🟠",
            "Dativ": "🟢", "Genitiv": "🟣"
        }
        cols = st.columns([2, 2, 2, 2, 3])
        for col, h in zip(cols, ["Word", "Gender", "Case", "Article Change", "Why"]):
            col.markdown(f"**{h}**")
        st.divider()
        for word in result["words"]:
            cols = st.columns([2, 2, 2, 2, 3])
            cols[0].markdown(f"`{word['word']}`")
            cols[1].markdown(word["gender"])
            emoji = case_colors.get(word["case"], "⚪")
            cols[2].markdown(f"{emoji} {word['case']}")
            cols[3].markdown(word["article_change"] if word["article_change"] != "none" else "—")
            cols[4].markdown(f"<small>{word['why']}</small>", unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Case analysis failed: {str(e)}")

def show_fix(sentence):
    st.markdown("### ✏️ Grammar Check")
    try:
        result = fix_grammar(sentence)
        if not result["has_error"]:
            st.success("✅ No grammar mistakes found!")
        else:
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**❌ Your sentence**")
                st.markdown(f"""
                <div style='background:#fff0f0;padding:12px;border-radius:8px;border:1px solid #ffcccc'>
                    {result["original"]}
                </div>""", unsafe_allow_html=True)
            with col2:
                st.markdown("**✅ Corrected**")
                st.markdown(f"""
                <div style='background:#f0fff0;padding:12px;border-radius:8px;border:1px solid #ccffcc'>
                    {result["corrected"]}
                </div>""", unsafe_allow_html=True)
            st.info(f"**What was wrong:** {result['what_was_wrong']}")
            st.caption(f"📌 Rule: {result['rule']}")
    except Exception as e:
        st.error(f"Grammar check failed: {str(e)}")

def show_breakdown(sentence):
    st.markdown("### 🔤 Word-by-Word Breakdown")
    try:
        result = get_word_breakdown(sentence)
        type_colors = {
            "Verb": "#FF9800", "Noun": "#2196F3", "Article": "#9C27B0",
            "Pronoun": "#4CAF50", "Adverb": "#607D8B",
            "Adjective": "#F44336", "Preposition": "#00BCD4"
        }
        cols = st.columns([2, 2, 2, 3])
        for col, h in zip(cols, ["Word", "Type", "Base Form", "Note"]):
            col.markdown(f"**{h}**")
        st.divider()
        for word in result["words"]:
            cols = st.columns([2, 2, 2, 3])
            cols[0].markdown(f"`{word['word']}`")
            color = type_colors.get(word["type"], "#607D8B")
            cols[1].markdown(
                f"<span style='color:{color};font-weight:bold'>{word['type']}</span>",
                unsafe_allow_html=True)
            cols[2].markdown(word["base_form"])
            cols[3].markdown(
                f"<small>{word['note']}</small>" if word["note"] else "—",
                unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Word breakdown failed: {str(e)}")

# ---------- UI ----------
st.title("🇩🇪 German Grammar Assistant")
st.caption("Paste a German sentence — grammar is checked automatically. Choose what else you want to know.")

sentence = st.text_area(
    "", placeholder="e.g. Ich habe gestern einen Apfel gegessen.",
    label_visibility="collapsed"
)

if sentence.strip():
    st.markdown("**What else do you want to know?**")

    # Select All toggle
    select_all = st.checkbox("✅ Select All")

    col1, col2 = st.columns(2)
    with col1:
        do_meaning   = st.checkbox("📖 Translation", value=select_all)
        do_tense     = st.checkbox("🕐 Tense & Why", value=select_all)
    with col2:
        do_cases     = st.checkbox("📋 Cases & Gender", value=select_all)
        do_breakdown = st.checkbox("🔤 Word-by-Word Breakdown", value=select_all)

    if st.button("Analyse ✨", type="primary"):
        # Always show grammar check first, automatically
        show_fix(sentence)
        st.write("")

        # Then show whatever else was selected
        if do_meaning:
            show_meaning(sentence)
            st.write("")
        if do_tense:
            show_tense(sentence)
            st.write("")
        if do_cases:
            show_cases(sentence)
            st.write("")
        if do_breakdown:
            show_breakdown(sentence)
else:
    st.info("👆 Enter a German sentence above to get started.")

st.divider()
st.caption("Built with Groq (Llama 3.3 70B) and Streamlit.")
