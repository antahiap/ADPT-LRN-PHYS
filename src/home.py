import streamlit as st
import fitz
import re
from pathlib import Path
from PIL import Image
from explanation_gpt import ExplanationGPT
from explain_paper import ExplainPaper
from pdf_file_reader import PDFFileReader
from constants import PAPER_PDF_PATH, PAPER_REF_PATH
from app.style import css
from mycomponent import mycomponent
from app.utilities import register_callback
import app.style as style
from mycomponent import mycomponent
from netcomponent import netcomponent
from streamlit.components.v1 import html

from network_vis import VisNetwork
from network_prmpt import NetworkPrmpt
import streamlit.components.v1 as components
import time

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
        if index > 0:
            st.subheader(explanation_gpt.topic.title())
        st.markdown(html, unsafe_allow_html=True)

def upload_pdf():
    paper_pdf = st.file_uploader("Upload your paper", type="pdf")
    if paper_pdf:
        with open(PAPER_PDF_PATH / paper_pdf.name, "wb") as f:
            f.write(paper_pdf.getbuffer())


        pdf_stem = paper_pdf.name.split('.pdf')[0]
        if not st.session_state.pdfs:
            st.session_state.pdfs = [pdf_stem]
        else:
            if not pdf_stem in st.session_state.pdfs:
                st.session_state.pdfs.append(pdf_stem)
    return paper_pdf

def divide_keyword_explanations(html):
    match = re.search(r'(.*?)<span class="tooltiptext">(.*?)</span>', html, re.DOTALL)
    return match.groups() if match else (None, None)

def handle_js_click():
    tooltip_info = mycomponent()
    if tooltip_info:
        print(tooltip_info)
        keyword_html, column = tooltip_info.values()
        keyword, _ = divide_keyword_explanations(keyword_html)
        print(keyword)
        if keyword:
            print(column)
            if column == '1':
                st.session_state.window_view[0] += 1
                st.session_state.window_view[1] += 1
            from_explanation_idx = st.session_state.window_view[0]
            from_explanation_gpt = st.session_state.explanation_gpts[from_explanation_idx]
            st.session_state.explanation_gpts[st.session_state.window_view[1]] = from_explanation_gpt.keywords_explanations[keyword]

def get_network():

    papers = [ "2308.16622", "1706.03762", "1308.0850", "2308.16441", '1609.08144', '1607.06450']
    papers = [ "1706.03762"] #, '1703.03130', '1608.05859', '1703.10722', '1508.04025', '1601.06733', '1705.04304', '1610.02357', '1610.10099', '1705.03122', '1508.07909', '1607.06450',  '1609.08144', ]# '1701.06538',

    if not st.session_state.pdfs:
        nodes= None
        edges = None
        nodes2 = None
        edges2 = None
    
    else: 
        papers = st.session_state.pdfs

        st.sidebar.title("Tools")
        th = st.sidebar.slider('Simillarity threshhold', 0.7, 1.0, .87)
        st.sidebar.button('References')
        selected_paper = st.sidebar.multiselect("Loaded papers:", papers + ['All'], papers)

        ref_selected = st.sidebar.selectbox("Select a paper to load references:", ['Nothing selected'] + papers)

        if not selected_paper:
            nodes = None
            edges = None
            nodes2 = None
            edges2 = None
        
        else:
            if 'All' in selected_paper:
                selected_paper = papers

            g = VisNetwork()
            G_data = g.json_network(th, PAPER_PDF_PATH, selected_paper)
            nodes=G_data['nodes']
            edges=G_data['edges']
            
            if not ref_selected == 'Nothing selected':

                pdf_src =PDFFileReader(PAPER_PDF_PATH / Path(ref_selected + '.pdf'))
                text_dic = pdf_src.read_pdf()
                ref_paper = [ref_selected] + pdf_src.list_reference(text_dic[-2]['references'])
                
                g_ref = VisNetwork()
                G_data_ref = g_ref.json_network(th, PAPER_REF_PATH, ref_paper)
                
                nodes=G_data_ref['nodes']
                edges=G_data_ref['edges']

            if st.session_state.net_info:

                nodes2=st.session_state.nodes2
                edges2=st.session_state.edges2

            else:
                nodes2 = None
                edges2 = None

    net_info = netcomponent(nodes=nodes, edges=edges, nodes2=nodes2, edges2=edges2 )

    if net_info:
        st.session_state.net_info = net_info

        src, dst = net_info.values()
        nt_prmpt = NetworkPrmpt(G_data)
        with st.spinner('Wait for it...'):
            g_prmpt = nt_prmpt.diff_paper(src, dst)

            g_zoom = VisNetwork()
            G_zoom_data = g_zoom.json_network(None, None, None, G=g_prmpt)
            st.session_state.nodes2=G_zoom_data['nodes']
            st.session_state.edges2=G_zoom_data['edges']

        st.experimental_rerun()
        
def get_paper_explanation(pdf_file_name):
    explanation_gpt = ExplanationGPT(pdf_file_name.stem)
    explanation_gpt.fill_from_db()
    if not explanation_gpt.explanation:
        pdf_file_reader = PDFFileReader(pdf_file_name)
        paper_json = pdf_file_reader.read_pdf()
        # paper_json = pdf_file_reader.get_json()
        explain_paper = ExplainPaper(pdf_file_name.stem, paper_json)
        explain_paper.generate_explanation()
        explanation_gpt.set_explanation(explain_paper.explanation)
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

def divide_keyword_explanations(html):
    match = re.search(r'(.*?)<span class="tooltiptext">(.*?)</span>', html, re.DOTALL)
    return match.groups() if match else (None, None)

def handle_js_value():
    tooltip_info = st.session_state.js_click
    print(tooltip_info)
    if tooltip_info.get("html"):
        js_click(tooltip_info["html"], tooltip_info["column"])
    else:
        js_selection(tooltip_info["selection"], tooltip_info["column"])

def js_selection(keyword, column):
    if keyword:
        if column == 1:
            st.session_state.window_view[0] += 1
            st.session_state.window_view[1] += 1
        from_explanation_idx = st.session_state.window_view[0]
        from_explanation_gpt = st.session_state.explanation_gpts[from_explanation_idx]
        from_explanation_gpt.add_keyword_explanation(keyword)
        st.session_state.explanation_gpts[st.session_state.window_view[1]] = from_explanation_gpt.keywords_explanations[keyword]
        st.session_state.explanation_gpts[st.session_state.window_view[1] + 1] = None
        update_buttons_disabled()
    
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
    ("right_button_disabled", True),
    ("selected_edge", None),
    ("net_info", None),
    ("nodes1", None),
    ("edges1", None),
    ("nodes2", None),
    ("edges2", None),
    ("pdfs", None)
]
for key, value in state_to_init:
    if key not in st.session_state:
        st.session_state[key] = value

paper_pdf = upload_pdf()

tab1, tab2, tab3= st.tabs(["Network", "Explanation", "Paper"])
with tab1:
    get_network()

if paper_pdf:
    with tab2:
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
    with tab3:
        write_pdf(PAPER_PDF_PATH / paper_pdf.name)




