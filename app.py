import io
import re
import time
import random
from gtts import gTTS
import streamlit as st
import pandas as pd

st.set_page_config(page_title='Fala Português', page_icon='🇵🇹', layout='centered')

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --green: #1a6b3c;
    --gold: #c9a84c;
    --cream: #f5f0e8;
    --dark: #1a1a1a;
    --red: #b03a2e;
    --light-green: #e8f0eb;
    --border: #d4cfc6;
    --muted: #6b6560;
}

* { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background-color: var(--cream) !important;
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stSidebar"] {
    background: var(--green) !important;
    border-right: none !important;
}

[data-testid="stSidebar"] * {
    color: var(--cream) !important;
}

[data-testid="stSidebar"] .stRadio label {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.95rem !important;
    padding: 8px 0 !important;
    letter-spacing: 0.02em;
}

[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
    font-family: 'Playfair Display', serif !important;
    font-size: 1.1rem !important;
    font-style: italic;
    opacity: 0.85;
}

h1, h2, h3 {
    font-family: 'Playfair Display', serif !important;
    color: var(--dark) !important;
}

.page-header {
    border-bottom: 2px solid var(--gold);
    padding-bottom: 12px;
    margin-bottom: 28px;
}

.page-header h1 {
    font-size: 2.4rem !important;
    margin: 0 !important;
    letter-spacing: -0.02em;
}

.page-header p {
    color: var(--muted);
    font-size: 0.9rem;
    margin-top: 4px;
    font-family: 'DM Sans', sans-serif;
}

.flashcard {
    background: white;
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 48px 36px;
    text-align: center;
    box-shadow: 0 4px 24px rgba(0,0,0,0.07);
    margin: 20px 0;
}

.flashcard .pt-word {
    font-family: 'Playfair Display', serif;
    font-size: 3.2rem;
    color: var(--green);
    letter-spacing: -0.02em;
    line-height: 1.1;
    margin-bottom: 8px;
}

.flashcard .pos-badge {
    display: inline-block;
    background: var(--light-green);
    color: var(--green);
    border: 1px solid #b8d4bf;
    border-radius: 2px;
    padding: 3px 12px;
    font-size: 0.78rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    font-weight: 500;
    margin-bottom: 16px;
}

.answer-card {
    background: white;
    border-left: 4px solid var(--green);
    border-radius: 0 4px 4px 0;
    padding: 20px 24px;
    margin: 8px 0;
}

.answer-card .en-word {
    font-family: 'Playfair Display', serif;
    font-size: 1.6rem;
    color: var(--dark);
    margin-bottom: 10px;
}

.example-sentence {
    background: var(--light-green);
    border-radius: 4px;
    padding: 16px 20px;
    margin: 8px 0;
    font-size: 1.0rem;
    color: var(--dark);
    line-height: 1.6;
    border: 1px solid #b8d4bf;
}

.example-sentence .translation {
    color: var(--muted);
    font-size: 0.875rem;
    font-style: italic;
    margin-top: 6px;
}

.quiz-word-display {
    background: var(--green);
    color: var(--cream) !important;
    border-radius: 4px;
    padding: 32px 24px;
    text-align: center;
    margin: 16px 0;
}

.quiz-word-display .pt-word {
    font-family: 'Playfair Display', serif;
    font-size: 2.8rem;
    color: white;
    margin-bottom: 4px;
}

.quiz-word-display .hint {
    opacity: 0.75;
    font-size: 0.9rem;
    font-style: italic;
}

.choice-btn-correct {
    background: #d4edda !important;
    border: 2px solid var(--green) !important;
    color: var(--green) !important;
    font-weight: 600 !important;
}

.choice-btn-wrong {
    background: #f8d7da !important;
    border: 2px solid var(--red) !important;
    color: var(--red) !important;
}

.result-correct {
    background: #d4edda;
    border: 1px solid #a3d4af;
    border-radius: 4px;
    padding: 16px 20px;
    margin: 12px 0;
    color: #1a5c2a;
    font-weight: 500;
}

