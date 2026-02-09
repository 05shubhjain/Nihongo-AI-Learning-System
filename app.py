import streamlit as st
from deep_translator import GoogleTranslator
import pandas as pd

st.set_page_config(page_title="Nihongo AI System", layout="wide")

# ---------------- INTERACTIVE SIDEBAR ----------------

st.sidebar.markdown("## 🇯🇵 Nihongo AI")

# session menu state
if "menu" not in st.session_state:
    st.session_state.menu = "🏠 Home"

# navigation buttons
if st.sidebar.button("🏠 Home", use_container_width=True):
    st.session_state.menu = "🏠 Home"

if st.sidebar.button("🌐 Translator", use_container_width=True):
    st.session_state.menu = "🌐 Translator"

if st.sidebar.button("📚 JLPT", use_container_width=True):
    st.session_state.menu = "📚 JLPT"

if st.sidebar.button("🖼 OCR", use_container_width=True):
    st.session_state.menu = "🖼 OCR"

if st.sidebar.button("🧠 Grammar", use_container_width=True):
    st.session_state.menu = "🧠 Grammar"

st.sidebar.markdown("---")

# progress tracking
if "xp" not in st.session_state:
    st.session_state.xp = 0
    st.session_state.level = 1

st.session_state.level = st.session_state.xp // 50 + 1

st.sidebar.markdown("### 🎮 Progress")

col1, col2 = st.sidebar.columns(2)
col1.metric("Level", st.session_state.level)
col2.metric("XP", st.session_state.xp)

st.sidebar.progress((st.session_state.xp % 50) / 50)

menu = st.session_state.menu

# ---------------- HOME ----------------
if menu == "🏠 Home":

    st.title("🇯🇵 Nihongo AI Learning System")

    st.markdown("""
    ### Learn Japanese using AI 🚀

    - Translate Japanese ↔ English
    - JLPT Preparation
    - OCR Japanese text from images
    - Grammar understanding using NLP
    """)

    col1, col2, col3 ,col4= st.columns(4)
    col1.info("🌐 Translator")
    col2.info("📚 JLPT Learning")
    col3.info("🖼 OCR Scanner")
    col4.info("🧠 Grammar AI")
    

# ---------------- TRANSLATOR ----------------
elif menu == "🌐 Translator":

    st.header("Japanese ↔ English Translator")

    option = st.selectbox(
        "Select Translation Direction",
        ("Japanese to English", "English to Japanese")
    )

    text = st.text_area("Enter text")

    if st.button("Translate"):
        if option == "Japanese to English":
            translated = GoogleTranslator(source='ja', target='en').translate(text)
        else:
            translated = GoogleTranslator(source='en', target='ja').translate(text)

        st.success(translated)

