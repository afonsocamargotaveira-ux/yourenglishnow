"""
YourEnglishNow — a Streamlit application for practising and assessing English.

Run with:
    streamlit run app.py

Requires: Python 3.9+ and streamlit >= 1.30
"""

import base64
import random
from collections import defaultdict

import streamlit as st

# ----------------------------------------------------------------------------
# Brand
# ----------------------------------------------------------------------------

NAVY = "#0B1F4B"
RED = "#D62839"

# Logo icon: a navy tile with a white speech bubble containing an "E";
# the red bottom bar of the "E" is the "Now" accent.
LOGO_ICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
<rect x="4" y="4" width="56" height="56" rx="14" fill="#0B1F4B"/>
<path fill="#FFFFFF" d="M22 14 H42 A8 8 0 0 1 50 22 V34 A8 8 0 0 1 42 42 H30 L20 51 V42 H22 A8 8 0 0 1 14 34 V22 A8 8 0 0 1 22 14 Z"/>
<rect x="23" y="21" width="4" height="14" fill="#0B1F4B"/>
<rect x="23" y="21" width="16" height="4" fill="#0B1F4B"/>
<rect x="23" y="26" width="12" height="4" fill="#0B1F4B"/>
<rect x="23" y="31" width="16" height="4" fill="#D62839"/>
</svg>"""

# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------

QUESTIONS_PER_QUIZ = 10

LEVELS = {
    "Beginner": {
        "cefr": "A1–A2",
        "description": "Everyday words, simple grammar and short texts.",
    },
    "Intermediate": {
        "cefr": "B1–B2",
        "description": "Common phrasal verbs, idioms and more complex grammar.",
    },
    "Advanced": {
        "cefr": "C1–C2",
        "description": "Nuanced vocabulary, advanced structures and subtle meaning.",
    },
}

# ----------------------------------------------------------------------------
# Question bank
# ----------------------------------------------------------------------------
# Each question is a dictionary with the keys:
#   id, level, category, question, options, correct_answer, explanation
# and optionally "passage" (for reading comprehension).
# For compactness the bank is defined with a helper where the FIRST option is
# the correct one; options are shuffled every time a quiz is generated, so the
# position of the right answer is random.

QUESTION_BANK = {"Beginner": [], "Intermediate": [], "Advanced": []}


def _add(level, category, question, correct, wrong, explanation, passage=None):
    """Add a question to the bank (validates the structure)."""
    options = [correct] + list(wrong)
    assert len(options) == 4 and len(set(options)) == 4, f"Bad options: {question}"
    item = {
        "id": f"{level[0]}{len(QUESTION_BANK[level]) + 1:02d}",
        "level": level,
        "category": category,
        "question": question,
        "options": options,
        "correct_answer": correct,
        "explanation": explanation,
    }
    if passage:
        item["passage"] = passage
    QUESTION_BANK[level].append(item)


# ---------------------------- BEGINNER (A1–A2) ------------------------------
B = "Beginner"
_add(B, "Grammar", "She ___ a student.", "is", ["are", "am", "be"],
     "With 'she' (third person singular) we use 'is'.")
_add(B, "Grammar", "I ___ breakfast every morning.", "have", ["has", "having", "am have"],
     "With 'I' we use the base form 'have' in the present simple.")
_add(B, "Grammar", "There ___ two books on the table.", "are", ["is", "am", "be"],
     "'Two books' is plural, so we say 'There are'.")
_add(B, "Grammar", "He ___ to school yesterday.", "went", ["goes", "go", "going"],
     "'Yesterday' signals the past, and the past of 'go' is 'went'.")
_add(B, "Sentence completion", "___ you like some tea?", "Would", ["Does", "Are", "Have"],
     "'Would you like...?' is the polite way to offer something.")
_add(B, "Vocabulary", "What is the opposite of 'hot'?", "cold", ["warm", "tall", "small"],
     "'Cold' is the opposite of 'hot'. 'Warm' is between the two.")
_add(B, "Vocabulary", "A place where you can borrow books is a ___.", "library",
     ["bakery", "pharmacy", "airport"],
     "A library is a place where people read and borrow books.")
_add(B, "Vocabulary", "My mother's sister is my ___.", "aunt", ["uncle", "cousin", "niece"],
     "Your mother's or father's sister is your aunt.")
_add(B, "Vocabulary", "We use ___ to cut paper.", "scissors", ["a spoon", "a pillow", "a mirror"],
     "Scissors are the tool we use for cutting paper.")
_add(B, "Reading comprehension", "How does Tom go to work?", "By bus",
     ["By car", "On foot", "By train"],
     "The text says: 'goes to work by bus'.",
     passage="Tom gets up at 7:00. He eats breakfast and goes to work by bus. "
             "He starts work at 9:00.")
_add(B, "Reading comprehension", "Where does Milo like to sleep?", "On the sofa",
     ["In the kitchen", "In a box", "On the bed"],
     "The text says Milo 'likes to sleep on the sofa'.",
     passage="Anna has a small cat called Milo. Milo likes to sleep on the sofa "
             "and drink milk.")
_add(B, "Phrasal verbs", "Please ___ your shoes before you enter the house.", "take off",
     ["take on", "take up", "take in"],
     "'Take off' means to remove clothes or shoes.")
_add(B, "Phrasal verbs", "It's dark in here. Please turn ___ the light.", "on",
     ["in", "by", "of"],
     "'Turn on' means to make a light or machine start working.")
_add(B, "Sentence completion", "I'm thirsty. I want a glass of ___.", "water",
     ["bread", "rice", "cheese"],
     "We drink water; we eat bread, rice and cheese.")
_add(B, "Sentence completion", "Good morning! How ___ you?", "are", ["is", "am", "be"],
     "With 'you' we use 'are': 'How are you?'")
_add(B, "Correct word usage", "I have ___ apple in my bag.", "an", ["a", "two", "many"],
     "We use 'an' before a vowel sound, and 'apple' starts with a vowel sound. "
     "'Two' and 'many' need a plural noun.")
_add(B, "Grammar", "She is ___ than her brother.", "taller", ["tall", "tallest", "more tall"],
     "For short adjectives we add -er to compare two people: 'taller than'.")
_add(B, "Correct word usage", "My birthday is ___ May.", "in", ["on", "at", "by"],
     "We use 'in' with months: 'in May'. We use 'on' with specific dates.")
_add(B, "Correct word usage", "This is ___ book.", "my", ["me", "I", "mine"],
     "'My' is a possessive adjective and goes before a noun.")
_add(B, "Idiomatic expressions", "What does 'Break a leg!' mean?", "Good luck!",
     ["Be careful!", "Go home!", "I'm sorry."],
     "'Break a leg' is a friendly way to wish someone good luck, especially before a performance.")

# -------------------------- INTERMEDIATE (B1–B2) ----------------------------
I = "Intermediate"
_add(I, "Grammar", "If I ___ more time, I would learn Spanish.", "had",
     ["have", "will have", "would have"],
     "This is the second conditional: 'if' + past simple, 'would' + base verb.")
_add(I, "Grammar", "She has lived here ___ 2015.", "since", ["for", "from", "during"],
     "We use 'since' with a point in time (2015) and 'for' with a period of time.")
_add(I, "Grammar", "I'm not used to ___ up so early.", "getting",
     ["get", "got", "be getting"],
     "'Be used to' is followed by a gerund (-ing form).")
_add(I, "Grammar", "The report ___ by the manager before the meeting started.",
     "had been checked", ["has checked", "was check", "had checked"],
     "The past perfect passive ('had been' + past participle) shows an action completed "
     "before another past action, and the report receives the action.")
_add(I, "Grammar", "He suggested ___ a taxi because it was late.", "taking",
     ["to take", "take", "took"],
     "'Suggest' is followed by a gerund: 'suggested taking'.")
_add(I, "Vocabulary", "Prices have risen ___ over the past year.", "significantly",
     ["significant", "signify", "significance"],
     "We need an adverb to modify the verb 'risen': 'significantly'.")
_add(I, "Vocabulary", "Which word is closest in meaning to 'reluctant'?", "unwilling",
     ["eager", "careless", "generous"],
     "'Reluctant' means not wanting to do something, so 'unwilling' is the closest.")
_add(I, "Vocabulary", "The company decided to ___ its operations abroad.", "expand",
     ["expend", "expel", "expose"],
     "'Expand' means to become or make larger. 'Expend' means to spend or use up.")
_add(I, "Phrasal verbs", "We ran ___ milk, so I went to the shop.", "out of",
     ["away from", "into", "over"],
     "'Run out of' means to have no more of something.")
_add(I, "Phrasal verbs", "She finally managed to ___ smoking.", "give up",
     ["give in", "give out", "give away"],
     "'Give up' means to stop doing a habit.")
_add(I, "Phrasal verbs", "I can't ___ with his rude behaviour any longer.", "put up",
     ["put on", "put off", "put out"],
     "'Put up with' means to tolerate something unpleasant.")
_add(I, "Idiomatic expressions", "'Once in a blue moon' means ___.", "very rarely",
     ["every night", "at midnight", "very often"],
     "The idiom describes something that happens extremely rarely.")
_add(I, "Idiomatic expressions", "If you are 'under the weather', you are ___.",
     "feeling slightly ill", ["very happy", "standing outside", "late for work"],
     "'Under the weather' is an idiom meaning slightly unwell.")
_add(I, "Reading comprehension", "Which disadvantage of remote work is mentioned?",
     "Employees can feel isolated",
     ["Longer commutes", "Lower salaries", "Less flexible hours"],
     "The text says some employees 'feel isolated' and struggle to separate work from home life.",
     passage="Remote work has become popular because it saves commuting time. "
             "However, some employees say they feel isolated and find it harder to "
             "separate work from personal life.")
_add(I, "Reading comprehension", "What almost happened to the museum in 2008?",
     "It nearly closed",
     ["It opened to visitors", "It moved to a new city", "It doubled its visitors"],
     "The text says it 'was nearly closed in 2008 due to funding problems'.",
     passage="The museum, which opened in 1990, attracts over a million visitors a "
             "year, though it was nearly closed in 2008 due to funding problems.")
_add(I, "Correct word usage", "The doctor gave me some ___ about healthy eating.", "advice",
     ["advices", "advise", "an advice"],
     "'Advice' is an uncountable noun, so it has no plural and no 'a/an'. "
     "'Advise' is the verb.")
_add(I, "Correct word usage", "I'm looking forward ___ you next week.", "to seeing",
     ["to see", "for seeing", "seeing"],
     "'Look forward to' is followed by a gerund because 'to' is a preposition here.")
_add(I, "Grammar", "Neither of the students ___ the answer.", "knew",
     ["know", "were knowing", "have know"],
     "The sentence is in the simple past, and 'neither of' takes a singular verb form.")
_add(I, "Grammar", "___ being tired, she kept working.", "Despite",
     ["Although", "However", "Because"],
     "'Despite' is followed by a noun or gerund. 'Although' needs a full clause.")
_add(I, "Grammar", "He is ___ person I have ever met.", "the kindest",
     ["kinder", "most kind", "kindest"],
     "The superlative of a short adjective is 'the kindest'.")

# ---------------------------- ADVANCED (C1–C2) ------------------------------
A = "Advanced"
_add(A, "Grammar", "Had I known about the delay, I ___ earlier.", "would have left",
     ["will leave", "would leave", "had left"],
     "This is an inverted third conditional (= 'If I had known...'), which takes "
     "'would have' + past participle.")
_add(A, "Grammar", "Not only ___ late, but he also forgot the documents.", "did he arrive",
     ["he arrived", "he did arrive", "arrived he"],
     "After a negative adverbial like 'not only' at the start of a sentence, "
     "we invert the subject and auxiliary.")
_add(A, "Grammar", "The committee insisted that he ___ the proposal.", "reconsider",
     ["reconsiders", "reconsidered", "would reconsiders"],
     "After 'insist that', the subjunctive uses the base form of the verb.")
_add(A, "Grammar", "By this time next year, she ___ her doctorate.", "will have completed",
     ["will complete", "has completed", "would complete"],
     "The future perfect describes an action finished before a future point in time.")
_add(A, "Grammar", "It's high time we ___ a decision.", "made",
     ["make", "will make", "have made"],
     "'It's high time' is followed by the past simple, even though it refers to now.")
_add(A, "Vocabulary", "The word 'ubiquitous' means ___.", "found everywhere",
     ["extremely rare", "easily broken", "deeply respected"],
     "'Ubiquitous' describes something that seems to be present everywhere.")
_add(A, "Vocabulary", "Her argument was so ___ that nobody could refute it.", "cogent",
     ["contrived", "complacent", "candid"],
     "'Cogent' means clear, logical and convincing.")
_add(A, "Vocabulary", "The politician's ___ remarks offended many voters.", "disparaging",
     ["disparate", "desperate", "dispassionate"],
     "'Disparaging' means expressing a low opinion of someone. 'Disparate' means "
     "fundamentally different.")
_add(A, "Vocabulary", "An 'ephemeral' pleasure is one that ___.", "lasts a very short time",
     ["lasts a lifetime", "is very expensive", "is shared with others"],
     "'Ephemeral' means lasting for a very short time.")
_add(A, "Correct word usage", "The new policy will ___ significant changes in how we operate.",
     "entail", ["entice", "entreat", "enthrall"],
     "'Entail' means to involve something as a necessary result.")
_add(A, "Phrasal verbs", "The negotiations ___ after both sides refused to compromise.",
     "broke down", ["broke in", "broke out", "broke through"],
     "'Break down' means to fail or collapse.")
_add(A, "Phrasal verbs", "I'd like to ___ the matter further before I commit.", "look into",
     ["look after", "look up to", "look out"],
     "'Look into' means to investigate or examine.")
_add(A, "Phrasal verbs", "She decided to ___ the offer, as it seemed too good to be true.",
     "turn down", ["turn up", "turn over", "turn in"],
     "'Turn down' means to refuse or reject.")
_add(A, "Idiomatic expressions", "To 'bite the bullet' means to ___.",
     "face something unpleasant with courage",
     ["eat very quickly", "speak without thinking", "give up completely"],
     "The idiom means to accept a difficult situation and deal with it bravely.")
_add(A, "Idiomatic expressions", "If you 'burn the midnight oil', you ___.",
     "work late into the night", ["waste resources", "lose your temper", "sleep very deeply"],
     "The idiom refers to working or studying very late at night.")
_add(A, "Reading comprehension", "What do critics of nuclear energy argue?",
     "Waste storage is unresolved and costs often overrun",
     ["It produces high carbon emissions", "It is too cheap to build",
      "It is unpopular with engineers"],
     "The passage says critics point to unresolved long-term waste storage and "
     "construction costs that exceed initial estimates.",
     passage="While proponents of nuclear energy emphasise its low carbon emissions, "
             "critics counter that the long-term storage of radioactive waste remains "
             "unresolved, and that construction costs frequently exceed initial estimates.")
_add(A, "Reading comprehension", "What does 'ostensibly neutral' suggest about the author's tone?",
     "It appears neutral but may not truly be",
     ["It is completely unbiased", "It is openly hostile", "It is deliberately humorous"],
     "'Ostensibly' means 'apparently'. The next clause shows the neutrality is "
     "only on the surface.",
     passage="The author's tone throughout the essay is ostensibly neutral; yet the "
             "careful selection of anecdotes subtly favours one side.")
_add(A, "Correct word usage", "The two proposals are fundamentally different; they have little in ___.",
     "common", ["mutual", "same", "share"],
     "'Have something in common' is a fixed expression.")
_add(A, "Correct word usage", "She was reprimanded for her ___ attitude towards safety regulations.",
     "cavalier", ["cordial", "copious", "covert"],
     "'Cavalier' means showing a lack of proper concern about something important.")
_add(A, "Grammar", "Hardly ___ the building when the alarm went off.", "had she entered",
     ["she had entered", "she entered", "did she enter"],
     "'Hardly... when' is used with the past perfect, and 'hardly' at the start "
     "triggers subject–auxiliary inversion.")


# ----------------------------------------------------------------------------
# Quiz logic
# ----------------------------------------------------------------------------

def classify(percentage):
    """Return (label, message) for a percentage score."""
    if percentage >= 90:
        return "Excellent", "Outstanding! You have a very strong command of this level."
    if percentage >= 70:
        return "Good", "Well done! You are comfortable with most of the material."
    if percentage >= 50:
        return "Fair", "A decent start. Review the explanations below and try again."
    return "Needs practice", "Keep going! Review the explanations and take another quiz."


def build_quiz(level):
    """Pick random questions for a level, preferring ones not seen recently."""
    pool = QUESTION_BANK[level]
    seen = st.session_state.seen[level]
    unseen = [q for q in pool if q["id"] not in seen]

    if len(unseen) >= QUESTIONS_PER_QUIZ:
        picked = random.sample(unseen, QUESTIONS_PER_QUIZ)
        seen.update(q["id"] for q in picked)
    else:
        # Use whatever is left, top up from the rest, then restart the cycle.
        others = [q for q in pool if q["id"] in seen]
        picked = unseen + random.sample(others, QUESTIONS_PER_QUIZ - len(unseen))
        st.session_state.seen[level] = {q["id"] for q in picked}

    quiz = []
    for q in picked:
        copy = dict(q)
        copy["options"] = random.sample(q["options"], k=len(q["options"]))  # shuffled
        quiz.append(copy)
    random.shuffle(quiz)
    return quiz


def init_state():
    defaults = {
        "stage": "home",       # home | quiz | results
        "level": "Beginner",
        "quiz": [],
        "answers": {},         # question index -> chosen option text
        "current": 0,
        "quiz_id": 0,
        "result": None,
        "warning": None,
        "seen": defaultdict(set),
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


# ---- Callbacks (run before the next rerun, so state is always consistent) ----

def start_quiz(level):
    st.session_state.level = level
    st.session_state.quiz = build_quiz(level)
    st.session_state.answers = {}
    st.session_state.current = 0
    st.session_state.result = None
    st.session_state.warning = None
    st.session_state.quiz_id += 1
    st.session_state.stage = "quiz"


def start_from_home():
    start_quiz(st.session_state.home_level)


def go_home():
    st.session_state.stage = "home"
    st.session_state.warning = None


def save_answer(index):
    """Store the answer for a question when the radio selection changes."""
    value = st.session_state.get(f"radio_{st.session_state.quiz_id}_{index}")
    if value is not None:
        st.session_state.answers[index] = value
        st.session_state.warning = None


def go_to(index):
    st.session_state.current = index
    st.session_state.warning = None


def submit_quiz():
    """Validate and score the quiz exactly once."""
    if st.session_state.result is not None:  # already scored (e.g. double click)
        st.session_state.stage = "results"
        return

    quiz = st.session_state.quiz
    answers = st.session_state.answers
    unanswered = [i + 1 for i in range(len(quiz)) if i not in answers]
    if unanswered:
        st.session_state.warning = (
            "Please answer all questions before submitting. "
            f"Unanswered: {', '.join(map(str, unanswered))}."
        )
        return

    details = []
    category_totals = defaultdict(lambda: [0, 0])  # category -> [correct, total]
    for i, q in enumerate(quiz):
        chosen = answers[i]
        is_correct = chosen == q["correct_answer"]
        category_totals[q["category"]][1] += 1
        category_totals[q["category"]][0] += int(is_correct)
        details.append({**q, "chosen": chosen, "is_correct": is_correct})

    score = sum(d["is_correct"] for d in details)
    percentage = round(score / len(quiz) * 100)
    label, message = classify(percentage)
    st.session_state.result = {
        "level": st.session_state.level,
        "score": score,
        "total": len(quiz),
        "percentage": percentage,
        "label": label,
        "message": message,
        "details": details,
        "categories": dict(category_totals),
    }
    st.session_state.warning = None
    st.session_state.stage = "results"


# ----------------------------------------------------------------------------
# UI helpers
# ----------------------------------------------------------------------------

def md_safe(text):
    """Escape underscores so blanks ('___') are shown literally in Markdown."""
    return text.replace("_", "\\_")


def inject_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

        .stApp, .stApp h1, .stApp h2, .stApp h3, .stApp p, .stApp li, .stApp label,
        .stApp button, .stApp input, .stApp textarea,
        [data-testid="stMarkdownContainer"], [data-testid="stMetricValue"],
        [data-testid="stMetricLabel"], [data-testid="stCaptionContainer"],
        .yen-word {
            font-family: 'Poppins', 'Segoe UI', Helvetica, Arial, sans-serif;
        }
        .stApp {background: #FFFFFF; color: #0B1F4B;}
        #MainMenu, footer {visibility: hidden;}
        .block-container {max-width: 760px; padding-top: 4.5rem; padding-bottom: 3rem;}

        h1, h2, h3 {color: #0B1F4B; font-weight: 700; letter-spacing: -0.3px;}
        [data-testid="stCaptionContainer"] {color: #5B6784;}
        hr {border-color: #E3E7F0;}

        /* Brand header */
        .yen-brand {display: flex; align-items: center; gap: 12px; padding-bottom: 14px;
                    border-bottom: 3px solid #0B1F4B; margin-bottom: 1.5rem;}
        .yen-brand img {height: 46px; width: 46px;}
        .yen-word {font-size: 1.7rem; line-height: 1; white-space: nowrap; letter-spacing: -0.5px; color: #0B1F4B;}
        .yen-word .light {font-weight: 400;}
        .yen-word .bold {font-weight: 700;}
        .yen-word .now {font-weight: 700; color: #D62839;}

        /* Hero */
        .yen-hero {background: #0B1F4B; color: #FFFFFF; border-radius: 16px;
                   padding: 1.6rem 1.6rem 1.4rem; margin-bottom: 1.5rem;
                   border-left: 8px solid #D62839;}
        .yen-hero h2 {color: #FFFFFF; margin: 0 0 .5rem; font-size: 1.6rem;}
        .yen-hero p {color: #DCE2F2; margin: 0; font-size: 1rem; line-height: 1.55;}

        /* Buttons */
        div.stButton > button {width: 100%; border-radius: 10px; padding: 0.6rem 1rem;
                               font-weight: 600; transition: all .15s ease;}
        button[kind="primary"], [data-testid="stBaseButton-primary"] {
            background: #D62839; border: 1.5px solid #D62839; color: #FFFFFF;}
        button[kind="primary"]:hover, [data-testid="stBaseButton-primary"]:hover {
            background: #B71F2E; border-color: #B71F2E; color: #FFFFFF;}
        button[kind="secondary"], [data-testid="stBaseButton-secondary"] {
            background: #FFFFFF; border: 1.5px solid #0B1F4B; color: #0B1F4B;}
        button[kind="secondary"]:hover, [data-testid="stBaseButton-secondary"]:hover {
            background: #0B1F4B; color: #FFFFFF; border-color: #0B1F4B;}

        /* Answer options as cards */
        div[role="radiogroup"] {gap: .5rem;}
        div[role="radiogroup"] > label {
            border: 1.5px solid #D7DCE8; border-radius: 12px; padding: .7rem .9rem;
            background: #FFFFFF; width: 100%; transition: border-color .15s, background .15s;}
        div[role="radiogroup"] > label:hover {border-color: #0B1F4B;}
        div[role="radiogroup"] > label:has(input:checked) {
            border-color: #D62839; background: #FDF1F2;}

        /* Cards, metrics, progress */
        [data-testid="stVerticalBlockBorderWrapper"] {border-radius: 14px; border-color: #E3E7F0;}
        [data-testid="stMetricValue"] {color: #0B1F4B; font-weight: 700;}
        [data-testid="stMetricLabel"] {color: #5B6784;}
        [data-testid="stProgress"] > div > div > div > div {background-color: #D62839;}

        @media (max-width: 640px) {
            .block-container {padding-left: 1rem; padding-right: 1rem;}
            .yen-word {font-size: 1.35rem;}
            .yen-brand img {height: 38px; width: 38px;}
            .yen-hero h2 {font-size: 1.3rem;}
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_logo():
    """Brand header: icon + YourEnglishNow wordmark."""
    icon = base64.b64encode(LOGO_ICON_SVG.encode()).decode()
    st.markdown(
        f"""
        <div class="yen-brand">
            <img src="data:image/svg+xml;base64,{icon}" alt="YourEnglishNow logo">
            <span class="yen-word"><span class="light">Your</span><span class="bold">English</span><span class="now">Now</span></span>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ----------------------------------------------------------------------------
