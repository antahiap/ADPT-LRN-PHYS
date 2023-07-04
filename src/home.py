import streamlit as st
from llm_chain import LlmChain


topic = st.text_area("Topic")
if st.button("Get knowledge"):
    llm_chain = LlmChain(topic)
    with st.spinner("Getting course..."):
        st.write(llm_chain.get_course())
    with st.spinner("Getting exercises..."):
        st.write(llm_chain.get_exercises())
    with st.spinner("Correcting exercises..."):
        st.write(llm_chain.correct_exercises())