.result-wrong {
    background: #f8d7da;
    border: 1px solid #e8b4b8;
    border-radius: 4px;
    padding: 16px 20px;
    margin: 12px 0;
    color: var(--red);
    font-weight: 500;
}

.stButton > button {
    background: white !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 3px !important;
    color: var(--dark) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 10px 20px !important;
    transition: all 0.15s ease !important;
    letter-spacing: 0.01em;
}

.stButton > button:hover {
    border-color: var(--green) !important;
    color: var(--green) !important;
    background: var(--light-green) !important;
}

.stButton > button[kind="primary"] {
    background: var(--green) !important;
    border-color: var(--green) !important;
    color: white !important;
}

.stButton > button[kind="primary"]:hover {
    background: #145430 !important;
    color: white !important;
}

.stTextInput > div > div > input {
    border: 1.5px solid var(--border) !important;
    border-radius: 3px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    background: white !important;
    color: var(--dark) !important;
    padding: 10px 14px !important;
}

.stTextInput > div > div > input:focus {
    border-color: var(--green) !important;
    box-shadow: 0 0 0 3px rgba(26,107,60,0.12) !important;
}

.score-display {
    display: flex;
    gap: 16px;
    margin: 0 0 24px 0;
}

.score-box {
    background: white;
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 14px 20px;
    flex: 1;
    text-align: center;
}

.score-box .score-num {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    color: var(--green);
    line-height: 1;
}

.score-box .score-label {
    font-size: 0.75rem;
    color: var(--muted);
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 4px;
}

.listening-card {
    background: white;
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 40px 32px;
    text-align: center;
    margin: 16px 0;
    position: relative;
    overflow: hidden;
}

.listening-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
    background: linear-gradient(90deg, var(--green), var(--gold));
}

.listening-card .listen-label {
    font-size: 0.78rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 20px;
}

.pairs-card {
    background: white;
    border: 1.5px solid var(--border);
    border-radius: 4px;
    padding: 18px;
    text-align: center;
    cursor: pointer;
    transition: all 0.15s ease;
    min-height: 80px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'DM Sans', sans-serif;
    font-size: 1.05rem;
    color: var(--dark);
}

.pairs-card:hover {
    border-color: var(--green);
    background: var(--light-green);
}

.pairs-selected {
    border-color: var(--gold) !important;
    background: #fdf8ec !important;
    font-weight: 600;
}

.pairs-matched {
    border-color: var(--green) !important;
    background: var(--light-green) !important;
    color: var(--green) !important;
    font-weight: 600;
}

.pairs-wrong {
    border-color: var(--red) !important;
    background: #f8d7da !important;
    color: var(--red) !important;
}

.progress-bar-container {
    background: var(--border);
    border-radius: 2px;
    height: 6px;
    margin: 0 0 20px 0;
    overflow: hidden;
}

.progress-bar-fill {
    background: var(--green);
    height: 100%;
    border-radius: 2px;
    transition: width 0.4s ease;
}

.section-divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 24px 0;
}

[data-testid="stAudio"] {
    margin: 12px 0;
}

.stMarkdown p {
    font-family: 'DM Sans', sans-serif;
    color: var(--dark);
}

.stAlert {
    border-radius: 4px !important;
}

div[data-testid="stForm"] {
    border: none !important;
    padding: 0 !important;
}

.sidebar-logo {
    font-family: 'Playfair Display', serif;
    font-size: 1.6rem;
    font-weight: 700;
    color: white !important;
    padding: 8px 0 4px 0;
    display: block;
}

.sidebar-sub {
    font-size: 0.8rem;
    opacity: 0.65;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    display: block;
    margin-bottom: 24px;
    font-style: normal !important;
    font-family: 'DM Sans', sans-serif !important;
}
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    try:
        df = pd.read_csv('vocab.csv')
        for col in df.columns:
            if df[col].dtype == 'object':
                df[col] = df[col].astype(str).str.strip()
        return df
    except Exception:
        return pd.DataFrame()

