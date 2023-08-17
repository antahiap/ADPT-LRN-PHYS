import streamlit as st
from app.utilities import get_questions, evaluate_answer, answer_the_question

MAX_QUESTIONS = 5

@st.cache_data
def retrieve_questions():
    return get_questions()
questions = retrieve_questions()

def clear_answer():
    st.session_state.answer = ""

if "index" not in st.session_state:
    st.session_state.index = 0

st.title("Learn Data Science")
st.write("We'll start with a few questions to evalute your level")

domain = st.selectbox("Select a domain", list(questions.keys()), on_change=clear_answer)
if domain:
    # Question
    question = questions[domain][st.session_state.index]
    st.header(question)

    # Prev - Next Button
    col = st.columns((0.9, 0.1))
    if st.session_state.index > 0:
        if col[0].button("Previous"):
            clear_answer()
            st.session_state.index -= 1
    if st.session_state.index < MAX_QUESTIONS - 1:
        if col[1].button("Next"):
            clear_answer()
            st.session_state.index += 1

    # Answer
    answer = st.text_area("Answer", height=100, key="answer")
    if st.button("Show answer"):
        with st.spinner("Asking AI"):
            st.write(answer_the_question(question))
    if st.button("Grade"):
        with st.spinner("Grading your answer..."):
            st.write(evaluate_answer(question, answer))


