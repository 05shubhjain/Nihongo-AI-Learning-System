import streamlit as st
from deep_translator import GoogleTranslator
import pandas as pd
import easyocr
from PIL import Image
import numpy as np
from fugashi import Tagger
import unidic_lite
import random
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="🇯🇵 Nihongo AI Ultimate",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- PREMIUM UI ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#0f172a,#111827,#1e293b);
    color: white;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#0f172a,#111827,#1e293b);
    border-right: 2px solid rgba(255,255,255,0.1);
}

[data-testid="stSidebar"] * {
    color: white;
}

.sidebar-title {
    text-align: center;
    font-size: 30px;
    font-weight: bold;
    color: #38bdf8;
    margin-bottom: 10px;
}

.stButton>button {
    background: linear-gradient(90deg,#2563eb,#7c3aed);
    color: white;
    border-radius: 15px;
    border: none;
    padding: 12px;
    font-weight: bold;
    width: 100%;
}

.stButton>button:hover {
    background: linear-gradient(90deg,#7c3aed,#2563eb);
}

.metric-box {
    background: rgba(255,255,255,0.05);
    padding: 15px;
    border-radius: 20px;
    margin-bottom: 15px;
}

.card {
    background: rgba(255,255,255,0.05);
    border-radius: 20px;
    padding: 25px;
    text-align: center;
    box-shadow: 0 4px 15px rgba(0,0,0,0.4);
}

.stTabs [role="tab"] {
    background: rgba(255,255,255,0.05);
    border-radius: 10px;
    padding: 10px;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(90deg,#2563eb,#7c3aed);
}

h1,h2,h3 {
    color: #38bdf8;
}

textarea,input {
    border-radius: 12px !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION ----------------
if "xp" not in st.session_state:
    st.session_state.xp = 0

if "streak" not in st.session_state:
    st.session_state.streak = 1

if "weak_words" not in st.session_state:
    st.session_state.weak_words = []

if "study_history" not in st.session_state:
    st.session_state.study_history = []

level = st.session_state.xp // 50 + 1

# ---------------- CACHE ----------------
@st.cache_data
def load_csv(path):
    return pd.read_csv(path)

# ---------------- HELPERS ----------------
def add_history(action):
    st.session_state.study_history.append(action)

def check_badges():
    badges = []

    if st.session_state.xp >= 50:
        badges.append("🥉 Beginner Learner")

    if st.session_state.xp >= 150:
        badges.append("🥈 Intermediate Learner")

    if st.session_state.xp >= 300:
        badges.append("🥇 Advanced Learner")

    if st.session_state.xp >= 500:
        badges.append("🏆 JLPT Master")

    return badges

# ---------------- PREMIUM SIDEBAR ----------------
with st.sidebar:

    st.markdown(
        """
        <div style='text-align:center;'>
            <h1 style='color:#38bdf8;'>🇯🇵 Nihongo AI</h1>
            <p style='color:#cbd5e1;'>Ultimate Japanese Learning System</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    st.markdown("### ✨ Navigation")

    menu = st.radio(
        "",
        [
            "🏠 Home",
            "🌐 Translator",
            "💬 Phrase Translator",
            "📚 JLPT",
            "🖼 OCR",
            "🧠 Grammar",
            "🃏 Flashcards",
            "🈶 Kanji Trainer",
            "🎯 Daily Challenge",
            "🏆 Achievements",
            "📜 Study History",
            "📊 Dashboard"
        ]
    )

    st.markdown("---")

    st.markdown(
        f"""
        <div style='
            background: rgba(255,255,255,0.05);
            padding: 18px;
            border-radius: 20px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
            margin-bottom:15px;'>
            <h4 style='color:#38bdf8;'>🎮 Your Progress</h4>
            <p>⭐ XP: {st.session_state.xp}</p>
            <p>🚀 Level: {level}</p>
            <p>🔥 Streak: {st.session_state.streak} Days</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.progress((st.session_state.xp % 50)/50)

    st.markdown("---")

    st.markdown(
        """
        <div style='
            background: linear-gradient(90deg,#2563eb,#7c3aed);
            padding:15px;
            border-radius:15px;
            text-align:center;
            font-weight:bold;
            color:white;'>
            🔥 Practice Daily To Unlock New Levels
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------------- PREMIUM HOME ----------------
if menu == "🏠 Home":

    st.markdown(
        """
        <div style='text-align:center; padding:20px;'>
            <h1 style='font-size:50px;'>🇯🇵 Nihongo AI Ultimate</h1>
            <h3 style='color:#cbd5e1;'>Learn Japanese Using AI + JLPT Preparation</h3>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div style='
                background: rgba(255,255,255,0.05);
                padding:30px;
                border-radius:25px;
                box-shadow:0 4px 15px rgba(0,0,0,0.4);'>
                <h2>🌐 Smart Translator</h2>
                <p>Translate Japanese ↔ English instantly.</p>
                <p>Supports phrase-level understanding.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        st.markdown(
            """
            <div style='
                background: rgba(255,255,255,0.05);
                padding:30px;
                border-radius:25px;
                box-shadow:0 4px 15px rgba(0,0,0,0.4);'>
                <h2>📚 JLPT Training</h2>
                <p>Prepare from N5 → N1.</p>
                <p>Vocabulary, Grammar, Reading Practice.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("<br>", unsafe_allow_html=True)

    col3, col4 = st.columns(2)

    with col3:
        st.markdown(
            """
            <div style='
                background: rgba(255,255,255,0.05);
                padding:30px;
                border-radius:25px;
                box-shadow:0 4px 15px rgba(0,0,0,0.4);'>
                <h2>🖼 OCR Scanner</h2>
                <p>Scan Japanese text from images.</p>
                <p>Instant translation + extraction.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col4:
        st.markdown(
            """
            <div style='
                background: rgba(255,255,255,0.05);
                padding:30px;
                border-radius:25px;
                box-shadow:0 4px 15px rgba(0,0,0,0.4);'>
                <h2>🧠 Grammar AI</h2>
                <p>Analyze Japanese sentence structure.</p>
                <p>Word-by-word explanation.</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown("---")

    st.subheader("🚀 Learning Progress")
    st.progress((st.session_state.xp % 100)/100)

    st.info("✨ Practice daily to unlock achievements and level up faster.")
# ---------------- TRANSLATOR ----------------
elif menu == "🌐 Translator":

    st.header("Japanese ↔ English Translator")

    option = st.selectbox("Direction", ["Japanese to English", "English to Japanese"])

    text = st.text_area("Enter Text")

    if st.button("Translate"):

        try:
            if option == "Japanese to English":
                translated = GoogleTranslator(source='ja', target='en').translate(text)
            else:
                translated = GoogleTranslator(source='en', target='ja').translate(text)

            st.success(translated)
            add_history("Used Translator")

        except:
            st.error("Translation Failed")

# ---------------- PHRASE TRANSLATOR ----------------
elif menu == "💬 Phrase Translator":

    st.header("Phrase Translator")

    phrase_input = st.text_input("Enter Phrase")

    try:
        phrase_df = load_csv("datasets/japanese_phrases.csv")
    except:
        phrase_df = pd.DataFrame(columns=["Japanese Phrase","English Meaning"])

    if st.button("Translate Phrase"):

        result = phrase_df[
            phrase_df["Japanese Phrase"].astype(str).str.strip() == phrase_input.strip()
        ]

        if not result.empty:
            st.success(result.iloc[0]["English Meaning"])
            st.session_state.xp += 5
            add_history("Translated Phrase")
        else:
            st.warning("Phrase Not Found")

# ---------------- JLPT ----------------
elif menu == "📚 JLPT":

    st.header("JLPT Preparation")

    jlpt_level = st.selectbox("JLPT Level", ["N5","N4","N3","N2","N1"])

    level_lower = jlpt_level.lower()

    vocab_file = f"datasets/{level_lower}_vocab.csv"
    grammar_file = f"datasets/{level_lower}_grammar.csv"
    reading_file = f"datasets/{level_lower}_reading.csv"

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Vocabulary",
        "Grammar",
        "Reading",
        "Mock Test",
        "Weakness"
    ])

    with tab1:

        if os.path.exists(vocab_file):

            vocab_df = load_csv(vocab_file)
            row = vocab_df.sample(1).iloc[0]

            st.header(row["Japanese"])
            answer = st.text_input("Meaning")

            if st.button("Check Vocabulary"):

                if answer.lower().strip() == str(row["English"]).lower().strip():
                    st.success("Correct")
                    st.session_state.xp += 10
                    add_history("Vocabulary Practice")
                else:
                    st.error(f"Correct Answer: {row['English']}")
                    st.session_state.weak_words.append(row["Japanese"])

    with tab2:

        if os.path.exists(grammar_file):

            grammar_df = load_csv(grammar_file)
            row = grammar_df.sample(1).iloc[0]

            st.write(row["question"])

            options = [
                row["option1"],
                row["option2"],
                row["option3"],
                row["option4"]
            ]

            choice = st.radio("Select", options)

            if st.button("Check Grammar"):

                if choice == row["answer"]:
                    st.success("Correct")
                    st.session_state.xp += 10
                    add_history("Grammar Practice")
                else:
                    st.error(f"Correct Answer: {row['answer']}")

    with tab3:

        if os.path.exists(reading_file):

            reading_df = load_csv(reading_file)
            row = reading_df.sample(1).iloc[0]

            st.write(row["passage"])
            st.write(row["question"])

            options = [
                row["option1"],
                row["option2"],
                row["option3"],
                row["option4"]
            ]

            choice = st.radio("Answer", options)

            if st.button("Check Reading"):

                if choice == row["answer"]:
                    st.success("Correct")
                    st.session_state.xp += 10
                    add_history("Reading Practice")
                else:
                    st.error(f"Correct Answer: {row['answer']}")

    with tab4:

        questions = [
            {"q":"学校 means?","ans":"school"},
            {"q":"猫 means?","ans":"cat"},
            {"q":"水 means?","ans":"water"}
        ]

        q = random.choice(questions)

        st.write(q["q"])

        user_answer = st.text_input("Answer")

        if st.button("Submit Mock"):

            if user_answer.lower() == q["ans"]:
                st.success("Correct")
                st.session_state.xp += 20
                add_history("Mock Test")
            else:
                st.error("Wrong")

    with tab5:

        if len(st.session_state.weak_words) > 0:
            for word in st.session_state.weak_words:
                st.write(f"❌ {word}")
        else:
            st.success("No weak words")

# ---------------- OCR ----------------
elif menu == "🖼 OCR":

    st.header("Japanese OCR Scanner")

    uploaded_file = st.file_uploader("Upload Image", type=["png","jpg","jpeg"])

    if uploaded_file:

        image = Image.open(uploaded_file)
        st.image(image, width=400)

        image_np = np.array(image)

        with st.spinner("Scanning..."):
            reader = easyocr.Reader(['ja'])
            result = reader.readtext(image_np)

        extracted_text = " ".join([text[1] for text in result])

        st.subheader("Extracted Text")
        st.write(extracted_text)

        if extracted_text:
            translated = GoogleTranslator(source='ja', target='en').translate(extracted_text)
            st.success(translated)
            add_history("OCR Scan")

elif menu == "🧠 Grammar":

    st.header("Grammar Explanation")

    sentence = st.text_area("Enter Japanese Sentence")

    if st.button("Explain"):

        translated = GoogleTranslator(source='ja', target='en').translate(sentence)
        st.success(translated)

        try:
            tagger = Tagger('-d "{}"'.format(unidic_lite.DICDIR))

            words = tagger(sentence)

            for word in words:

                jp_word = word.surface

                try:
                    meaning = GoogleTranslator(source='ja', target='en').translate(jp_word)
                except:
                    meaning = "Not Found"

                st.write(f"{jp_word} → {meaning}")

        except Exception as e:
            st.error("Japanese tokenizer failed to load.")
            st.write(e)

# ---------------- FLASHCARDS ----------------
elif menu == "🃏 Flashcards":

    st.header("Japanese Flashcards")

    jlpt_level = st.selectbox("Select Level", ["N5","N4","N3","N2","N1"])

    vocab_file = f"datasets/{jlpt_level.lower()}_vocab.csv"

    if os.path.exists(vocab_file):

        vocab_df = load_csv(vocab_file)
        flashcard = vocab_df.sample(1).iloc[0]

        st.header(flashcard["Japanese"])

        if st.button("Reveal Meaning"):
            st.success(flashcard["English"])
            st.session_state.xp += 5
            add_history("Flashcard Practice")

# ---------------- KANJI ----------------
elif menu == "🈶 Kanji Trainer":

    st.header("Kanji Trainer")

    kanji_data = {
        "日":"Sun/Day",
        "月":"Moon/Month",
        "火":"Fire",
        "水":"Water",
        "木":"Tree",
        "金":"Gold",
        "山":"Mountain",
        "川":"River",
        "人":"Person"
    }

    kanji = random.choice(list(kanji_data.keys()))

    st.header(kanji)

    guess = st.text_input("Meaning")

    if st.button("Check Kanji"):

        if guess.lower() in kanji_data[kanji].lower():
            st.success("Correct")
            st.session_state.xp += 10
            add_history("Kanji Practice")
        else:
            st.error(f"Correct Answer: {kanji_data[kanji]}")

# ---------------- DAILY ----------------
elif menu == "🎯 Daily Challenge":

    st.header("Daily Challenge")

    challenge_word = "学校"

    st.write(f"Meaning of {challenge_word}")

    answer = st.text_input("Answer")

    if st.button("Submit Challenge"):

        if answer.lower() == "school":
            st.success("Challenge Complete")
            st.session_state.xp += 30
            add_history("Daily Challenge")
        else:
            st.error("Wrong")

# ---------------- ACHIEVEMENTS ----------------
elif menu == "🏆 Achievements":

    st.header("Achievements")

    badges = check_badges()

    if badges:
        for badge in badges:
            st.success(badge)
    else:
        st.warning("No badges yet")

# ---------------- HISTORY ----------------
elif menu == "📜 Study History":

    st.header("Study History")

    if len(st.session_state.study_history) > 0:

        for item in st.session_state.study_history:
            st.write(f"📘 {item}")

    else:
        st.info("No history yet")

# ---------------- DASHBOARD ----------------
elif menu == "📊 Dashboard":

    st.header("Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("XP", st.session_state.xp)
    col2.metric("Level", level)
    col3.metric("Weak Words", len(st.session_state.weak_words))

    st.progress((st.session_state.xp % 100)/100)

    st.subheader("Weak Words")

    if len(st.session_state.weak_words) > 0:
        for word in st.session_state.weak_words:
            st.write(word)
    else:
        st.success("No weak words yet")
