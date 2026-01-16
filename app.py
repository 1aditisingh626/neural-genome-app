import streamlit as st
import pandas as pd
import plotly.express as px
import random

# ==================================================
# PAGE CONFIG
# ==================================================
st.set_page_config(
    page_title="Neural Genome | Cognitive Signals",
    page_icon="🧬",
    layout="wide"
)

# ==================================================
# THEME COLORS
# ==================================================
bg_main = "#eef2ff"
accent = "#4f46e5"
text_color = "#1e293b"
soft_card = "#ffffff"

# ==================================================
# CSS
# ==================================================
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&display=swap');

[data-testid="stSidebar"] {{
    display: none;
}}

.block-container {{
    max-width: 900px;
    padding-top: 2rem;
    padding-bottom: 3rem;
    margin: auto;
}}

body {{
    background-color: {bg_main};
    color: {text_color};
    font-family: 'Space Grotesk', sans-serif;
}}

.title {{
    font-size: 3rem;
    font-weight: 800;
    text-align: center;
    background: linear-gradient(90deg, {accent}, #6366f1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}}

.subtitle {{
    text-align: center;
    opacity: 0.7;
    margin-bottom: 2.5rem;
}}

.card {{
    background: {soft_card};
    padding: 1.8rem;
    border-radius: 16px;
    box-shadow: 0 20px 40px rgba(0,0,0,0.05);
    margin-bottom: 2rem;
}}

.trait {{
    font-size: 0.9rem;
    color: {accent};
    margin-bottom: 1rem;
}}

.stButton>button {{
    background: {accent} !important;
    color: white !important;
    border-radius: 999px !important;
    padding: 0.7rem 2.5rem !important;
    font-weight: 600;
}}
</style>
""", unsafe_allow_html=True)

# ==================================================
# QUESTIONS
# ==================================================
questions = {
    "Openness": {
        "question": "When you hear a completely new idea, what do you usually do?",
        "options": {
            "Ignore it": 1,
            "Think about it a little": 3,
            "Explore it deeply": 7
        }
    },
    "Conscientiousness": {
        "question": "How do you usually handle long or difficult tasks?",
        "options": {
            "I avoid or delay them": 1,
            "I try but lose consistency": 4,
            "I plan and finish them properly": 7
        }
    },
    "Extraversion": {
        "question": "In group situations, what feels most natural to you?",
        "options": {
            "Stay quiet and observe": 2,
            "Speak when needed": 4,
            "Lead or energize the group": 7
        }
    },
    "Agreeableness": {
        "question": "When someone disagrees with you strongly, what do you do?",
        "options": {
            "Defend your point strongly": 2,
            "Listen but stay neutral": 4,
            "Try to maintain harmony": 7
        }
    },
    "Neuroticism": {
        "question": "When something unexpected happens, how do you react emotionally?",
        "options": {
            "I stay calm": 2,
            "I feel some stress": 4,
            "I overthink or worry a lot": 7
        }
    }
}

trait_info = {
    "Openness": "Curiosity • Imagination",
    "Conscientiousness": "Discipline • Structure",
    "Extraversion": "Energy • Social Drive",
    "Agreeableness": "Empathy • Cooperation",
    "Neuroticism": "Emotional Sensitivity"
}

# ==================================================
# SESSION STATE
# ==================================================
if "step" not in st.session_state:
    st.session_state.step = 0
if "scores" not in st.session_state:
    st.session_state.scores = {}

traits = list(questions.keys())

# ==================================================
# HEADER
# ==================================================
st.markdown("<div class='title'>NEURAL GENOME</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Cognitive Signal Extraction Interface</div>", unsafe_allow_html=True)

# ==================================================
# QUESTION FLOW
# ==================================================
if st.session_state.step < len(traits):
    trait = traits[st.session_state.step]
    q = questions[trait]

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown(f"### Signal {st.session_state.step + 1} of 5")
    st.markdown(f"**{q['question']}**")
    st.markdown(f"<div class='trait'>{trait_info[trait]}</div>", unsafe_allow_html=True)

    option = st.radio("Choose one:", list(q["options"].keys()))

    if st.button("ENCODE RESPONSE"):
        st.session_state.scores[trait] = q["options"][option]
        st.session_state.step += 1
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)

# ==================================================
# RESULTS
# ==================================================
else:
    percentages = {k: round((v / 7) * 100) for k, v in st.session_state.scores.items()}

    st.markdown("## 🧬 Cognitive Signal Map")

    df = pd.DataFrame(dict(r=percentages.values(), theta=percentages.keys()))
    fig = px.line_polar(df, r="r", theta="theta", line_close=True)
    fig.update_traces(fill="toself", line_color=accent)
    fig.update_layout(
        polar=dict(radialaxis=dict(visible=False)),
        paper_bgcolor="rgba(0,0,0,0)",
        height=420
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("## 🔍 Neural Insights (What Your Results Mean)")

    for trait, score in sorted(percentages.items(), key=lambda x: -x[1]):
        st.markdown(f"### {trait} — {score}%")
        st.progress(score / 100)

        if score >= 70:
            level = "HIGH"
        elif score >= 40:
            level = "MODERATE"
        else:
            level = "LOW"

        explanations = {
            "Openness": {
                "HIGH": "You enjoy new ideas, creativity, and exploring different ways of thinking.",
                "MODERATE": "You like new ideas sometimes but prefer familiar approaches.",
                "LOW": "You prefer routine and proven methods."
            },
            "Conscientiousness": {
                "HIGH": "You are disciplined, organized, and goal-focused.",
                "MODERATE": "You try to stay organized but struggle sometimes.",
                "LOW": "You prefer flexibility over strict planning."
            },
            "Extraversion": {
                "HIGH": "You gain energy from social interaction.",
                "MODERATE": "You balance social and alone time well.",
                "LOW": "You prefer quiet environments."
            },
            "Agreeableness": {
                "HIGH": "You value harmony and empathy.",
                "MODERATE": "You are kind but assertive when needed.",
                "LOW": "You prioritize logic over emotions."
            },
            "Neuroticism": {
                "HIGH": "You experience emotions strongly and may overthink.",
                "MODERATE": "You feel stress but manage it.",
                "LOW": "You remain calm under pressure."
            }
        }

        st.markdown(f"🧠 **Signal Level:** {level}")
        st.markdown(f"*{explanations[trait][level]}*")

    st.info(
        "This is not a fixed personality. It reflects your current thinking tendencies."
    )

    if st.button("RECALIBRATE GENOME"):
        st.session_state.clear()
        st.rerun()

# ==================================================
# FOOTER
# ==================================================
st.markdown(
    "<p style='text-align:center;opacity:0.4;margin-top:2rem;'>Neural Genome Engine • 2026</p>",
    unsafe_allow_html=True
)