# ---------------- JLPT ----------------
elif menu == "📚 JLPT":

    st.header("JLPT Preparation System")

    # performance tracking
    if "vocab_correct" not in st.session_state:
        st.session_state.vocab_correct = 0
        st.session_state.vocab_total = 0

    if "grammar_correct" not in st.session_state:
        st.session_state.grammar_correct = 0
        st.session_state.grammar_total = 0

    if "reading_correct" not in st.session_state:
        st.session_state.reading_correct = 0
        st.session_state.reading_total = 0

    if "weak_words" not in st.session_state:
        st.session_state.weak_words = []

    # JLPT mini tabs
    jlpt_tab1, jlpt_tab2, jlpt_tab3, jlpt_tab4, jlpt_tab5 = st.tabs([
        "📘 Vocabulary",
        "🧠 Grammar",
        "📖 Reading",
        "📝 Mock Test",
        "📊 Progress"
    ])

    # -------- VOCABULARY --------
    with jlpt_tab1:

        df = pd.read_csv("datasets/n5_vocab.csv")

        if "vocab_word" not in st.session_state:
            st.session_state.vocab_word = df.sample(1).iloc[0]

        word = st.session_state.vocab_word
        japanese_word = word["Japanese"]
        correct_answer = word["English"]

        st.subheader("Vocabulary Trainer")
        st.header(japanese_word)

        user_answer = st.text_input("Enter meaning")

        if st.button("Check Vocabulary"):

            st.session_state.vocab_total += 1

            if user_answer.strip().lower() == correct_answer.strip().lower():
                st.success("Correct 🎉")
                st.session_state.vocab_correct += 1
                st.session_state.xp += 10
            else:
                st.error(f"Wrong! Correct answer: {correct_answer}")
                st.session_state.weak_words.append(japanese_word)

        if st.button("Next Word"):
            st.session_state.vocab_word = df.sample(1).iloc[0]
            st.rerun()

    # -------- GRAMMAR --------
    with jlpt_tab2:

        df = pd.read_csv("datasets/n5_grammar.csv")

        if "grammar_q" not in st.session_state:
            st.session_state.grammar_q = df.sample(1).iloc[0]

        q = st.session_state.grammar_q

        st.subheader("Grammar Practice")
        st.write(q["question"])

        options = [q["option1"], q["option2"], q["option3"], q["option4"]]
        user_choice = st.radio("Choose correct answer", options)

        if st.button("Check Grammar"):

            st.session_state.grammar_total += 1

            if user_choice == q["answer"]:
                st.success("Correct 🎉")
                st.session_state.grammar_correct += 1
                st.session_state.xp += 10
            else:
                st.error(f"Wrong! Correct answer: {q['answer']}")

        if st.button("Next Grammar Question"):
            st.session_state.grammar_q = df.sample(1).iloc[0]
            st.rerun()

    # -------- READING --------
    with jlpt_tab3:

        df = pd.read_csv("datasets/n5_reading.csv")

        if "reading_q" not in st.session_state:
            st.session_state.reading_q = df.sample(1).iloc[0]

        r = st.session_state.reading_q

        st.subheader("Reading Practice")
        st.write(r["passage"])
        st.write(r["question"])

        options = [r["option1"], r["option2"], r["option3"], r["option4"]]
        user_choice = st.radio("Select answer", options)

        if st.button("Check Reading"):

            st.session_state.reading_total += 1

            if user_choice == r["answer"]:
                st.success("Correct 🎉")
                st.session_state.reading_correct += 1
                st.session_state.xp += 10
            else:
                st.error(f"Wrong! Correct answer: {r['answer']}")

        if st.button("Next Reading Question"):
            st.session_state.reading_q = df.sample(1).iloc[0]
            st.rerun()

    # -------- MOCK TEST --------
    with jlpt_tab4:

        st.subheader("Mini JLPT Mock Test")

        questions = [
            {"q": "水 means?", "ans": "water"},
            {"q": "学校 means?", "ans": "school"},
            {"q": "食べる means?", "ans": "eat"}
        ]

        if "mock_index" not in st.session_state:
            st.session_state.mock_index = 0
            st.session_state.mock_score = 0

        q = questions[st.session_state.mock_index]

        st.write(q["q"])

        user_answer = st.text_input("Your answer")

        if st.button("Submit Answer"):

            if user_answer.lower() == q["ans"]:
                st.session_state.mock_score += 1

            st.session_state.mock_index += 1

            if st.session_state.mock_index >= len(questions):
                st.write(f"Final Score: {st.session_state.mock_score}/{len(questions)}")
            else:
                st.rerun()

    # -------- PROGRESS --------
    with jlpt_tab5:

        st.subheader("🎮 Learning Status")
        st.write(f"Level: {st.session_state.level}")
        st.write(f"XP Points: {st.session_state.xp}")
        st.progress((st.session_state.xp % 50) / 50)

# ---------------- OCR ----------------
elif menu == "🖼 OCR":

    st.header("Japanese Image Scanner")

    import easyocr
    from PIL import Image
    import numpy as np

    uploaded_file = st.file_uploader("Upload Japanese image", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:

        image = Image.open(uploaded_file)
        st.image(image, width=400)

        image_np = np.array(image)

        reader = easyocr.Reader(['ja'])
        result = reader.readtext(image_np)

        extracted_text = " ".join([text[1] for text in result])

        st.write(extracted_text)

        if extracted_text.strip() != "":
            translated = GoogleTranslator(source='ja', target='en').translate(extracted_text)
            st.success(translated)

# ---------------- GRAMMAR ----------------
elif menu == "🧠 Grammar":

    st.header("Japanese Grammar Explanation")

    from fugashi import Tagger

    sentence = st.text_area("Enter Japanese sentence")

    if st.button("Explain Sentence"):

        translated = GoogleTranslator(source='ja', target='en').translate(sentence)
        st.success(translated)

        tagger = Tagger()
        words = tagger(sentence)

        for word in words:
            jp_word = word.surface
            meaning = GoogleTranslator(source='ja', target='en').translate(jp_word)
            st.write(f"{jp_word} → {meaning}")
