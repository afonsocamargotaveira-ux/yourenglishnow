"""
LinguaNow — a Streamlit application for practising and assessing languages
(English, Spanish, French, German and Portuguese).

Run with:
    streamlit run app.py

Requires: Python 3.9+ and streamlit >= 1.30
"""

import base64
import html
import random
from collections import defaultdict

import streamlit as st

# ----------------------------------------------------------------------------
# Brand
# ----------------------------------------------------------------------------

NAVY = "#0B1F4B"
RED = "#D62839"

# LinguaNow logo: two overlapping speech bubbles (a conversation between languages).
# The navy bubble carries an "A", the red bubble carries three "typing" dots.
LOGO_ICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
<path fill="#0B1F4B" d="M13 6 H31 A9 9 0 0 1 40 15 V25 A9 9 0 0 1 31 34 H19 L10 42 V34 H13 A9 9 0 0 1 4 25 V15 A9 9 0 0 1 13 6 Z"/>
<path fill="none" stroke="#FFFFFF" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" d="M11 21 L18 10 L25 21 M14 17 H22"/>
<path fill="#D62839" stroke="#FFFFFF" stroke-width="3" stroke-linejoin="round" d="M33 24 H51 A9 9 0 0 1 60 33 V43 A9 9 0 0 1 51 52 L54 60 L42 52 H33 A9 9 0 0 1 24 43 V33 A9 9 0 0 1 33 24 Z"/>
<circle cx="35" cy="38" r="2.5" fill="#FFFFFF"/><circle cx="42" cy="38" r="2.5" fill="#FFFFFF"/><circle cx="49" cy="38" r="2.5" fill="#FFFFFF"/>
</svg>"""

# ----------------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------------

QUESTIONS_PER_QUIZ = 10

LANGUAGES = {
    "English": {"code": "E", "native": "English"},
    "Spanish": {"code": "S", "native": "Español"},
    "French": {"code": "F", "native": "Français"},
    "German": {"code": "G", "native": "Deutsch"},
    "Portuguese": {"code": "P", "native": "Português"},
}

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

QUESTION_BANK = {lang: {level: [] for level in LEVELS} for lang in LANGUAGES}


def _add(language, level, category, question, correct, wrong, explanation, passage=None):
    """Add a question to the bank (validates the structure)."""
    options = [correct] + list(wrong)
    assert len(options) == 4 and len(set(options)) == 4, f"Bad options: {question}"
    bank = QUESTION_BANK[language][level]
    item = {
        "id": f"{LANGUAGES[language]['code']}{level[0]}{len(bank) + 1:02d}",
        "language": language,
        "level": level,
        "category": category,
        "question": question,
        "options": options,
        "correct_answer": correct,
        "explanation": explanation,
    }
    if passage:
        item["passage"] = passage
    bank.append(item)


def _bulk(language, level, rows):
    """Add many questions: (category, question, correct, [3 wrong], explanation[, passage])."""
    for category, question, correct, wrong, explanation, *rest in rows:
        _add(language, level, category, question, correct, wrong, explanation,
             rest[0] if rest else None)


# ============================================================================
# ENGLISH
# ============================================================================
# ---------------------------- BEGINNER (A1–A2) ------------------------------
B = "Beginner"
_add("English", B, "Grammar", "She ___ a student.", "is", ["are", "am", "be"],
     "With 'she' (third person singular) we use 'is'.")
_add("English", B, "Grammar", "I ___ breakfast every morning.", "have", ["has", "having", "am have"],
     "With 'I' we use the base form 'have' in the present simple.")
_add("English", B, "Grammar", "There ___ two books on the table.", "are", ["is", "am", "be"],
     "'Two books' is plural, so we say 'There are'.")
_add("English", B, "Grammar", "He ___ to school yesterday.", "went", ["goes", "go", "going"],
     "'Yesterday' signals the past, and the past of 'go' is 'went'.")
_add("English", B, "Sentence completion", "___ you like some tea?", "Would", ["Does", "Are", "Have"],
     "'Would you like...?' is the polite way to offer something.")
_add("English", B, "Vocabulary", "What is the opposite of 'hot'?", "cold", ["warm", "tall", "small"],
     "'Cold' is the opposite of 'hot'. 'Warm' is between the two.")
_add("English", B, "Vocabulary", "A place where you can borrow books is a ___.", "library",
     ["bakery", "pharmacy", "airport"],
     "A library is a place where people read and borrow books.")
_add("English", B, "Vocabulary", "My mother's sister is my ___.", "aunt", ["uncle", "cousin", "niece"],
     "Your mother's or father's sister is your aunt.")
_add("English", B, "Vocabulary", "We use ___ to cut paper.", "scissors", ["a spoon", "a pillow", "a mirror"],
     "Scissors are the tool we use for cutting paper.")
_add("English", B, "Reading comprehension", "How does Tom go to work?", "By bus",
     ["By car", "On foot", "By train"],
     "The text says: 'goes to work by bus'.",
     passage="Tom gets up at 7:00. He eats breakfast and goes to work by bus. "
             "He starts work at 9:00.")
_add("English", B, "Reading comprehension", "Where does Milo like to sleep?", "On the sofa",
     ["In the kitchen", "In a box", "On the bed"],
     "The text says Milo 'likes to sleep on the sofa'.",
     passage="Anna has a small cat called Milo. Milo likes to sleep on the sofa "
             "and drink milk.")
_add("English", B, "Phrasal verbs", "Please ___ your shoes before you enter the house.", "take off",
     ["take on", "take up", "take in"],
     "'Take off' means to remove clothes or shoes.")
_add("English", B, "Phrasal verbs", "It's dark in here. Please turn ___ the light.", "on",
     ["in", "by", "of"],
     "'Turn on' means to make a light or machine start working.")
_add("English", B, "Sentence completion", "I'm thirsty. I want a glass of ___.", "water",
     ["bread", "rice", "cheese"],
     "We drink water; we eat bread, rice and cheese.")
_add("English", B, "Sentence completion", "Good morning! How ___ you?", "are", ["is", "am", "be"],
     "With 'you' we use 'are': 'How are you?'")
_add("English", B, "Correct word usage", "I have ___ apple in my bag.", "an", ["a", "two", "many"],
     "We use 'an' before a vowel sound, and 'apple' starts with a vowel sound. "
     "'Two' and 'many' need a plural noun.")
_add("English", B, "Grammar", "She is ___ than her brother.", "taller", ["tall", "tallest", "more tall"],
     "For short adjectives we add -er to compare two people: 'taller than'.")
_add("English", B, "Correct word usage", "My birthday is ___ May.", "in", ["on", "at", "by"],
     "We use 'in' with months: 'in May'. We use 'on' with specific dates.")
_add("English", B, "Correct word usage", "This is ___ book.", "my", ["me", "I", "mine"],
     "'My' is a possessive adjective and goes before a noun.")
_add("English", B, "Idiomatic expressions", "What does 'Break a leg!' mean?", "Good luck!",
     ["Be careful!", "Go home!", "I'm sorry."],
     "'Break a leg' is a friendly way to wish someone good luck, especially before a performance.")

# -------------------------- INTERMEDIATE (B1–B2) ----------------------------
I = "Intermediate"
_add("English", I, "Grammar", "If I ___ more time, I would learn Spanish.", "had",
     ["have", "will have", "would have"],
     "This is the second conditional: 'if' + past simple, 'would' + base verb.")
_add("English", I, "Grammar", "She has lived here ___ 2015.", "since", ["for", "from", "during"],
     "We use 'since' with a point in time (2015) and 'for' with a period of time.")
_add("English", I, "Grammar", "I'm not used to ___ up so early.", "getting",
     ["get", "got", "be getting"],
     "'Be used to' is followed by a gerund (-ing form).")
_add("English", I, "Grammar", "The report ___ by the manager before the meeting started.",
     "had been checked", ["has checked", "was check", "had checked"],
     "The past perfect passive ('had been' + past participle) shows an action completed "
     "before another past action, and the report receives the action.")
_add("English", I, "Grammar", "He suggested ___ a taxi because it was late.", "taking",
     ["to take", "take", "took"],
     "'Suggest' is followed by a gerund: 'suggested taking'.")
_add("English", I, "Vocabulary", "Prices have risen ___ over the past year.", "significantly",
     ["significant", "signify", "significance"],
     "We need an adverb to modify the verb 'risen': 'significantly'.")
_add("English", I, "Vocabulary", "Which word is closest in meaning to 'reluctant'?", "unwilling",
     ["eager", "careless", "generous"],
     "'Reluctant' means not wanting to do something, so 'unwilling' is the closest.")
_add("English", I, "Vocabulary", "The company decided to ___ its operations abroad.", "expand",
     ["expend", "expel", "expose"],
     "'Expand' means to become or make larger. 'Expend' means to spend or use up.")
_add("English", I, "Phrasal verbs", "We ran ___ milk, so I went to the shop.", "out of",
     ["away from", "into", "over"],
     "'Run out of' means to have no more of something.")
_add("English", I, "Phrasal verbs", "She finally managed to ___ smoking.", "give up",
     ["give in", "give out", "give away"],
     "'Give up' means to stop doing a habit.")
_add("English", I, "Phrasal verbs", "I can't ___ with his rude behaviour any longer.", "put up",
     ["put on", "put off", "put out"],
     "'Put up with' means to tolerate something unpleasant.")
_add("English", I, "Idiomatic expressions", "'Once in a blue moon' means ___.", "very rarely",
     ["every night", "at midnight", "very often"],
     "The idiom describes something that happens extremely rarely.")
_add("English", I, "Idiomatic expressions", "If you are 'under the weather', you are ___.",
     "feeling slightly ill", ["very happy", "standing outside", "late for work"],
     "'Under the weather' is an idiom meaning slightly unwell.")
_add("English", I, "Reading comprehension", "Which disadvantage of remote work is mentioned?",
     "Employees can feel isolated",
     ["Longer commutes", "Lower salaries", "Less flexible hours"],
     "The text says some employees 'feel isolated' and struggle to separate work from home life.",
     passage="Remote work has become popular because it saves commuting time. "
             "However, some employees say they feel isolated and find it harder to "
             "separate work from personal life.")
_add("English", I, "Reading comprehension", "What almost happened to the museum in 2008?",
     "It nearly closed",
     ["It opened to visitors", "It moved to a new city", "It doubled its visitors"],
     "The text says it 'was nearly closed in 2008 due to funding problems'.",
     passage="The museum, which opened in 1990, attracts over a million visitors a "
             "year, though it was nearly closed in 2008 due to funding problems.")
_add("English", I, "Correct word usage", "The doctor gave me some ___ about healthy eating.", "advice",
     ["advices", "advise", "an advice"],
     "'Advice' is an uncountable noun, so it has no plural and no 'a/an'. "
     "'Advise' is the verb.")
_add("English", I, "Correct word usage", "I'm looking forward ___ you next week.", "to seeing",
     ["to see", "for seeing", "seeing"],
     "'Look forward to' is followed by a gerund because 'to' is a preposition here.")
_add("English", I, "Grammar", "Neither of the students ___ the answer.", "knew",
     ["know", "were knowing", "have know"],
     "The sentence is in the simple past, and 'neither of' takes a singular verb form.")
_add("English", I, "Grammar", "___ being tired, she kept working.", "Despite",
     ["Although", "However", "Because"],
     "'Despite' is followed by a noun or gerund. 'Although' needs a full clause.")
_add("English", I, "Grammar", "He is ___ person I have ever met.", "the kindest",
     ["kinder", "most kind", "kindest"],
     "The superlative of a short adjective is 'the kindest'.")

# ---------------------------- ADVANCED (C1–C2) ------------------------------
A = "Advanced"
_add("English", A, "Grammar", "Had I known about the delay, I ___ earlier.", "would have left",
     ["will leave", "would leave", "had left"],
     "This is an inverted third conditional (= 'If I had known...'), which takes "
     "'would have' + past participle.")
_add("English", A, "Grammar", "Not only ___ late, but he also forgot the documents.", "did he arrive",
     ["he arrived", "he did arrive", "arrived he"],
     "After a negative adverbial like 'not only' at the start of a sentence, "
     "we invert the subject and auxiliary.")
_add("English", A, "Grammar", "The committee insisted that he ___ the proposal.", "reconsider",
     ["reconsiders", "reconsidered", "would reconsiders"],
     "After 'insist that', the subjunctive uses the base form of the verb.")
_add("English", A, "Grammar", "By this time next year, she ___ her doctorate.", "will have completed",
     ["will complete", "has completed", "would complete"],
     "The future perfect describes an action finished before a future point in time.")
_add("English", A, "Grammar", "It's high time we ___ a decision.", "made",
     ["make", "will make", "have made"],
     "'It's high time' is followed by the past simple, even though it refers to now.")
_add("English", A, "Vocabulary", "The word 'ubiquitous' means ___.", "found everywhere",
     ["extremely rare", "easily broken", "deeply respected"],
     "'Ubiquitous' describes something that seems to be present everywhere.")
_add("English", A, "Vocabulary", "Her argument was so ___ that nobody could refute it.", "cogent",
     ["contrived", "complacent", "candid"],
     "'Cogent' means clear, logical and convincing.")
_add("English", A, "Vocabulary", "The politician's ___ remarks offended many voters.", "disparaging",
     ["disparate", "desperate", "dispassionate"],
     "'Disparaging' means expressing a low opinion of someone. 'Disparate' means "
     "fundamentally different.")
_add("English", A, "Vocabulary", "An 'ephemeral' pleasure is one that ___.", "lasts a very short time",
     ["lasts a lifetime", "is very expensive", "is shared with others"],
     "'Ephemeral' means lasting for a very short time.")
_add("English", A, "Correct word usage", "The new policy will ___ significant changes in how we operate.",
     "entail", ["entice", "entreat", "enthrall"],
     "'Entail' means to involve something as a necessary result.")
_add("English", A, "Phrasal verbs", "The negotiations ___ after both sides refused to compromise.",
     "broke down", ["broke in", "broke out", "broke through"],
     "'Break down' means to fail or collapse.")
_add("English", A, "Phrasal verbs", "I'd like to ___ the matter further before I commit.", "look into",
     ["look after", "look up to", "look out"],
     "'Look into' means to investigate or examine.")
_add("English", A, "Phrasal verbs", "She decided to ___ the offer, as it seemed too good to be true.",
     "turn down", ["turn up", "turn over", "turn in"],
     "'Turn down' means to refuse or reject.")
_add("English", A, "Idiomatic expressions", "To 'bite the bullet' means to ___.",
     "face something unpleasant with courage",
     ["eat very quickly", "speak without thinking", "give up completely"],
     "The idiom means to accept a difficult situation and deal with it bravely.")
_add("English", A, "Idiomatic expressions", "If you 'burn the midnight oil', you ___.",
     "work late into the night", ["waste resources", "lose your temper", "sleep very deeply"],
     "The idiom refers to working or studying very late at night.")
_add("English", A, "Reading comprehension", "What do critics of nuclear energy argue?",
     "Waste storage is unresolved and costs often overrun",
     ["It produces high carbon emissions", "It is too cheap to build",
      "It is unpopular with engineers"],
     "The passage says critics point to unresolved long-term waste storage and "
     "construction costs that exceed initial estimates.",
     passage="While proponents of nuclear energy emphasise its low carbon emissions, "
             "critics counter that the long-term storage of radioactive waste remains "
             "unresolved, and that construction costs frequently exceed initial estimates.")
_add("English", A, "Reading comprehension", "What does 'ostensibly neutral' suggest about the author's tone?",
     "It appears neutral but may not truly be",
     ["It is completely unbiased", "It is openly hostile", "It is deliberately humorous"],
     "'Ostensibly' means 'apparently'. The next clause shows the neutrality is "
     "only on the surface.",
     passage="The author's tone throughout the essay is ostensibly neutral; yet the "
             "careful selection of anecdotes subtly favours one side.")
_add("English", A, "Correct word usage", "The two proposals are fundamentally different; they have little in ___.",
     "common", ["mutual", "same", "share"],
     "'Have something in common' is a fixed expression.")
_add("English", A, "Correct word usage", "She was reprimanded for her ___ attitude towards safety regulations.",
     "cavalier", ["cordial", "copious", "covert"],
     "'Cavalier' means showing a lack of proper concern about something important.")
_add("English", A, "Grammar", "Hardly ___ the building when the alarm went off.", "had she entered",
     ["she had entered", "she entered", "did she enter"],
     "'Hardly... when' is used with the past perfect, and 'hardly' at the start "
     "triggers subject–auxiliary inversion.")


# ============================================================================
# SPANISH
# ============================================================================
_bulk("Spanish", "Beginner", [
    ("Grammar", "Yo ___ estudiante.", "soy", ["es", "eres", "estoy"],
     "With 'yo' (I), 'ser' becomes 'soy'. We use 'ser' for identity and professions."),
    ("Grammar", "Ella ___ en Madrid.", "vive", ["vivo", "vives", "viven"],
     "With 'ella' (she) the verb 'vivir' takes the ending -e: 'vive'."),
    ("Grammar", "Nosotros ___ al cine los sábados.", "vamos", ["van", "voy", "vais"],
     "The 'nosotros' form of 'ir' (to go) is 'vamos'."),
    ("Vocabulary", "¿Cuál es el contrario de «grande»?", "pequeño", ["alto", "lento", "nuevo"],
     "'Pequeño' (small) is the opposite of 'grande' (big)."),
    ("Vocabulary", "El hermano de mi madre es mi ___.", "tío", ["primo", "abuelo", "sobrino"],
     "Your mother's or father's brother is your 'tío' (uncle)."),
    ("Vocabulary", "Uso un ___ para escribir en papel.", "bolígrafo", ["tenedor", "zapato", "espejo"],
     "A 'bolígrafo' is a pen, used for writing."),
    ("Reading comprehension", "¿Cómo va Marta al trabajo?", "En autobús", ["En coche", "A pie", "En tren"],
     "The text says she goes to work 'en autobús' (by bus).",
     "Marta se levanta a las siete. Desayuna café con pan y va al trabajo en autobús. "
     "Empieza a trabajar a las nueve."),
    ("Reading comprehension", "¿Cuándo juega Toby en el parque?", "Por la tarde",
     ["Por la mañana", "Por la noche", "Al mediodía"],
     "The text says Toby plays in the park 'por la tarde' (in the afternoon).",
     "Luis tiene un perro pequeño que se llama Toby. A Toby le gusta jugar en el parque "
     "por la tarde."),
    ("Sentence completion", "Tengo sed. Quiero un vaso de ___.", "agua", ["pan", "arroz", "queso"],
     "We drink 'agua' (water); we eat bread, rice and cheese."),
    ("Sentence completion", "¡Buenos días! ¿Cómo ___ usted?", "está", ["es", "tiene", "hace"],
     "'¿Cómo está usted?' is the formal way to ask 'How are you?'"),
    ("Correct word usage", "Mi cumpleaños es ___ mayo.", "en", ["a", "por", "de"],
     "We use 'en' with months: 'en mayo'."),
    ("Correct word usage", "Hoy hace mucho calor y yo ___ cansado.", "estoy", ["soy", "tengo", "hago"],
     "We use 'estar' for temporary states such as feeling tired."),
    ("Verbs & prepositions", "Voy ___ la escuela en bicicleta.", "a", ["en", "de", "con"],
     "The verb 'ir' (to go) is followed by 'a' to show the destination."),
    ("Idiomatic expressions", "«Estar en las nubes» significa ___.", "estar distraído",
     ["estar contento", "estar enfermo", "tener hambre"],
     "The idiom describes someone who is not paying attention (literally 'to be in the clouds')."),
])
_bulk("Spanish", "Intermediate", [
    ("Grammar", "Si tuviera más tiempo, ___ un idioma nuevo.", "aprendería",
     ["aprendo", "aprenderé", "aprendí"],
     "Hypothetical conditional: 'si' + imperfect subjunctive, then the conditional ('aprendería')."),
    ("Grammar", "Cuando llegué, mis amigos ya ___.", "se habían ido",
     ["se van", "se irán", "se iban"],
     "The pluperfect ('habían' + participle) shows an action completed before another past action."),
    ("Grammar", "Espero que mañana ___ buen tiempo.", "haga", ["hace", "hará", "hizo"],
     "'Esperar que' triggers the present subjunctive: 'haga'."),
    ("Grammar", "Es importante que tú ___ la verdad.", "digas", ["dices", "dirás", "dijiste"],
     "Expressions of necessity or importance + 'que' take the subjunctive: 'digas'."),
    ("Grammar", "Llevo tres años ___ español.", "estudiando", ["estudio", "estudié", "estudiado"],
     "'Llevar' + time + gerund expresses an action that started in the past and continues now."),
    ("Vocabulary", "¿Qué palabra es sinónimo de «comenzar»?", "empezar", ["terminar", "romper", "pensar"],
     "'Empezar' and 'comenzar' both mean to begin."),
    ("Vocabulary", "Hay que ___ los gastos para ahorrar dinero.", "reducir",
     ["producir", "conducir", "traducir"],
     "'Reducir' means to make smaller. The other verbs sound similar but mean produce, drive, translate."),
    ("Vocabulary", "Una persona que habla poco es ___.", "callada",
     ["ruidosa", "generosa", "alegre"],
     "'Callado/a' describes someone quiet who does not speak much."),
    ("Idiomatic expressions", "«Costar un ojo de la cara» significa ___.", "ser muy caro",
     ["ser muy feo", "ser peligroso", "ser muy raro"],
     "The idiom means something is extremely expensive."),
    ("Idiomatic expressions", "«Tomar el pelo» a alguien significa ___.", "burlarse de esa persona",
     ["ayudarla", "peinarla", "despertarla"],
     "'Tomar el pelo' means to tease or fool someone."),
    ("Verbs & prepositions", "Sueño ___ una vida tranquila en el campo.", "con", ["en", "a", "de"],
     "'Soñar con' is the standard construction for dreaming about something."),
    ("Verbs & prepositions", "Me acuerdo ___ mi primer día de clase.", "de", ["en", "a", "por"],
     "'Acordarse de' always takes the preposition 'de'."),
    ("Reading comprehension", "¿Qué desventaja del teletrabajo se menciona?",
     "Algunos empleados se sienten solos", ["Se gana menos dinero", "Se viaja más", "Hay menos libertad"],
     "The text says some employees 'se sienten solos' (feel lonely).",
     "El teletrabajo se ha hecho popular porque ahorra tiempo de desplazamiento. Sin embargo, "
     "algunos empleados dicen que se sienten solos y que les cuesta separar la vida laboral "
     "de la personal."),
    ("Correct word usage", "Gracias ___ tu ayuda.", "por", ["para", "de", "con"],
     "'Gracias por' is the fixed expression for thanking someone for something."),
])
_bulk("Spanish", "Advanced", [
    ("Grammar", "Si hubiera sabido del retraso, ___ antes.", "habría salido",
     ["saldría", "salgo", "saldré"],
     "Third conditional (unreal past): 'si' + pluperfect subjunctive, then 'habría' + participle."),
    ("Grammar", "Ojalá ___ más tiempo para viajar.", "tuviera", ["tengo", "tendré", "tenía"],
     "'Ojalá' + imperfect subjunctive expresses a wish that is unlikely or contrary to reality."),
    ("Grammar", "Para cuando llegues, ya ___ la cena.", "habremos preparado",
     ["preparamos", "prepararemos", "preparábamos"],
     "The future perfect ('habremos' + participle) describes an action finished before a future moment."),
    ("Grammar", "Se prohíbe que los alumnos ___ el móvil en clase.", "usen",
     ["usan", "usarán", "usaron"],
     "Verbs of prohibition + 'que' take the subjunctive: 'usen'."),
    ("Vocabulary", "«Efímero» significa ___.", "de corta duración",
     ["muy caro", "muy antiguo", "muy pesado"],
     "'Efímero' describes something that lasts only a short time."),
    ("Vocabulary", "«Ubicuo» describe algo que ___.", "está en todas partes",
     ["es muy raro", "es muy frágil", "se mueve rápido"],
     "'Ubicuo' means present everywhere at the same time."),
    ("Vocabulary", "Su argumento era tan ___ que nadie pudo rebatirlo.", "contundente",
     ["contiguo", "contagioso", "constante"],
     "'Contundente' describes an argument that is forceful and convincing."),
    ("Correct word usage", "El nuevo reglamento ___ importantes cambios.", "conlleva",
     ["convoca", "conversa", "concierne"],
     "'Conllevar' means to involve or bring with it as a consequence."),
    ("Verbs & prepositions", "Insistió ___ que nadie debía enterarse.", "en", ["de", "por", "a"],
     "'Insistir en' takes the preposition 'en'."),
    ("Verbs & prepositions", "Se dio cuenta ___ su error demasiado tarde.", "de", ["en", "a", "por"],
     "'Darse cuenta de' (to realise) takes the preposition 'de'."),
    ("Idiomatic expressions", "«Morderse la lengua» significa ___.", "contenerse y no decir algo",
     ["hablar demasiado", "mentir", "gritar"],
     "The idiom means to hold back from saying something you want to say."),
    ("Idiomatic expressions", "«Quemarse las pestañas» significa ___.", "estudiar mucho, sobre todo de noche",
     ["enfadarse mucho", "llorar", "cocinar mal"],
     "The idiom describes studying or working very hard, often late at night."),
    ("Reading comprehension", "¿Qué sostienen los críticos de la energía nuclear?",
     "Los residuos no tienen solución y los costes suelen superar lo previsto",
     ["Que emite demasiado carbono", "Que es demasiado barata", "Que no gusta a los ingenieros"],
     "The text says critics point to unresolved waste storage and construction costs that exceed estimates.",
     "Aunque los defensores de la energía nuclear destacan sus bajas emisiones de carbono, "
     "los críticos sostienen que el almacenamiento a largo plazo de los residuos sigue sin "
     "resolverse y que los costes de construcción suelen superar lo previsto."),
    ("Reading comprehension", "¿Qué sugiere la expresión «en apariencia neutral»?",
     "Parece neutral, pero quizá no lo sea", ["Es totalmente imparcial", "Es abiertamente hostil", "Es deliberadamente cómica"],
     "'En apariencia' means 'apparently'. The following clause shows neutrality is only on the surface.",
     "El tono del autor es, en apariencia, neutral; sin embargo, la cuidadosa elección de las "
     "anécdotas favorece sutilmente a una de las partes."),
])

# ============================================================================
# FRENCH
# ============================================================================
_bulk("French", "Beginner", [
    ("Grammar", "Je ___ étudiant.", "suis", ["es", "est", "sommes"],
     "With 'je' (I), 'être' becomes 'suis'."),
    ("Grammar", "Elle ___ à Paris.", "habite", ["habites", "habitons", "habitent"],
     "With 'elle' (she), regular -er verbs end in -e: 'habite'."),
    ("Grammar", "Nous ___ au cinéma le samedi.", "allons", ["allez", "vais", "vont"],
     "The 'nous' form of 'aller' (to go) is 'allons'."),
    ("Vocabulary", "Quel est le contraire de « grand » ?", "petit", ["lent", "vieux", "long"],
     "'Petit' (small) is the opposite of 'grand' (big)."),
    ("Vocabulary", "Le frère de ma mère est mon ___.", "oncle", ["cousin", "grand-père", "neveu"],
     "Your mother's or father's brother is your 'oncle' (uncle)."),
    ("Vocabulary", "J'utilise un ___ pour écrire sur le papier.", "stylo", ["couteau", "oreiller", "miroir"],
     "A 'stylo' is a pen."),
    ("Reading comprehension", "Comment Marie va-t-elle au travail ?", "En bus", ["En voiture", "À pied", "En train"],
     "The text says she goes to work 'en bus'.",
     "Marie se lève à sept heures. Elle prend son petit-déjeuner et va au travail en bus. "
     "Elle commence à neuf heures."),
    ("Reading comprehension", "Quand Toby joue-t-il dans le parc ?", "L'après-midi",
     ["Le matin", "Le soir", "La nuit"],
     "The text says Toby likes to play in the park 'l'après-midi' (in the afternoon).",
     "Paul a un petit chien qui s'appelle Toby. Toby aime jouer dans le parc l'après-midi."),
    ("Sentence completion", "J'ai soif. Je voudrais un verre d'___.", "eau", ["pain", "riz", "fromage"],
     "We drink 'eau' (water); we eat bread, rice and cheese."),
    ("Sentence completion", "Bonjour ! Comment ___-vous ?", "allez", ["allons", "vais", "vont"],
     "'Comment allez-vous ?' is the formal way to ask 'How are you?'"),
    ("Correct word usage", "Mon anniversaire est ___ mai.", "en", ["à", "de", "sur"],
     "We use 'en' with months: 'en mai'."),
    ("Correct word usage", "Il fait chaud et j'___ soif.", "ai", ["suis", "fais", "vais"],
     "French uses 'avoir' (to have) for thirst: 'avoir soif'."),
    ("Verbs & prepositions", "Je vais ___ l'école à vélo.", "à", ["en", "de", "avec"],
     "The verb 'aller' takes 'à' to show the destination."),
    ("Idiomatic expressions", "« Il pleut des cordes » signifie ___.", "il pleut très fort",
     ["il fait très froid", "il y a du vent", "il neige"],
     "The idiom means it is raining heavily."),
])
_bulk("French", "Intermediate", [
    ("Grammar", "Si j'avais plus de temps, j'___ une nouvelle langue.", "apprendrais",
     ["apprends", "apprendrai", "ai appris"],
     "Hypothetical conditional: 'si' + imparfait, then the conditionnel ('apprendrais')."),
    ("Grammar", "Quand je suis arrivé, mes amis étaient déjà ___.", "partis",
     ["partir", "partaient", "parti"],
     "The pluperfect with 'être' requires the participle to agree with the plural subject: 'partis'."),
    ("Grammar", "Il faut que tu ___ la vérité.", "dises", ["dis", "diras", "as dit"],
     "'Il faut que' is followed by the subjunctive: 'dises'."),
    ("Grammar", "J'habite en France ___ 2015.", "depuis", ["pendant", "il y a", "pour"],
     "'Depuis' marks the starting point of an action that continues now."),
    ("Grammar", "Elle m'a dit qu'elle ___ le lendemain.", "viendrait", ["viendra", "vient", "vienne"],
     "In reported speech after a past verb, the future becomes the conditionnel: 'viendrait'."),
    ("Vocabulary", "Quel mot est synonyme de « commencer » ?", "débuter", ["terminer", "casser", "penser"],
     "'Débuter' and 'commencer' both mean to begin."),
    ("Vocabulary", "Il faut ___ les dépenses pour économiser.", "réduire",
     ["produire", "conduire", "traduire"],
     "'Réduire' means to cut down. The other verbs mean produce, drive and translate."),
    ("Vocabulary", "Une personne qui parle peu est ___.", "réservée",
     ["bruyante", "généreuse", "joyeuse"],
     "'Réservé(e)' describes someone quiet who keeps to themselves."),
    ("Idiomatic expressions", "« Coûter les yeux de la tête » signifie ___.", "être très cher",
     ["être très laid", "être dangereux", "être très rare"],
     "The idiom means something is extremely expensive."),
    ("Idiomatic expressions", "« Poser un lapin à quelqu'un » signifie ___.",
     "ne pas venir à un rendez-vous", ["lui offrir un cadeau", "l'inviter à dîner", "se moquer de lui"],
     "The idiom means to stand someone up."),
    ("Verbs & prepositions", "Je rêve ___ voyager autour du monde.", "de", ["à", "en", "sur"],
     "'Rêver de' + infinitive expresses a dream or wish."),
    ("Verbs & prepositions", "Je pense ___ mes prochaines vacances.", "à", ["de", "en", "sur"],
     "'Penser à' means to think about something or someone."),
    ("Reading comprehension", "Quel inconvénient du télétravail est mentionné ?",
     "Certains employés se sentent isolés", ["Des trajets plus longs", "Des salaires plus bas", "Des horaires moins flexibles"],
     "The text says some employees feel isolated ('se sentir isolés').",
     "Le télétravail est devenu populaire parce qu'il fait gagner du temps de transport. "
     "Cependant, certains employés disent se sentir isolés et avoir du mal à séparer vie "
     "professionnelle et vie personnelle."),
    ("Correct word usage", "Il y a beaucoup ___ monde ici.", "de", ["du", "des", "de la"],
     "After adverbs of quantity such as 'beaucoup', we use 'de' without an article: 'beaucoup de monde'."),
])
_bulk("French", "Advanced", [
    ("Grammar", "Si j'avais su pour le retard, je ___ plus tôt.", "serais parti",
     ["partirais", "suis parti", "partirai"],
     "Unreal past condition: 'si' + plus-que-parfait, then the conditionnel passé ('serais parti')."),
    ("Grammar", "Il est essentiel que nous ___ une décision rapidement.", "prenions",
     ["prenons", "prendrons", "avons pris"],
     "Expressions of necessity ('il est essentiel que') take the subjunctive: 'prenions'."),
    ("Grammar", "Bien qu'il ___ fatigué, il a continué à travailler.", "soit",
     ["est", "sera", "était"],
     "'Bien que' (although) is always followed by the subjunctive: 'soit'."),
    ("Grammar", "Quand tu arriveras, nous ___ déjà dîné.", "aurons", ["avons", "avions", "eûmes"],
     "The futur antérieur ('aurons' + participle) shows an action completed before a future moment."),
    ("Vocabulary", "« Éphémère » signifie ___.", "qui dure très peu de temps",
     ["très cher", "très ancien", "très lourd"],
     "'Éphémère' describes something short-lived."),
    ("Vocabulary", "« Une pléthore de » signifie ___.", "une très grande quantité de",
     ["un manque de", "une petite quantité de", "un danger de"],
     "'Une pléthore de' means an excessive abundance of something."),
    ("Vocabulary", "Son argumentation était si ___ que personne n'a pu la réfuter.", "convaincante",
     ["convenable", "convoitée", "convenue"],
     "'Convaincant(e)' means persuasive. 'Convenable' means proper or suitable."),
    ("Correct word usage", "Cette nouvelle politique va ___ des changements importants.", "entraîner",
     ["entretenir", "entrevoir", "entrouvrir"],
     "'Entraîner' means to bring about or lead to a consequence."),
    ("Verbs & prepositions", "Il a insisté ___ que personne ne soit informé.", "pour",
     ["sur", "de", "à"],
     "'Insister pour que' + subjunctive means to insist that something be done."),
    ("Verbs & prepositions", "Elle s'est rendu compte ___ son erreur trop tard.", "de", ["à", "en", "sur"],
     "'Se rendre compte de' (to realise) takes 'de'."),
    ("Idiomatic expressions", "« Se mordre les doigts d'avoir fait quelque chose » signifie ___.",
     "le regretter amèrement", ["avoir faim", "s'excuser poliment", "se blesser"],
     "The idiom means to bitterly regret an action."),
    ("Idiomatic expressions", "« Mettre de l'eau dans son vin » signifie ___.",
     "modérer ses exigences", ["boire moins", "se mettre en colère", "mentir"],
     "The idiom means to tone down one's demands and compromise."),
    ("Reading comprehension", "Que soutiennent les détracteurs du nucléaire ?",
     "Le stockage des déchets n'est pas résolu et les coûts dépassent souvent les prévisions",
     ["Il émet trop de carbone", "Il est trop bon marché", "Il déplaît aux ingénieurs"],
     "The text says critics cite unresolved waste storage and construction costs exceeding forecasts.",
     "Si les partisans de l'énergie nucléaire soulignent ses faibles émissions de carbone, "
     "les détracteurs répliquent que le stockage à long terme des déchets radioactifs reste un "
     "problème non résolu et que les coûts de construction dépassent souvent les prévisions."),
    ("Reading comprehension", "Que suggère l'expression « en apparence neutre » ?",
     "Il semble neutre, mais peut-être ne l'est-il pas",
     ["Il est totalement impartial", "Il est ouvertement hostile", "Il est volontairement comique"],
     "'En apparence' means 'apparently'. The next clause shows the neutrality is superficial.",
     "Le ton de l'auteur est en apparence neutre ; pourtant, le choix soigneux des anecdotes "
     "favorise subtilement un camp."),
])

# ============================================================================
# GERMAN
# ============================================================================
_bulk("German", "Beginner", [
    ("Grammar", "Ich ___ Student.", "bin", ["bist", "ist", "sind"],
     "With 'ich' (I), 'sein' becomes 'bin'."),
    ("Grammar", "Sie ___ in Berlin.", "wohnt", ["wohne", "wohnst", "wohnen"],
     "With 'sie' (she), regular verbs end in -t: 'wohnt'."),
    ("Grammar", "Wir ___ am Samstag ins Kino.", "gehen", ["geht", "gehst", "gehe"],
     "With 'wir' (we), the verb takes the infinitive form: 'gehen'."),
    ("Vocabulary", "Was ist das Gegenteil von „groß“?", "klein", ["lang", "alt", "schnell"],
     "'Klein' (small) is the opposite of 'groß' (big)."),
    ("Vocabulary", "Der Bruder meiner Mutter ist mein ___.", "Onkel", ["Cousin", "Opa", "Neffe"],
     "Your mother's or father's brother is your 'Onkel' (uncle)."),
    ("Vocabulary", "Ich schreibe mit einem ___.", "Stift", ["Messer", "Kissen", "Spiegel"],
     "A 'Stift' is a pen or pencil, used for writing."),
    ("Reading comprehension", "Wie fährt Anna zur Arbeit?", "Mit dem Bus", ["Mit dem Auto", "Zu Fuß", "Mit dem Zug"],
     "The text says she goes to work 'mit dem Bus' (by bus).",
     "Anna steht um sieben Uhr auf. Sie frühstückt und fährt mit dem Bus zur Arbeit. "
     "Um neun Uhr beginnt sie zu arbeiten."),
    ("Reading comprehension", "Wann spielt Toby im Park?", "Am Nachmittag",
     ["Am Morgen", "Am Abend", "In der Nacht"],
     "The text says Toby plays in the park 'am Nachmittag' (in the afternoon).",
     "Tim hat einen kleinen Hund. Er heißt Toby und spielt gern am Nachmittag im Park."),
    ("Sentence completion", "Ich habe Durst. Ich möchte ein Glas ___.", "Wasser", ["Brot", "Reis", "Käse"],
     "We drink 'Wasser' (water); we eat bread, rice and cheese."),
    ("Sentence completion", "Guten Morgen! Wie ___ es Ihnen?", "geht", ["ist", "hat", "macht"],
     "'Wie geht es Ihnen?' is the formal way to ask 'How are you?'"),
    ("Correct word usage", "Mein Geburtstag ist ___ Mai.", "im", ["am", "um", "auf"],
     "We use 'im' (in + dem) with months: 'im Mai'."),
    ("Correct word usage", "Ich habe ___ Apfel.", "einen", ["ein", "eine", "einem"],
     "'Apfel' is masculine and is the direct object, so it takes the accusative 'einen'."),
    ("Verbs & prepositions", "Ich rufe meine Mutter ___.", "an", ["auf", "ab", "aus"],
     "'Anrufen' is a separable verb: the prefix 'an' goes to the end of the sentence."),
    ("Idiomatic expressions", "Was bedeutet „Ich drücke dir die Daumen“?", "Ich wünsche dir viel Glück.",
     ["Ich bin böse auf dich.", "Ich gebe dir Geld.", "Ich helfe dir beim Tragen."],
     "'Die Daumen drücken' (literally 'press the thumbs') means to wish someone good luck."),
])
_bulk("German", "Intermediate", [
    ("Grammar", "Wenn ich mehr Zeit ___, würde ich eine neue Sprache lernen.", "hätte",
     ["habe", "hatte", "haben"],
     "Unreal conditions use Konjunktiv II ('hätte') together with 'würde' + infinitive."),
    ("Grammar", "Als ich ankam, ___ meine Freunde schon gegangen.", "waren",
     ["sind", "haben", "wurden"],
     "The Plusquamperfekt uses 'waren' + participle with verbs of motion such as 'gehen'."),
    ("Grammar", "Ich warte ___ den Bus.", "auf", ["an", "für", "über"],
     "'Warten auf' + accusative is the fixed construction."),
    ("Grammar", "Er hat gefragt, ___ ich Zeit habe.", "ob", ["dass", "wenn", "weil"],
     "'Ob' introduces an indirect yes/no question."),
    ("Grammar", "Das Buch, ___ ich gelesen habe, war spannend.", "das", ["der", "dem", "die"],
     "The relative pronoun must be neuter ('Buch') and accusative: 'das'."),
    ("Vocabulary", "Welches Wort ist ein Synonym für „anfangen“?", "beginnen", ["beenden", "brechen", "denken"],
     "'Beginnen' and 'anfangen' both mean to begin."),
    ("Vocabulary", "Man muss die Kosten ___, um Geld zu sparen.", "senken",
     ["schenken", "lenken", "denken"],
     "'Senken' means to lower or reduce."),
    ("Vocabulary", "Jemand, der wenig spricht, ist ___.", "schweigsam",
     ["laut", "großzügig", "fröhlich"],
     "'Schweigsam' describes a person who says little."),
    ("Idiomatic expressions", "Was bedeutet „Ich verstehe nur Bahnhof“?", "Ich verstehe gar nichts.",
     ["Ich bin am Bahnhof.", "Ich will verreisen.", "Ich verstehe alles."],
     "The idiom means you cannot understand anything at all."),
    ("Idiomatic expressions", "„Jemandem einen Bären aufbinden“ bedeutet ___.",
     "jemandem etwas Unwahres erzählen", ["jemandem ein Geschenk machen", "jemanden besuchen", "jemanden erschrecken"],
     "The idiom means to tell someone a tall tale or trick them."),
    ("Verbs & prepositions", "Ich träume ___ einer Reise um die Welt.", "von", ["mit", "auf", "an"],
     "'Träumen von' is the fixed construction."),
    ("Verbs & prepositions", "Ich erinnere mich gern ___ meine Kindheit.", "an", ["von", "auf", "über"],
     "'Sich erinnern an' + accusative is the fixed construction."),
    ("Reading comprehension", "Welcher Nachteil des Homeoffice wird genannt?",
     "Manche Beschäftigte fühlen sich allein", ["Längere Fahrzeiten", "Niedrigere Gehälter", "Weniger flexible Zeiten"],
     "The text says some employees feel alone ('sich allein fühlen').",
     "Das Homeoffice ist beliebt geworden, weil man Fahrzeit spart. Manche Beschäftigte sagen "
     "jedoch, dass sie sich allein fühlen und Beruf und Privatleben schwer trennen können."),
    ("Correct word usage", "Ich bin stolz ___ dich.", "auf", ["von", "für", "an"],
     "'Stolz sein auf' + accusative is the fixed construction."),
])
_bulk("German", "Advanced", [
    ("Grammar", "Hätte ich von der Verspätung gewusst, ___ ich früher losgefahren.", "wäre",
     ["hätte", "würde", "war"],
     "Unreal past condition: Konjunktiv II of the perfect. 'Losfahren' forms its perfect with 'sein', so 'wäre'."),
    ("Grammar", "Er tat so, als ___ er nichts gehört.", "hätte", ["hatte", "hat", "haben"],
     "'Als ob / als' for something unreal takes Konjunktiv II: 'hätte'."),
    ("Grammar", "Das Fest wurde ___ des starken Regens abgesagt.", "wegen", ["trotz", "dank", "entgegen"],
     "'Wegen' + genitive gives the reason. 'Trotz' (despite) would not make sense here."),
    ("Grammar", "Der Vertrag soll bis Freitag unterschrieben ___.", "werden", ["sein", "haben", "worden"],
     "The passive infinitive is participle + 'werden'."),
    ("Vocabulary", "„Allgegenwärtig“ bedeutet ___.", "überall vorhanden",
     ["sehr selten", "zerbrechlich", "sehr teuer"],
     "'Allgegenwärtig' describes something that is present everywhere."),
    ("Vocabulary", "Sein Argument war so ___, dass niemand es widerlegen konnte.", "stichhaltig",
     ["stichelnd", "sträflich", "strittig"],
     "'Stichhaltig' means sound and convincing."),
    ("Correct word usage", "Die neue Regelung zieht erhebliche Änderungen ___ sich.", "nach",
     ["mit", "bei", "für"],
     "'Nach sich ziehen' is a fixed expression meaning to bring about as a consequence."),
    ("Correct word usage", "Seine Bemerkungen waren ___ und verletzten viele Menschen.", "abfällig",
     ["ausführlich", "abwechselnd", "ausgiebig"],
     "'Abfällig' means disparaging or contemptuous."),
    ("Verbs & prepositions", "Er bestand ___ seinem Recht.", "auf", ["an", "in", "zu"],
     "'Bestehen auf' + dative means to insist on something."),
    ("Verbs & prepositions", "Das hängt ___ vielen Faktoren ab.", "von", ["an", "mit", "bei"],
     "'Abhängen von' means to depend on."),
    ("Idiomatic expressions", "„Jemandem den Wind aus den Segeln nehmen“ bedeutet ___.",
     "jemandes Argumente oder Pläne entkräften", ["jemandem helfen", "jemanden warnen", "jemanden einladen"],
     "The idiom means to take away someone's advantage or argument."),
    ("Idiomatic expressions", "„Die Katze aus dem Sack lassen“ bedeutet ___.", "ein Geheimnis verraten",
     ["ein Tier verkaufen", "etwas verstecken", "einen Fehler machen"],
     "The idiom means to let a secret slip."),
    ("Reading comprehension", "Was entgegnen die Kritiker der Kernenergie?",
     "Die Lagerung des Abfalls ist ungelöst und die Baukosten steigen oft über die Schätzungen",
     ["Sie stößt zu viel CO₂ aus", "Sie ist zu billig", "Sie ist bei Ingenieuren unbeliebt"],
     "The text says critics cite unresolved waste storage and construction costs exceeding estimates.",
     "Während Befürworter der Kernenergie die geringen CO₂-Emissionen betonen, entgegnen "
     "Kritiker, dass die langfristige Lagerung radioaktiver Abfälle ungelöst bleibe und die "
     "Baukosten häufig die ursprünglichen Schätzungen überstiegen."),
    ("Reading comprehension", "Was deutet „dem Anschein nach neutral“ an?",
     "Er wirkt neutral, ist es aber vielleicht nicht", ["Er ist völlig unparteiisch", "Er ist offen feindselig", "Er ist absichtlich witzig"],
     "'Dem Anschein nach' means 'apparently'. The next clause shows the neutrality is only superficial.",
     "Der Ton des Autors ist dem Anschein nach neutral; dennoch bevorzugt die sorgfältige "
     "Auswahl der Anekdoten unterschwellig eine Seite."),
])

# ============================================================================
# PORTUGUESE (Brazilian)
# ============================================================================
_bulk("Portuguese", "Beginner", [
    ("Grammar", "Eu ___ estudante.", "sou", ["é", "estou", "somos"],
     "With 'eu' (I), 'ser' becomes 'sou'. We use 'ser' for identity and professions."),
    ("Grammar", "Ela ___ em São Paulo.", "mora", ["moro", "moras", "moram"],
     "With 'ela' (she), the verb 'morar' becomes 'mora'."),
    ("Grammar", "Nós ___ ao cinema aos sábados.", "vamos", ["vão", "vou", "vais"],
     "The 'nós' form of 'ir' (to go) is 'vamos'."),
    ("Vocabulary", "Qual é o contrário de «grande»?", "pequeno", ["alto", "lento", "novo"],
     "'Pequeno' (small) is the opposite of 'grande' (big)."),
    ("Vocabulary", "O irmão da minha mãe é meu ___.", "tio", ["primo", "avô", "sobrinho"],
     "Your mother's or father's brother is your 'tio' (uncle)."),
    ("Vocabulary", "Eu uso uma ___ para escrever.", "caneta", ["faca", "almofada", "espelho"],
     "A 'caneta' is a pen, used for writing."),
    ("Reading comprehension", "Como Ana vai para o trabalho?", "De ônibus", ["De carro", "A pé", "De trem"],
     "The text says she goes to work 'de ônibus' (by bus).",
     "Ana acorda às sete horas. Ela toma café da manhã e vai para o trabalho de ônibus. "
     "Começa a trabalhar às nove."),
    ("Reading comprehension", "Quando o Totó brinca no parque?", "À tarde", ["De manhã", "À noite", "De madrugada"],
     "The text says Totó likes to play in the park 'à tarde' (in the afternoon).",
     "Pedro tem um cachorro pequeno chamado Totó. Totó gosta de brincar no parque à tarde."),
    ("Sentence completion", "Estou com sede. Quero um copo de ___.", "água", ["pão", "arroz", "queijo"],
     "We drink 'água' (water); we eat bread, rice and cheese."),
    ("Sentence completion", "Bom dia! Como o senhor ___?", "está", ["é", "faz", "tem"],
     "'Como o senhor está?' is the polite way to ask 'How are you?'"),
    ("Correct word usage", "Meu aniversário é ___ maio.", "em", ["a", "por", "de"],
     "We use 'em' with months: 'em maio'."),
    ("Correct word usage", "Hoje faz muito calor e eu ___ cansado.", "estou", ["sou", "faço", "vou"],
     "We use 'estar' for temporary states such as feeling tired."),
    ("Verbs & prepositions", "Eu gosto ___ música brasileira.", "de", ["em", "a", "por"],
     "'Gostar' is always followed by the preposition 'de'."),
    ("Idiomatic expressions", "«Está chovendo a cântaros» significa ___.", "está chovendo muito",
     ["está fazendo frio", "está ventando", "está nevando"],
     "The idiom means it is raining heavily."),
])
_bulk("Portuguese", "Intermediate", [
    ("Grammar", "Se eu tivesse mais tempo, ___ uma nova língua.", "aprenderia",
     ["aprendo", "aprenderei", "aprendi"],
     "Hypothetical conditional: 'se' + imperfect subjunctive, then the conditional ('aprenderia')."),
    ("Grammar", "Quando cheguei, meus amigos já ___.", "tinham saído",
     ["saem", "sairão", "saindo"],
     "The pluperfect ('tinham' + participle) shows an action completed before another past action."),
    ("Grammar", "Espero que amanhã ___ bom tempo.", "faça", ["faz", "fará", "fez"],
     "'Esperar que' triggers the present subjunctive: 'faça'."),
    ("Grammar", "É importante que você ___ a verdade.", "diga", ["diz", "dirá", "disse"],
     "Expressions of importance + 'que' take the subjunctive: 'diga'."),
    ("Grammar", "Moro no Brasil ___ 2015.", "desde", ["durante", "há", "por"],
     "'Desde' marks the starting point of an action that continues now."),
    ("Vocabulary", "Qual palavra é sinônimo de «começar»?", "iniciar", ["terminar", "quebrar", "pensar"],
     "'Iniciar' and 'começar' both mean to begin."),
    ("Vocabulary", "É preciso ___ os gastos para economizar.", "reduzir",
     ["produzir", "conduzir", "traduzir"],
     "'Reduzir' means to cut down. The other verbs mean produce, drive and translate."),
    ("Vocabulary", "Uma pessoa que fala pouco é ___.", "calada",
     ["barulhenta", "generosa", "alegre"],
     "'Calado/a' describes someone quiet who does not speak much."),
    ("Idiomatic expressions", "«Custar os olhos da cara» significa ___.", "ser muito caro",
     ["ser muito feio", "ser perigoso", "ser muito raro"],
     "The idiom means something is extremely expensive."),
    ("Idiomatic expressions", "«Dar o bolo» em alguém significa ___.", "não aparecer a um encontro",
     ["oferecer um presente", "convidar para jantar", "ajudar a cozinhar"],
     "The idiom means to stand someone up."),
    ("Verbs & prepositions", "Eu sonho ___ uma viagem pelo mundo.", "com", ["em", "de", "por"],
     "'Sonhar com' + noun is the standard construction for dreaming about something."),
    ("Verbs & prepositions", "Eu me lembro ___ meu primeiro dia de aula.", "do", ["no", "ao", "pelo"],
     "'Lembrar-se de' + 'o' contracts to 'do'."),
    ("Reading comprehension", "Qual desvantagem do trabalho remoto é mencionada?",
     "Alguns funcionários se sentem isolados", ["Deslocamentos mais longos", "Salários mais baixos", "Horários menos flexíveis"],
     "The text says some employees feel isolated ('se sentem isolados').",
     "O trabalho remoto ficou popular porque economiza tempo de deslocamento. No entanto, "
     "alguns funcionários dizem que se sentem isolados e têm dificuldade em separar a vida "
     "profissional da pessoal."),
    ("Correct word usage", "Obrigado ___ sua ajuda.", "pela", ["de", "à", "com"],
     "'Obrigado' is followed by 'por' (here contracted with 'a': 'pela')."),
])
_bulk("Portuguese", "Advanced", [
    ("Grammar", "Se eu tivesse sabido do atraso, ___ mais cedo.", "teria saído",
     ["sairia", "saí", "sairei"],
     "Unreal past condition: 'se' + pluperfect subjunctive, then 'teria' + participle."),
    ("Grammar", "Quando você chegar, nós já ___ o jantar.", "teremos preparado",
     ["preparamos", "prepararíamos", "preparávamos"],
     "The future perfect ('teremos' + participle) describes an action finished before a future moment."),
    ("Grammar", "Embora ele ___ cansado, continuou trabalhando.", "estivesse",
     ["estava", "esteve", "estará"],
     "'Embora' (although) takes the subjunctive: 'estivesse'."),
    ("Grammar", "O comitê exigiu que ele ___ a proposta.", "reconsiderasse",
     ["reconsiderou", "reconsiderava", "reconsiderará"],
     "Verbs of demand in the past + 'que' take the imperfect subjunctive."),
    ("Vocabulary", "«Efêmero» significa ___.", "de curta duração",
     ["muito caro", "muito antigo", "muito pesado"],
     "'Efêmero' describes something that lasts only a short time."),
    ("Vocabulary", "«Onipresente» descreve algo que ___.", "está em toda parte",
     ["é muito raro", "é muito frágil", "se move depressa"],
     "'Onipresente' means present everywhere at the same time."),
    ("Vocabulary", "O argumento dela era tão ___ que ninguém conseguiu refutá-lo.", "convincente",
     ["convidativo", "conveniente", "convencional"],
     "'Convincente' means persuasive. 'Conveniente' means suitable or practical."),
    ("Correct word usage", "A nova política vai ___ mudanças importantes.", "acarretar",
     ["acarear", "acariciar", "acarinhar"],
     "'Acarretar' means to bring about as a consequence."),
    ("Verbs & prepositions", "Ele insistiu ___ que ninguém soubesse.", "em", ["de", "por", "a"],
     "'Insistir em' takes the preposition 'em'."),
    ("Verbs & prepositions", "Ela se deu conta ___ erro tarde demais.", "do", ["no", "ao", "pelo"],
     "'Dar-se conta de' (to realise) takes 'de'; with 'o erro' it contracts to 'do'."),
    ("Idiomatic expressions", "«Engolir sapos» significa ___.",
     "aguentar situações desagradáveis sem reclamar", ["comer algo estranho", "falar demais", "ficar com raiva"],
     "The idiom means to put up with unpleasant situations without complaining."),
    ("Idiomatic expressions", "«Queimar as pestanas» significa ___.", "estudar muito, especialmente à noite",
     ["ficar com raiva", "chorar muito", "cozinhar mal"],
     "The idiom describes studying hard, often late at night."),
    ("Reading comprehension", "O que afirmam os críticos da energia nuclear?",
     "Os resíduos não têm solução e os custos costumam superar as estimativas",
     ["Que emite muito carbono", "Que é barata demais", "Que os engenheiros não gostam"],
     "The text says critics cite unresolved waste storage and construction costs exceeding estimates.",
     "Embora os defensores da energia nuclear destaquem suas baixas emissões de carbono, os "
     "críticos afirmam que o armazenamento de longo prazo dos resíduos radioativos continua sem "
     "solução e que os custos de construção frequentemente superam as estimativas iniciais."),
    ("Reading comprehension", "O que sugere a expressão «aparentemente neutro»?",
     "Parece neutro, mas talvez não seja", ["É totalmente imparcial", "É abertamente hostil", "É propositalmente cômico"],
     "'Aparentemente' means 'apparently'. The next clause shows the neutrality is only on the surface.",
     "O tom do autor é, aparentemente, neutro; no entanto, a escolha cuidadosa das anedotas "
     "favorece sutilmente um dos lados."),
])


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


def build_quiz(language, level):
    """Pick random questions for a language and level, preferring ones not seen recently."""
    pool = QUESTION_BANK[language][level]
    seen = st.session_state.seen[(language, level)]
    unseen = [q for q in pool if q["id"] not in seen]

    if len(unseen) >= QUESTIONS_PER_QUIZ:
        picked = random.sample(unseen, QUESTIONS_PER_QUIZ)
        seen.update(q["id"] for q in picked)
    else:
        # Use whatever is left, top up from the rest, then restart the cycle.
        others = [q for q in pool if q["id"] in seen]
        picked = unseen + random.sample(others, QUESTIONS_PER_QUIZ - len(unseen))
        st.session_state.seen[(language, level)] = {q["id"] for q in picked}

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
        "language": "English",
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
    st.session_state.quiz = build_quiz(st.session_state.language, level)
    st.session_state.answers = {}
    st.session_state.current = 0
    st.session_state.result = None
    st.session_state.warning = None
    st.session_state.quiz_id += 1
    st.session_state.stage = "quiz"


def start_from_home():
    start_quiz(st.session_state.home_level)


def set_language():
    st.session_state.language = st.session_state.home_language


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
        "language": st.session_state.language,
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

def esc(text):
    """HTML-escape text before placing it inside custom markup."""
    return html.escape(text, quote=True)


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
        .stApp {background: #F6F8FC; color: #0B1F4B;}
        #MainMenu, footer {visibility: hidden;}
        .block-container {max-width: 820px; padding-top: 4.5rem; padding-bottom: 3rem;}
        h1, h2, h3 {color: #0B1F4B; font-weight: 700; letter-spacing: -0.3px;}
        [data-testid="stCaptionContainer"] {color: #5B6784;}
        hr {border-color: #E3E7F0;}

        /* ---------- Brand header ---------- */
        .yen-brand {display: flex; align-items: center; justify-content: space-between;
                    gap: 12px; margin-bottom: 1.25rem;}
        .yen-brand-left {display: flex; align-items: center; gap: 12px;}
        .yen-brand img {height: 48px; width: 48px;}
        .yen-word {font-size: 1.75rem; line-height: 1; letter-spacing: -0.6px;
                   white-space: nowrap; color: #0B1F4B;}
        .yen-word .lingua {font-weight: 700;}
        .yen-word .now {font-weight: 700; color: #D62839;}
        .yen-pill {font-size: .75rem; font-weight: 500; color: #0B1F4B; background: #FFFFFF;
                   border: 1px solid #E3E7F0; border-radius: 999px; padding: .3rem .85rem;
                   white-space: nowrap;}

        /* ---------- Hero ---------- */
        .yen-hero {position: relative; overflow: hidden; border-radius: 22px;
                   background: linear-gradient(135deg, #0B1F4B 0%, #16337F 100%);
                   padding: 2rem 1.8rem 1.6rem; margin-bottom: .5rem;}
        .yen-hero::after {content: ""; position: absolute; right: -50px; top: -50px;
                          width: 190px; height: 190px; border-radius: 50%;
                          background: #D62839; opacity: .92;}
        .yen-hero::before {content: ""; position: absolute; right: 70px; top: 120px;
                           width: 70px; height: 70px; border-radius: 50%;
                           background: rgba(255,255,255,.10);}
        .yen-hero > * {position: relative; z-index: 1;}
        .yen-eyebrow {font-size: .72rem; letter-spacing: .14em; text-transform: uppercase;
                      font-weight: 600; color: #FF8A96 !important;}
        .yen-hero-title {font-size: 2.2rem; font-weight: 700; line-height: 1.15;
                         letter-spacing: -0.8px; margin: .5rem 0 .8rem;
                         color: #FFFFFF !important; max-width: 80%;}
        .yen-hero-title em {font-style: normal; color: #FF8A96 !important;}
        .yen-hero p {color: #DCE2F2 !important; margin: 0 0 1.1rem; line-height: 1.6;
                     max-width: 88%; font-size: .98rem;}
        .yen-chips {display: flex; flex-wrap: wrap; gap: .45rem;}
        .yen-chips span {color: #FFFFFF !important; font-size: .8rem; font-weight: 500;
                         border: 1px solid rgba(255,255,255,.4); border-radius: 999px;
                         padding: .25rem .8rem; background: rgba(255,255,255,.08);}

        /* ---------- Steps ---------- */
        .yen-step {display: flex; align-items: center; gap: .6rem; font-weight: 600;
                   font-size: 1.05rem; margin: 1.6rem 0 .6rem; color: #0B1F4B;}
        .yen-step span {background: #D62839; color: #FFFFFF; border-radius: 50%;
                        width: 1.7rem; height: 1.7rem; display: inline-grid;
                        place-items: center; font-size: .85rem; font-weight: 600;}

        /* ---------- Buttons ---------- */
        div.stButton > button {width: 100%; border-radius: 12px; padding: 0.65rem 1rem;
                               font-weight: 600; transition: all .15s ease;}
        button[kind="primary"], [data-testid="stBaseButton-primary"] {
            background: #D62839; border: 1.5px solid #D62839; color: #FFFFFF;}
        button[kind="primary"]:hover, [data-testid="stBaseButton-primary"]:hover {
            background: #B71F2E; border-color: #B71F2E; color: #FFFFFF;}
        button[kind="secondary"], [data-testid="stBaseButton-secondary"] {
            background: #FFFFFF; border: 1.5px solid #0B1F4B; color: #0B1F4B;}
        button[kind="secondary"]:hover, [data-testid="stBaseButton-secondary"]:hover {
            background: #0B1F4B; color: #FFFFFF; border-color: #0B1F4B;}
        .st-key-btn_start button {padding: .9rem 1rem; font-size: 1.05rem;
                                  box-shadow: 0 8px 20px rgba(214,40,57,.25);}

        /* ---------- Radio options as cards ---------- */
        div[role="radiogroup"] {gap: .5rem;}
        div[role="radiogroup"] > label {
            border: 1.5px solid #D7DCE8; border-radius: 14px; padding: .75rem 1rem;
            background: #FFFFFF; width: 100%; transition: border-color .15s, background .15s;}
        div[role="radiogroup"] > label:hover {border-color: #0B1F4B;}
        div[role="radiogroup"] > label:has(input:checked) {
            border-color: #D62839; background: #FDF1F2;}

        /* Language picker: compact pills */
        .st-key-lang_picker div[role="radiogroup"] {flex-direction: row; flex-wrap: wrap;}
        .st-key-lang_picker div[role="radiogroup"] > label {
            width: auto; padding: .45rem 1rem; border-radius: 999px;}
        .st-key-lang_picker div[role="radiogroup"] > label:has(input:checked) {
            background: #0B1F4B; border-color: #0B1F4B;}
        .st-key-lang_picker div[role="radiogroup"] > label:has(input:checked) * {
            color: #FFFFFF !important;}

        /* ---------- Quiz ---------- */
        .yen-chiprow {display: flex; flex-wrap: wrap; gap: .4rem; margin-bottom: .8rem;}
        .yen-chip {font-size: .78rem; font-weight: 500; border-radius: 999px;
                   padding: .25rem .8rem; background: #FFFFFF; border: 1px solid #E3E7F0;
                   color: #0B1F4B;}
        .yen-chip.navy {background: #0B1F4B; border-color: #0B1F4B; color: #FFFFFF;}
        .yen-chip.red {background: #D62839; border-color: #D62839; color: #FFFFFF;}
        .st-key-qcard {background: #FFFFFF; border: 1px solid #E3E7F0; border-radius: 20px;
                       padding: 1.3rem 1.3rem 1rem; margin: .8rem 0 1rem;
                       box-shadow: 0 8px 28px rgba(11,31,75,.07);}
        .yen-tag {display: inline-block; font-size: .7rem; font-weight: 600;
                  letter-spacing: .08em; text-transform: uppercase; color: #D62839;
                  background: #FDF1F2; border-radius: 6px; padding: .2rem .55rem;}
        .yen-q {font-size: 1.2rem; font-weight: 600; line-height: 1.45;
                margin: .7rem 0 1rem; color: #0B1F4B;}

        /* ---------- Results ---------- */
        .yen-score {display: flex; align-items: center; flex-wrap: wrap; gap: 1.5rem;
                    background: linear-gradient(135deg, #0B1F4B 0%, #16337F 100%);
                    border-radius: 22px; padding: 1.6rem; margin: .2rem 0 1rem;
                    border-left: 8px solid #D62839;}
        .yen-ring {width: 124px; height: 124px; border-radius: 50%; flex: none;
                   display: grid; place-items: center;}
        .yen-ring-in {width: 94px; height: 94px; border-radius: 50%; background: #0B1F4B;
                      display: grid; place-items: center; color: #FFFFFF !important;
                      font-size: 1.6rem; font-weight: 700;}
        .yen-score h2 {color: #FFFFFF !important; margin: .2rem 0 .3rem; font-size: 1.7rem;}
        .yen-score p {color: #DCE2F2 !important; margin: 0 0 .4rem;}
        .yen-score-line {color: #FFFFFF !important; font-weight: 600;}
        .yen-card {background: #FFFFFF; border: 1px solid #E3E7F0; border-radius: 16px;
                   padding: 1rem 1.2rem; margin: 1rem 0;}
        .yen-card-title {font-weight: 600; margin-bottom: .6rem;}
        .yen-cat {display: flex; align-items: center; gap: .8rem; margin: .45rem 0;
                  font-size: .9rem;}
        .yen-cat .n {flex: 0 0 38%; font-weight: 500;}
        .yen-cat .bar {flex: 1; height: 9px; border-radius: 999px; background: #E8EDF9;
                       overflow: hidden;}
        .yen-cat .bar i {display: block; height: 100%; background: #D62839;
                         border-radius: 999px;}
        .yen-cat .v {flex: 0 0 2.6rem; text-align: right; font-weight: 600;}

        .yen-badge {display: inline-block; font-size: .72rem; font-weight: 600;
                    border-radius: 999px; padding: .2rem .65rem; margin-left: .4rem;}
        .yen-badge.good {background: #E8EDF9; color: #0B1F4B;}
        .yen-badge.bad {background: #D62839; color: #FFFFFF;}
        .yen-ans {border-left: 4px solid; border-radius: 8px; padding: .55rem .85rem;
                  margin: .4rem 0; font-size: .95rem;}
        .yen-ans small {display: block; opacity: .7; font-size: .68rem;
                        text-transform: uppercase; letter-spacing: .08em;}
        .yen-ans.good {border-color: #0B1F4B; background: #EEF2FB;}
        .yen-ans.bad {border-color: #D62839; background: #FDF1F2;}
        .yen-why {margin-top: .7rem; color: #33415F; font-size: .92rem; line-height: 1.55;}

        [data-testid="stVerticalBlockBorderWrapper"] {border-radius: 16px; border-color: #E3E7F0;
                                                       background: #FFFFFF;}
        [data-testid="stProgress"] > div > div > div > div {background-color: #D62839;}
        .yen-footer {text-align: center; color: #8A94AD; font-size: .8rem; margin-top: 2.5rem;}

        @media (max-width: 640px) {
            .block-container {padding-left: 1rem; padding-right: 1rem;}
            .yen-word {font-size: 1.4rem;}
            .yen-brand img {height: 40px; width: 40px;}
            .yen-pill {display: none;}
            .yen-hero {padding: 1.4rem 1.2rem;}
            .yen-hero-title {font-size: 1.65rem; max-width: 100%;}
            .yen-hero p {max-width: 100%;}
            .yen-q {font-size: 1.08rem;}
            .yen-cat .n {flex-basis: 45%;}
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_logo():
    """Brand header: LinguaNow icon + wordmark."""
    icon = base64.b64encode(LOGO_ICON_SVG.encode()).decode()
    st.markdown(
        f"""
        <div class="yen-brand">
            <div class="yen-brand-left">
                <img src="data:image/svg+xml;base64,{icon}" alt="LinguaNow logo">
                <span class="yen-word"><span class="lingua">Lingua</span><span class="now">Now</span></span>
            </div>
            <span class="yen-pill">{len(LANGUAGES)} languages · {len(LEVELS)} levels</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def step_title(number, text):
    st.markdown(
        f'<div class="yen-step"><span>{number}</span>{esc(text)}</div>',
        unsafe_allow_html=True,
    )