# Screens
# ----------------------------------------------------------------------------

def render_home():
    st.markdown(
        """
        <div class="yen-hero">
            <h2>Find your level. Improve it today.</h2>
            <p>Take a short 10-question quiz covering grammar, vocabulary, reading,
            idioms, phrasal verbs and word usage. Every quiz is drawn at random from
            a larger question bank, so each attempt is different.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("Choose your level")
    levels = list(LEVELS)
    st.radio(
        "Level",
        levels,
        index=levels.index(st.session_state.level),
        key="home_level",
        format_func=lambda name: f"{name}  ·  CEFR {LEVELS[name]['cefr']}",
        label_visibility="collapsed",
    )
    st.caption(LEVELS[st.session_state.home_level]["description"])

    st.button("Start quiz", type="primary", on_click=start_from_home)


def render_quiz():
    quiz = st.session_state.quiz
    total = len(quiz)
    current = st.session_state.current
    answers = st.session_state.answers
    q = quiz[current]
    level = st.session_state.level

    st.caption(f"{level} · CEFR {LEVELS[level]['cefr']}")
    st.progress(len(answers) / total, text=f"{len(answers)} of {total} answered")
    st.subheader(f"Question {current + 1} of {total}")
    st.caption(q["category"])

    if q.get("passage"):
        st.info(q["passage"])

    st.markdown(f"**{md_safe(q['question'])}**")

    radio_key = f"radio_{st.session_state.quiz_id}_{current}"
    saved = answers.get(current)
    st.radio(
        "Choose one answer",
        q["options"],
        index=q["options"].index(saved) if saved in q["options"] else None,
        key=radio_key,
        on_change=save_answer,
        args=(current,),
        label_visibility="collapsed",
    )

    if st.session_state.warning:
        st.warning(st.session_state.warning)

    left, middle, right = st.columns(3)
    with left:
        st.button("Previous", disabled=current == 0, on_click=go_to,
                  args=(current - 1,), key="btn_prev")
    with middle:
        st.button("Quit", on_click=go_home, key="btn_quit")
    with right:
        if current < total - 1:
            st.button("Next", type="primary", on_click=go_to,
                      args=(current + 1,), key="btn_next")
        else:
            st.button("Submit", type="primary", on_click=submit_quiz, key="btn_submit")

    if current == total - 1 and len(answers) < total:
        missing = [str(i + 1) for i in range(total) if i not in answers]
        st.caption(f"Still unanswered: {', '.join(missing)}")


def render_results():
    result = st.session_state.result
    if result is None:  # safety net
        go_home()
        st.rerun()
        return

    st.subheader("Your results")
    st.caption(f"{result['level']} level · CEFR {LEVELS[result['level']]['cefr']}")

    col1, col2, col3 = st.columns(3)
    col1.metric("Correct answers", f"{result['score']} / {result['total']}")
    col2.metric("Score", f"{result['percentage']}%")
    col3.metric("Performance", result["label"])
    st.progress(result["percentage"] / 100)
    st.write(result["message"])

    with st.expander("Performance by category"):
        for category, (correct, count) in sorted(result["categories"].items()):
            st.write(f"**{category}**: {correct} / {count}")

    left, right = st.columns(2)
    with left:
        st.button("New quiz (same level)", type="primary",
                  on_click=start_quiz, args=(result["level"],), key="btn_again")
    with right:
        st.button("Choose another level", on_click=go_home, key="btn_home")

    st.divider()
    st.subheader("Review your answers")
    for number, d in enumerate(result["details"], start=1):
        with st.container(border=True):
            status = "Correct" if d["is_correct"] else "Incorrect"
            st.markdown(f"**Question {number}** · {status} · _{d['category']}_")
            if d.get("passage"):
                st.info(d["passage"])
            st.markdown(f"**{md_safe(d['question'])}**")
            if d["is_correct"]:
                st.success(f"Your answer: {d['chosen']}")
            else:
                st.error(f"Your answer: {d['chosen']}")
                st.success(f"Correct answer: {d['correct_answer']}")
            st.markdown(f"**Why:** {d['explanation']}")


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------

def main():
    st.set_page_config(page_title="YourEnglishNow", page_icon="💬", layout="centered")
    init_state()
    inject_css()
    render_logo()

    stage = st.session_state.stage
    if stage == "quiz":
        render_quiz()
    elif stage == "results":
        render_results()
    else:
        render_home()


if __name__ == "__main__":
    main()