df = load_data()

@st.cache_data
def speak_portuguese(text):
    tts = gTTS(text=text, lang='pt', tld='pt')
    audio_buffer = io.BytesIO()
    tts.write_to_fp(audio_buffer)
    audio_buffer.seek(0)
    return audio_buffer

st.sidebar.markdown('<span class="sidebar-logo">Fala Português</span>', unsafe_allow_html=True)
st.sidebar.markdown('<span class="sidebar-sub">European Portuguese</span>', unsafe_allow_html=True)

page = st.sidebar.radio(
    "Navigation",
    ["Flashcards", "Quiz", "Fill in the Blanks", "Listening Challenge", "Word Pairs", "Speed Round"],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
if not df.empty:
    st.sidebar.markdown(f"**{len(df)}** words in your deck")


if page == "Flashcards":
    st.markdown('<div class="page-header"><h1>Flashcards</h1><p>Study vocabulary at your own pace</p></div>', unsafe_allow_html=True)

    if df.empty:
        st.warning("vocab.csv is empty or missing!")
    else:
        if 'current_index' not in st.session_state:
            st.session_state.current_index = random.randint(0, len(df) - 1)
        if 'show_answer' not in st.session_state:
            st.session_state.show_answer = False
        if 'fc_seen' not in st.session_state:
            st.session_state.fc_seen = 0

        word_data = df.iloc[st.session_state.current_index]

        progress = min(st.session_state.fc_seen / max(len(df), 1), 1.0)
        st.markdown(f'<div class="progress-bar-container"><div class="progress-bar-fill" style="width:{progress*100:.0f}%"></div></div>', unsafe_allow_html=True)

        st.markdown(f"""
        <div class="flashcard">
            <div class="pt-word">{word_data['portuguese']}</div>
            <div class="pos-badge">{word_data['part_of_speech']}</div>
        </div>
        """, unsafe_allow_html=True)

        audio_file = speak_portuguese(word_data['portuguese'])
        st.audio(audio_file, format='audio/mp3')

        if st.session_state.show_answer:
            st.markdown(f"""
            <div class="answer-card">
                <div class="en-word">{word_data['english']}</div>
            </div>
            """, unsafe_allow_html=True)
            st.markdown(f"""
            <div class="example-sentence">
                {word_data['example_pt']}
                <div class="translation">{word_data['example_en']}</div>
            </div>
            """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Show Answer", use_container_width=True):
                st.session_state.show_answer = True
                st.rerun()
        with col2:
            if st.button("Next Word →", use_container_width=True, type="primary"):
                st.session_state.current_index = random.randint(0, len(df) - 1)
                st.session_state.show_answer = False
                st.session_state.fc_seen += 1
                st.rerun()


elif page == "Quiz":
    st.markdown('<div class="page-header"><h1>Vocabulary Quiz</h1><p>Select the correct English translation</p></div>', unsafe_allow_html=True)

    if df.empty or len(df) < 4:
        st.warning("You need at least 4 words in your database for the quiz.")
    else:
        if 'quiz_score' not in st.session_state:
            st.session_state.quiz_score = 0
        if 'quiz_total' not in st.session_state:
            st.session_state.quiz_total = 0

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f'<div class="score-box"><div class="score-num">{st.session_state.quiz_score}</div><div class="score-label">Correct</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="score-box"><div class="score-num">{st.session_state.quiz_total}</div><div class="score-label">Attempted</div></div>', unsafe_allow_html=True)
        with col3:
            pct = int(st.session_state.quiz_score / max(st.session_state.quiz_total, 1) * 100)
            st.markdown(f'<div class="score-box"><div class="score-num">{pct}%</div><div class="score-label">Accuracy</div></div>', unsafe_allow_html=True)

        if "quiz_word" not in st.session_state:
            correct_row = df.sample(n=1).iloc[0]
            wrong_choices = df[df['english'] != correct_row['english']].sample(n=3)['english'].tolist()
            all_choices = wrong_choices + [correct_row['english']]
            random.shuffle(all_choices)
            st.session_state.quiz_word = correct_row
            st.session_state.quiz_choices = all_choices
            st.session_state.quiz_answered = False
            st.session_state.selected_answer = None

        current_q = st.session_state.quiz_word
        choices = st.session_state.quiz_choices

        st.markdown(f"""
        <div class="quiz-word-display">
            <div class="pt-word">{current_q['portuguese']}</div>
            <div class="hint">{current_q['part_of_speech']}</div>
        </div>
        """, unsafe_allow_html=True)

        quiz_audio = speak_portuguese(current_q['portuguese'])
        st.audio(quiz_audio, format='audio/mp3')

        for choice in choices:
            if st.button(choice, key=f"quiz_{choice}", use_container_width=True, disabled=st.session_state.quiz_answered):
                st.session_state.quiz_answered = True
                st.session_state.selected_answer = choice
                st.session_state.quiz_total += 1
                if choice == current_q['english']:
                    st.session_state.quiz_score += 1
                st.rerun()

        if st.session_state.quiz_answered:
            user_ans = st.session_state.selected_answer
            correct_ans = current_q['english']
            if user_ans == correct_ans:
                st.markdown('<div class="result-correct">✓ Correct!</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="result-wrong">✗ Incorrect — you selected "{user_ans}"</div>', unsafe_allow_html=True)

            st.markdown(f"""
            <div class="example-sentence">
                <strong>{current_q['portuguese']}</strong> = {correct_ans}<br>
                {current_q['example_pt']}
                <div class="translation">{current_q['example_en']}</div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("Next Question →", type="primary", use_container_width=True):
                del st.session_state.quiz_word
                del st.session_state.quiz_choices
                del st.session_state.quiz_answered
                del st.session_state.selected_answer
                st.rerun()


elif page == "Fill in the Blanks":
    st.markdown('<div class="page-header"><h1>Fill in the Blanks</h1><p>Active recall — type the missing Portuguese word</p></div>', unsafe_allow_html=True)

    if df.empty:
        st.warning("Your database is empty.")
    else:
        if 'cloze_score' not in st.session_state:
            st.session_state.cloze_score = 0
        if 'cloze_total' not in st.session_state:
            st.session_state.cloze_total = 0
        if "cloze_counter" not in st.session_state:
            st.session_state.cloze_counter = 0
        if "cloze_word" not in st.session_state:
            st.session_state.cloze_word = df.sample(n=1).iloc[0]
            st.session_state.cloze_answered = False
            st.session_state.cloze_correct = False

        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f'<div class="score-box"><div class="score-num">{st.session_state.cloze_score}/{st.session_state.cloze_total}</div><div class="score-label">Score</div></div>', unsafe_allow_html=True)
        with col2:
            pct = int(st.session_state.cloze_score / max(st.session_state.cloze_total, 1) * 100)
            st.markdown(f'<div class="score-box"><div class="score-num">{pct}%</div><div class="score-label">Accuracy</div></div>', unsafe_allow_html=True)

        current_q = st.session_state.cloze_word
        pt_word = current_q['portuguese']
        pt_sentence = current_q['example_pt']
        en_sentence = current_q['example_en']

        pattern = re.compile(r'\b' + re.escape(pt_word) + r'\b', re.IGNORECASE)
        masked_sentence = pattern.sub("______", pt_sentence)

        if masked_sentence == pt_sentence:
            st.info(f"Note: '{pt_word}' may appear conjugated in this sentence.")

        st.markdown(f"""
        <div class="flashcard" style="text-align:left; padding: 32px 28px;">
            <div style="font-size:1.3rem; line-height:1.7; font-family:'Playfair Display',serif; margin-bottom:12px;">{masked_sentence}</div>
            <div style="color:var(--muted); font-size:0.9rem; font-style:italic;">{en_sentence}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f'<div style="background:#fdf8ec; border:1px solid #e8d9a0; border-radius:4px; padding:12px 16px; margin-bottom:16px; font-size:0.9rem; color:var(--dark);">Hint: The word means <strong>{current_q["english"]}</strong> ({current_q["part_of_speech"]})</div>', unsafe_allow_html=True)

        with st.form(key=f"cloze_form_{st.session_state.cloze_counter}"):
            user_input = st.text_input("Type the missing word:", key=f"cloze_input_{st.session_state.cloze_counter}", placeholder="Portuguese word…")
            submit_button = st.form_submit_button(label="Check Answer", use_container_width=True)

        if submit_button:
            st.session_state.cloze_answered = True
            st.session_state.cloze_total += 1
            if user_input.strip().lower() == pt_word.lower():
                st.session_state.cloze_correct = True
                st.session_state.cloze_score += 1
            else:
                st.session_state.cloze_correct = False

        if st.session_state.cloze_answered:
            if st.session_state.cloze_correct:
                st.markdown('<div class="result-correct">✓ Correct! Excellent recall.</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="result-wrong">✗ The correct word was: <strong>{pt_word}</strong></div>', unsafe_allow_html=True)

            full_audio = speak_portuguese(pt_sentence)
            st.audio(full_audio, format='audio/mp3')

            if st.button("Next Sentence →", type="primary", use_container_width=True):
                st.session_state.cloze_counter += 1
                del st.session_state.cloze_word
                del st.session_state.cloze_answered
                del st.session_state.cloze_correct
                st.rerun()


elif page == "Listening Challenge":
    st.markdown('<div class="page-header"><h1>Listening Challenge</h1><p>Listen and identify the Portuguese word you hear</p></div>', unsafe_allow_html=True)

    if df.empty or len(df) < 4:
        st.warning("You need at least 4 words in your database.")
    else:
        if 'listen_score' not in st.session_state:
            st.session_state.listen_score = 0
        if 'listen_total' not in st.session_state:
            st.session_state.listen_total = 0

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f'<div class="score-box"><div class="score-num">{st.session_state.listen_score}</div><div class="score-label">Correct</div></div>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<div class="score-box"><div class="score-num">{st.session_state.listen_total}</div><div class="score-label">Attempted</div></div>', unsafe_allow_html=True)
        with col3:
            pct = int(st.session_state.listen_score / max(st.session_state.listen_total, 1) * 100)
            st.markdown(f'<div class="score-box"><div class="score-num">{pct}%</div><div class="score-label">Accuracy</div></div>', unsafe_allow_html=True)

        if "listen_word" not in st.session_state:
            correct_row = df.sample(n=1).iloc[0]
            wrong_choices = df[df['portuguese'] != correct_row['portuguese']].sample(n=3)['portuguese'].tolist()
            all_choices = wrong_choices + [correct_row['portuguese']]
            random.shuffle(all_choices)
            st.session_state.listen_word = correct_row
            st.session_state.listen_choices = all_choices
            st.session_state.listen_answered = False
            st.session_state.listen_selected = None

        current_q = st.session_state.listen_word
        choices = st.session_state.listen_choices

        st.markdown("""
        <div class="listening-card">
            <div class="listen-label">🎧 Listen carefully</div>
            <div style="font-family:'Playfair Display',serif; font-size:1.1rem; color:var(--muted); font-style:italic;">Which word do you hear?</div>
        </div>
        """, unsafe_allow_html=True)

        audio_file = speak_portuguese(current_q['portuguese'])
        st.audio(audio_file, format='audio/mp3')

        st.markdown("**Select the word you heard:**")
        for choice in choices:
            if st.button(choice, key=f"listen_{choice}", use_container_width=True, disabled=st.session_state.listen_answered):
                st.session_state.listen_answered = True
                st.session_state.listen_selected = choice
                st.session_state.listen_total += 1
                if choice == current_q['portuguese']:
                    st.session_state.listen_score += 1
                st.rerun()

        if st.session_state.listen_answered:
            correct_ans = current_q['portuguese']
            user_ans = st.session_state.listen_selected
            if user_ans == correct_ans:
                st.markdown('<div class="result-correct">✓ Correct! Your ear is sharp.</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="result-wrong">✗ You heard "{user_ans}", but it was "{correct_ans}"</div>', unsafe_allow_html=True)

            st.markdown(f"""
            <div class="example-sentence">
                <strong>{current_q['portuguese']}</strong> = {current_q['english']}<br>
                {current_q['example_pt']}
                <div class="translation">{current_q['example_en']}</div>
            </div>
            """, unsafe_allow_html=True)

            if st.button("Next Word →", type="primary", use_container_width=True):
                del st.session_state.listen_word
                del st.session_state.listen_choices
                del st.session_state.listen_answered
                del st.session_state.listen_selected
                st.rerun()


