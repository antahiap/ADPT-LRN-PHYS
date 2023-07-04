import streamlit as st
from llm_chain import LlmChain


topic = st.text_area("Topic")
if st.button("Get knowledge"):
    llm_chain = LlmChain(topic)
    st.subheader("Course")
    with st.spinner("Getting course..."):
        st.write(llm_chain.get_course())
    st.divider()
    st.subheader("Exercises")
    with st.spinner("Getting exercises..."):
        st.write(llm_chain.get_exercises())
    st.divider()
    st.subheader("Corrected exercises")
    with st.spinner("Correcting exercises..."):
        st.write(llm_chain.correct_exercises())
