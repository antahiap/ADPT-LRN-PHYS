import streamlit as st
from app.utilities import get_questions, evaluate_answer

MAX_QUESTIONS = 5

@st.cache_data
def retrieve_questions():
    return get_questions()
questions = retrieve_questions()

if "index" not in st.session_state:
    st.session_state.index = 0

st.title("Learn Data Science")
st.write("We'll start with a few questions to evalute your level")

domain = st.selectbox("Select a domain", list(questions.keys()))
if domain:
    # Question
    question = questions[domain][st.session_state.index]
    st.header(question)

    # Prev - Next Button
    col = st.columns((0.9, 0.1))
    if st.session_state.index > 0:
        if col[0].button("Previous"):
            st.session_state.index -= 1
    if st.session_state.index < MAX_QUESTIONS - 1:
        if col[1].button("Next"):
            st.session_state.index += 1

    # Answer
    answer = st.text_area("Answer", height=100)
    if answer:
        with st.spinner("Grading your answer..."):
            st.write(evaluate_answer(question, answer))