elif page == "Word Pairs":
    st.markdown('<div class="page-header"><h1>Word Pairs</h1><p>Match each Portuguese word to its English meaning</p></div>', unsafe_allow_html=True)

    if df.empty or len(df) < 4:
        st.warning("You need at least 4 words in your database.")
    else:
        PAIR_COUNT = 4

        if 'pairs_score' not in st.session_state:
            st.session_state.pairs_score = 0
        if 'pairs_rounds' not in st.session_state:
            st.session_state.pairs_rounds = 0

        if 'pairs_words' not in st.session_state:
            sample = df.sample(n=PAIR_COUNT)
            st.session_state.pairs_words = sample[['portuguese', 'english']].to_dict('records')
            pt_order = list(range(PAIR_COUNT))
            en_order = list(range(PAIR_COUNT))
            random.shuffle(pt_order)
            random.shuffle(en_order)
            st.session_state.pairs_pt_order = pt_order
            st.session_state.pairs_en_order = en_order
            st.session_state.pairs_selected_pt = None
            st.session_state.pairs_selected_en = None
            st.session_state.pairs_matched = []
            st.session_state.pairs_wrong_flash = []
            st.session_state.pairs_complete = False

        words = st.session_state.pairs_words
        pt_order = st.session_state.pairs_pt_order
        en_order = st.session_state.pairs_en_order
        matched = st.session_state.pairs_matched
        wrong_flash = st.session_state.pairs_wrong_flash

        st.markdown(f'<div class="score-box" style="margin-bottom:20px;"><div class="score-num">{len(matched)}/{PAIR_COUNT}</div><div class="score-label">Matched</div></div>', unsafe_allow_html=True)

        if st.session_state.pairs_complete:
            st.markdown('<div class="result-correct" style="text-align:center; font-size:1.2rem;">All pairs matched!</div>', unsafe_allow_html=True)
            st.session_state.pairs_rounds += 1
            st.session_state.pairs_score += PAIR_COUNT
            if st.button("New Round →", type="primary", use_container_width=True):
                for key in ['pairs_words', 'pairs_pt_order', 'pairs_en_order',
                            'pairs_selected_pt', 'pairs_selected_en',
                            'pairs_matched', 'pairs_wrong_flash', 'pairs_complete']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()
        else:
            col_pt, col_en = st.columns(2)

            with col_pt:
                st.markdown("**Portuguese**")
                for idx in pt_order:
                    w = words[idx]
                    is_matched = idx in matched
                    is_selected = st.session_state.pairs_selected_pt == idx
                    is_wrong = idx in wrong_flash

                    card_class = "pairs-card"
                    if is_matched:
                        card_class += " pairs-matched"
                    elif is_wrong:
                        card_class += " pairs-wrong"
                    elif is_selected:
                        card_class += " pairs-selected"

                    st.markdown(f'<div class="{card_class}">{w["portuguese"]}</div>', unsafe_allow_html=True)

                    if not is_matched:
                        if st.button(f"Select", key=f"pt_{idx}", use_container_width=True):
                            st.session_state.pairs_selected_pt = idx
                            st.session_state.pairs_wrong_flash = []
                            if st.session_state.pairs_selected_en is not None:
                                en_idx = st.session_state.pairs_selected_en
                                if idx == en_idx:
                                    st.session_state.pairs_matched.append(idx)
                                    st.session_state.pairs_selected_pt = None
                                    st.session_state.pairs_selected_en = None
                                    if len(st.session_state.pairs_matched) == PAIR_COUNT:
                                        st.session_state.pairs_complete = True
                                else:
                                    st.session_state.pairs_wrong_flash = [idx, en_idx]
                                    st.session_state.pairs_selected_pt = None
                                    st.session_state.pairs_selected_en = None
                            st.rerun()

            with col_en:
                st.markdown("**English**")
                for idx in en_order:
                    w = words[idx]
                    is_matched = idx in matched
                    is_selected = st.session_state.pairs_selected_en == idx
                    is_wrong = idx in wrong_flash

                    card_class = "pairs-card"
                    if is_matched:
                        card_class += " pairs-matched"
                    elif is_wrong:
                        card_class += " pairs-wrong"
                    elif is_selected:
                        card_class += " pairs-selected"

                    st.markdown(f'<div class="{card_class}">{w["english"]}</div>', unsafe_allow_html=True)

                    if not is_matched:
                        if st.button(f"Select", key=f"en_{idx}", use_container_width=True):
                            st.session_state.pairs_selected_en = idx
                            st.session_state.pairs_wrong_flash = []
                            if st.session_state.pairs_selected_pt is not None:
                                pt_idx = st.session_state.pairs_selected_pt
                                if idx == pt_idx:
                                    st.session_state.pairs_matched.append(idx)
                                    st.session_state.pairs_selected_pt = None
                                    st.session_state.pairs_selected_en = None
                                    if len(st.session_state.pairs_matched) == PAIR_COUNT:
                                        st.session_state.pairs_complete = True
                                else:
                                    st.session_state.pairs_wrong_flash = [pt_idx, idx]
                                    st.session_state.pairs_selected_pt = None
                                    st.session_state.pairs_selected_en = None
                            st.rerun()


