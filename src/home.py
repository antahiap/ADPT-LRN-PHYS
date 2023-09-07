import streamlit as st
from streamlit import session_state as _state
from streamlit.components.v1 import components as _components
import fitz
import re
from pathlib import Path
from PIL import Image
from explanation_gpt import ExplanationGPT
from pdf_file_reader import PDFFileReader
from constants import PAPER_PDF_PATH, PAPER_TXT_PATH
from app.style import css
from mycomponent import mycomponent

def _patch_register_widget(register_widget):
    def wrapper_register_widget(*args, **kwargs):
        user_key = kwargs.get("user_key", None)
        callbacks = _state.get("_components_callbacks", None)

        # Check if a callback was registered for that user_key.
        if user_key and callbacks and user_key in callbacks:
            callback = callbacks[user_key]

            # Add callback-specific args for the real register_widget function.
            kwargs["on_change_handler"] = callback[0]
            kwargs["args"] = callback[1]
            kwargs["kwargs"] = callback[2]

        # Call the original function with updated kwargs.
        return register_widget(*args, **kwargs)

    return wrapper_register_widget


# Patch function only once.
if not hasattr(_components.register_widget, "__callbacks_patched__"):
    setattr(_components.register_widget, "__callbacks_patched__", True)
    _components.register_widget = _patch_register_widget(_components.register_widget)


def register_callback(element_key, callback, *callback_args, **callback_kwargs):
    # Initialize callbacks store.
    if "_components_callbacks" not in _state:
        _state._components_callbacks = {}

    # Register a callback for a given element_key.
    _state._components_callbacks[element_key] = (callback, callback_args, callback_kwargs)

def write_pdf(pdf_file_path):
    doc = fitz.open(pdf_file_path)
    image_list = []
    for page_number in range(doc.page_count):
        page = doc.load_page(page_number)
        pix = page.get_pixmap(dpi=300)  # scale up the image resolution
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        image_list.append(img)
    st.image(image_list)

def get_paper_explanation(pdf_file_name):
    pdf_file_reader = PDFFileReader(pdf_file_name)
    pdf_file_reader.read_pdf()
    content = open(pdf_file_reader.get_text_path(), "r").read()
    explanation_gpt = ExplanationGPT(pdf_file_name.stem, context=content)
    explanation_gpt.generate_info()
    return explanation_gpt

def add_column_to_tooltip(html, column_id):
    return html.replace('<span class="tooltip">', f'<span class="tooltip" column-id="{column_id}">')

def write_explanation(index):
    explanation_idx = st.session_state.window_view[index]
    explanation_gpt = st.session_state.explanation_gpts[explanation_idx]
    if explanation_gpt:
        if not explanation_gpt.html:
            with st.spinner("Generating explanation..."):
                explanation_gpt.generate_info()
        html = explanation_gpt.html
        html = add_column_to_tooltip(html, index)
        st.subheader(explanation_gpt.topic.title())
        st.markdown(html, unsafe_allow_html=True)

def upload_pdf():
    paper_pdf = st.file_uploader("Upload your paper", type="pdf")
    if paper_pdf:
        with open(PAPER_PDF_PATH / paper_pdf.name, "wb") as f:
            f.write(paper_pdf.getbuffer())
    return paper_pdf

def divide_keyword_explanations(html):
    match = re.search(r'(.*?)<span class="tooltiptext">(.*?)</span>', html, re.DOTALL)
    return match.groups() if match else (None, None)

def handle_js_click():
    tooltip_info = st.session_state.js_click
    print(tooltip_info)
    if tooltip_info:
        keyword_html, column = tooltip_info.values()
        keyword, _ = divide_keyword_explanations(keyword_html)
        if keyword:
            if column == '1':
                st.session_state.window_view[0] += 1
                st.session_state.window_view[1] += 1
            from_explanation_idx = st.session_state.window_view[0]
            from_explanation_gpt = st.session_state.explanation_gpts[from_explanation_idx]
            st.session_state.explanation_gpts[st.session_state.window_view[1]] = from_explanation_gpt.keywords_explanations[keyword]
            st.experimental_rerun()

def init_paper():
    with st.spinner("Generating explanation..."):
        st.session_state.window_view = [0, 1]
        st.session_state.explanation_gpts = [None] * 5
        st.session_state.explanation_gpts[0] = get_paper_explanation(PAPER_PDF_PATH / paper_pdf.name)


st.set_page_config(page_title="Home", page_icon=":house:", layout="wide")
st.markdown(css, unsafe_allow_html=True)


if 'keyword_html' not in st.session_state:
    st.session_state.keyword_html = None
if "explanation_gpts" not in st.session_state:
    st.session_state.explanation_gpts = [None] * 5
if "window_view" not in st.session_state:
    st.session_state.window_view = [0, 1]

paper_pdf = upload_pdf()
if paper_pdf:
    tab1, tab2 = st.tabs(["Explanation", "Paper"])
    with tab1:
        if not st.session_state.explanation_gpts[0] or st.session_state.explanation_gpts[0].topic != Path(paper_pdf.name).stem:
            init_paper()
        col1, col2 = st.columns(2)
        with col1:
            if st.button("<"):
                st.session_state.window_view[0] -= 1
                st.session_state.window_view[1] -= 1
                st.experimental_rerun()
            write_explanation(0)
        with col2:
            sub_col1, sub_col2 = st.columns([0.9, 0.1])
            if sub_col2.button("\>"):
                st.session_state.window_view[0] += 1
                st.session_state.window_view[1] += 1
                st.experimental_rerun()
            write_explanation(1)
        register_callback("js_click", handle_js_click)
        mycomponent(key="js_click")
            
    with tab2:
        write_pdf(PAPER_PDF_PATH / paper_pdf.name)
