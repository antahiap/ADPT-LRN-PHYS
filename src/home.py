import streamlit as st
from topic_teacher import TopicTeacher

if "exercise" not in st.session_state:
    st.session_state.exercise = ""
if "course" not in st.session_state:
    st.session_state.course = ""
if "correction" not in st.session_state:
    st.session_state.correction = ""

topic = st.text_area("Topic")
llm_chain = TopicTeacher(topic)
st.subheader("Course")
if st.button("Teach Me !"):
    with st.spinner("Getting course..."):
        st.session_state.course=llm_chain.get_course()
st.write(st.session_state.course)
st.divider()

st.subheader("Exercise")
if st.button("Give me an exercise"):
    with st.spinner("Getting exercises..."):
        st.session_state.exercise = llm_chain.get_exercise()
st.write(st.session_state.exercise)
st.divider()

st.subheader("Corrected exercises")
answer = st.text_area("Answer")
if st.button("Correct exercise"):
    with st.spinner("Correcting exercises..."):
        st.session_state.correction = llm_chain.correct_exercise(st.session_state.exercise, answer)
st.write(st.session_state.correction)
