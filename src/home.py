import streamlit as st
import fitz
import re
from pathlib import Path
from PIL import Image
from explanation_gpt import ExplanationGPT
from pdf_file_reader import PDFFileReader
from constants import PAPER_PDF_PATH
from app.style import css
from mycomponent import mycomponent
from app.utilities import register_callback

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
    content = pdf_file_reader.get_text_from_json()
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

def handle_js_value():
    tooltip_info = st.session_state.js_click
    print(tooltip_info)
    if tooltip_info.get("html"):
        js_click(tooltip_info["html"], tooltip_info["column"])
    else:
        js_selection(tooltip_info["selection"])

def js_selection(selection):
    print(selection)

def js_click(keyword_html, column):
    keyword, _ = divide_keyword_explanations(keyword_html)
    if keyword:
        if column == '1':
            st.session_state.window_view[0] += 1
            st.session_state.window_view[1] += 1
        from_explanation_idx = st.session_state.window_view[0]
        from_explanation_gpt = st.session_state.explanation_gpts[from_explanation_idx]
        st.session_state.explanation_gpts[st.session_state.window_view[1]] = from_explanation_gpt.keywords_explanations[keyword]
        st.session_state.explanation_gpts[st.session_state.window_view[1] + 1] = None
        update_buttons_disabled()

def left_button_click():
    st.session_state.window_view[0] -= 1
    st.session_state.window_view[1] -= 1
    update_buttons_disabled()

def right_button_click():
    st.session_state.window_view[0] += 1
    st.session_state.window_view[1] += 1
    update_buttons_disabled()

def update_buttons_disabled():
    st.session_state.left_button_disabled = st.session_state.window_view[0] == 0
    st.session_state.right_button_disabled = st.session_state.explanation_gpts[st.session_state.window_view[1] + 1] == None

def write_buttons():
    col1, col2 = st.columns(2)
    with col1:
        st.button("<", disabled=st.session_state.left_button_disabled, on_click=left_button_click)
    with col2:
        _, sub_col2 = st.columns([0.9, 0.1])
        sub_col2.button("\>", disabled=st.session_state.right_button_disabled, on_click=right_button_click)

def init_paper():
    with st.spinner("Generating explanation..."):
        st.session_state.window_view = [0, 1]
        st.session_state.explanation_gpts = [None] * 100
        st.session_state.explanation_gpts[0] = get_paper_explanation(PAPER_PDF_PATH / paper_pdf.name)

st.set_page_config(page_title="Home", page_icon=":house:", layout="wide")
st.markdown(css, unsafe_allow_html=True)

state_to_init = [
    ("keyword_html", None),
    ("explanation_gpts", [None] * 100),
    ("window_view", [0, 1]),
    ("left_button_disabled", True),
    ("right_button_disabled", True)
]
for key, value in state_to_init:
    if key not in st.session_state:
        st.session_state[key] = value

paper_pdf = upload_pdf()
if paper_pdf:
    tab1, tab2 = st.tabs(["Explanation", "Paper"])
    with tab1:
        if not st.session_state.explanation_gpts[0] or st.session_state.explanation_gpts[0].topic != Path(paper_pdf.name).stem:
            init_paper()
        write_buttons()
        col1, col2 = st.columns(2)
        with col1:
            write_explanation(0)
        with col2:
            write_explanation(1)
            register_callback("js_click", handle_js_value)
            mycomponent(key="js_click")
            
    with tab2:
        write_pdf(PAPER_PDF_PATH / paper_pdf.name)