# ----------------------------------------------------------------------------
# Screens
# ----------------------------------------------------------------------------

def render_home():
    chips = "".join(f"<span>{esc(info['native'])}</span>" for info in LANGUAGES.values())
    st.markdown(
        f"""
        <div class="yen-hero">
            <div class="yen-eyebrow">Practise · Assess · Improve</div>
            <div class="yen-hero-title">Learn any language.<br><em>Right now.</em></div>
            <p>Ten questions, four choices and clear explanations. Pick a language and a
            level, and see where you stand in just a few minutes.</p>
            <div class="yen-chips">{chips}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    language = st.session_state.language
    languages = list(LANGUAGES)
    step_title(1, "Choose a language")
    with st.container(key="lang_picker"):
        st.radio(
            "Language",
            languages,
            index=languages.index(language),
            key="home_language",
            horizontal=True,
            on_change=set_language,
            format_func=lambda name: LANGUAGES[name]["native"],
            label_visibility="collapsed",
        )

    levels = list(LEVELS)
    step_title(2, "Choose your level")
    st.radio(
        "Level",
        levels,
        index=levels.index(st.session_state.level),
        key="home_level",
        format_func=lambda name: f"{name}  ·  CEFR {LEVELS[name]['cefr']}",
        label_visibility="collapsed",
    )
    st.caption(LEVELS[st.session_state.home_level]["description"])

    st.write("")
    st.button("Start quiz", type="primary", key="btn_start", on_click=start_from_home)


def render_quiz():
    quiz = st.session_state.quiz
    total = len(quiz)
    current = st.session_state.current
    answers = st.session_state.answers
    q = quiz[current]
    level = st.session_state.level
    language = st.session_state.language

    st.markdown(
        f"""
        <div class="yen-chiprow">
            <span class="yen-chip navy">{esc(language)}</span>
            <span class="yen-chip">{esc(level)} · CEFR {LEVELS[level]['cefr']}</span>
            <span class="yen-chip red">Question {current + 1} / {total}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.progress(len(answers) / total, text=f"{len(answers)} of {total} answered")

    with st.container(key="qcard"):
        st.markdown(f'<span class="yen-tag">{esc(q["category"])}</span>', unsafe_allow_html=True)
        if q.get("passage"):
            st.info(q["passage"])
        st.markdown(f'<div class="yen-q">{esc(q["question"])}</div>', unsafe_allow_html=True)

        radio_key = f"radio_{st.session_state.quiz_id}_{current}"
        saved = answers.get(current)
        st.radio(
            "Choose one answer",
            q["options"],
            index=q["options"].index(saved) if saved in q["options"] else None,
            key=radio_key,
            on_change=save_answer,
            args=(current,),
            format_func=lambda option, opts=q["options"]: f"{chr(65 + opts.index(option))}.  {option}",
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

    pct = result["percentage"]
    st.markdown(
        f"""
        <div class="yen-score">
            <div class="yen-ring" style="background: conic-gradient(#D62839 {pct}%, rgba(255,255,255,.18) 0);">
                <div class="yen-ring-in">{pct}%</div>
            </div>
            <div>
                <div class="yen-eyebrow">{esc(result['language'])} · {esc(result['level'])} · CEFR {LEVELS[result['level']]['cefr']}</div>
                <h2>{esc(result['label'])}</h2>
                <p>{esc(result['message'])}</p>
                <div class="yen-score-line">{result['score']} of {result['total']} correct</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    rows = "".join(
        f'<div class="yen-cat"><span class="n">{esc(cat)}</span>'
        f'<div class="bar"><i style="width:{round(c / t * 100)}%"></i></div>'
        f'<span class="v">{c}/{t}</span></div>'
        for cat, (c, t) in sorted(result["categories"].items())
    )
    st.markdown(
        f'<div class="yen-card"><div class="yen-card-title">Performance by category</div>{rows}</div>',
        unsafe_allow_html=True,
    )

    left, right = st.columns(2)
    with left:
        st.button("New quiz (same language and level)", type="primary",
                  on_click=start_quiz, args=(result["level"],), key="btn_again")
    with right:
        st.button("Change language or level", on_click=go_home, key="btn_home")

    st.markdown('<div class="yen-step" style="margin-top:2rem"><span>✓</span>Review your answers</div>',
                unsafe_allow_html=True)
    for number, d in enumerate(result["details"], start=1):
        with st.container(border=True):
            badge = ('<span class="yen-badge good">Correct</span>' if d["is_correct"]
                     else '<span class="yen-badge bad">Incorrect</span>')
            st.markdown(
                f'<span class="yen-tag">{esc(d["category"])}</span>'
                f'<span style="margin-left:.5rem;font-weight:600">Question {number}</span>{badge}',
                unsafe_allow_html=True,
            )
            if d.get("passage"):
                st.info(d["passage"])
            st.markdown(f'<div class="yen-q" style="font-size:1.05rem">{esc(d["question"])}</div>',
                        unsafe_allow_html=True)
            if d["is_correct"]:
                st.markdown(f'<div class="yen-ans good"><small>Your answer</small>{esc(d["chosen"])}</div>',
                            unsafe_allow_html=True)
            else:
                st.markdown(
                    f'<div class="yen-ans bad"><small>Your answer</small>{esc(d["chosen"])}</div>'
                    f'<div class="yen-ans good"><small>Correct answer</small>{esc(d["correct_answer"])}</div>',
                    unsafe_allow_html=True,
                )
            st.markdown(f'<div class="yen-why"><b>Why:</b> {esc(d["explanation"])}</div>',
                        unsafe_allow_html=True)


# ----------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------

def main():
    init_state()
    st.set_page_config(page_title="LinguaNow", page_icon="💬", layout="centered")
    inject_css()
    render_logo()

    stage = st.session_state.stage
    if stage == "quiz":
        render_quiz()
    elif stage == "results":
        render_results()
    else:
        render_home()

    st.markdown('<div class="yen-footer">LinguaNow · Practise a little, every day.</div>',
                unsafe_allow_html=True)


if __name__ == "__main__":
    main()