elif page == "Speed Round":
    st.markdown('<div class="page-header"><h1>Speed Round</h1><p>10 words — type fast, build your streak</p></div>', unsafe_allow_html=True)

    if df.empty:
        st.warning("Your database is empty.")
    else:
        SPEED_TOTAL = min(10, len(df))

        if 'speed_active' not in st.session_state:
            st.session_state.speed_active = False
        if 'speed_done' not in st.session_state:
            st.session_state.speed_done = False

        if not st.session_state.speed_active and not st.session_state.speed_done:
            st.markdown("""
            <div class="flashcard" style="text-align:center;">
                <div style="font-family:'Playfair Display',serif; font-size:1.8rem; margin-bottom:12px;">Ready?</div>
                <div style="color:var(--muted);">You'll see 10 Portuguese words. Type the English translation as fast as you can. Partial matches count.</div>
            </div>
            """, unsafe_allow_html=True)
            if st.button("Start Speed Round", type="primary", use_container_width=True):
                sample = df.sample(n=SPEED_TOTAL)
                st.session_state.speed_words = sample.to_dict('records')
                st.session_state.speed_idx = 0
                st.session_state.speed_score = 0
                st.session_state.speed_streak = 0
                st.session_state.speed_best_streak = 0
                st.session_state.speed_counter = 0
                st.session_state.speed_answered = False
                st.session_state.speed_correct = False
                st.session_state.speed_active = True
                st.session_state.speed_done = False
                st.session_state.speed_start = time.time()
                st.rerun()

        elif st.session_state.speed_active:
            idx = st.session_state.speed_idx
            words = st.session_state.speed_words

            progress_pct = idx / SPEED_TOTAL
            st.markdown(f'<div class="progress-bar-container"><div class="progress-bar-fill" style="width:{progress_pct*100:.0f}%"></div></div>', unsafe_allow_html=True)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f'<div class="score-box"><div class="score-num">{idx}/{SPEED_TOTAL}</div><div class="score-label">Progress</div></div>', unsafe_allow_html=True)
            with col2:
                st.markdown(f'<div class="score-box"><div class="score-num">{st.session_state.speed_score}</div><div class="score-label">Correct</div></div>', unsafe_allow_html=True)
            with col3:
                st.markdown(f'<div class="score-box"><div class="score-num">{st.session_state.speed_streak}</div><div class="score-label">Streak</div></div>', unsafe_allow_html=True)

            current_word = words[idx]

            st.markdown(f"""
            <div class="quiz-word-display">
                <div class="pt-word">{current_word['portuguese']}</div>
                <div class="hint">{current_word['part_of_speech']}</div>
            </div>
            """, unsafe_allow_html=True)

            with st.form(key=f"speed_form_{st.session_state.speed_counter}"):
                user_input = st.text_input("English translation:", key=f"speed_input_{st.session_state.speed_counter}", placeholder="Type fast…")
                submit = st.form_submit_button("Submit", use_container_width=True)

            if submit:
                correct_ans = current_word['english'].lower()
                user_ans = user_input.strip().lower()
                is_correct = user_ans in correct_ans or correct_ans in user_ans

                st.session_state.speed_answered = True
                st.session_state.speed_correct = is_correct

                if is_correct:
                    st.session_state.speed_score += 1
                    st.session_state.speed_streak += 1
                    st.session_state.speed_best_streak = max(st.session_state.speed_best_streak, st.session_state.speed_streak)
                else:
                    st.session_state.speed_streak = 0

                st.session_state.speed_counter += 1

                if st.session_state.speed_answered:
                    if st.session_state.speed_correct:
                        st.markdown('<div class="result-correct">✓ Correct!</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="result-wrong">✗ Answer: <strong>{current_word["english"]}</strong></div>', unsafe_allow_html=True)

                st.session_state.speed_idx += 1
                if st.session_state.speed_idx >= SPEED_TOTAL:
                    st.session_state.speed_active = False
                    st.session_state.speed_done = True
                    st.session_state.speed_elapsed = time.time() - st.session_state.speed_start

                time.sleep(0.8)
                st.rerun()

        elif st.session_state.speed_done:
            elapsed = int(st.session_state.speed_elapsed)
            score = st.session_state.speed_score
            best_streak = st.session_state.speed_best_streak
            mins, secs = divmod(elapsed, 60)

            st.markdown(f"""
            <div class="flashcard" style="text-align:center; padding:48px 36px;">
                <div style="font-family:'Playfair Display',serif; font-size:1.2rem; color:var(--muted); margin-bottom:8px;">Round Complete</div>
                <div style="font-family:'Playfair Display',serif; font-size:3.5rem; color:var(--green);">{score}<span style="font-size:1.8rem; color:var(--muted);">/{SPEED_TOTAL}</span></div>
                <div style="color:var(--muted); margin: 8px 0 24px 0;">words correct</div>
            </div>
            """, unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f'<div class="score-box"><div class="score-num">{mins:02d}:{secs:02d}</div><div class="score-label">Time</div></div>', unsafe_allow_html=True)
            with col2:
                st.markdown(f'<div class="score-box"><div class="score-num">{best_streak}</div><div class="score-label">Best Streak</div></div>', unsafe_allow_html=True)

            if st.button("Play Again", type="primary", use_container_width=True):
                for key in ['speed_active', 'speed_done', 'speed_words', 'speed_idx',
                            'speed_score', 'speed_streak', 'speed_best_streak',
                            'speed_counter', 'speed_answered', 'speed_correct', 'speed_elapsed', 'speed_start']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.rerun()