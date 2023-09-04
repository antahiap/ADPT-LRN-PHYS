import streamlit as st
import fitz
from PIL import Image
from paper_gpt import PaperGPT
from pdf_file_reader import PDFFileReader
from constants import PAPER_PDF_PATH, PAPER_TXT_PATH
from app.style import css

def write_pdf(pdf_file_path):
    doc = fitz.open(pdf_file_path)
    image_list = []
    for page_number in range(doc.page_count):
        page = doc.load_page(page_number)
        pix = page.get_pixmap(dpi=300)  # scale up the image resolution
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        image_list.append(img)
    st.image(image_list)

def write_summary(pdf_file_name):
    pdf_file_reader = PDFFileReader(pdf_file_name)
    pdf_file_reader.read_pdf()
    content = open(pdf_file_reader.get_text_path(), "r").read()
    paper = PaperGPT(content, pdf_file_name)
    # paper.summary = "The paper introduces the Transformer , a new network architecture based solely on attention mechanisms for sequence transduction tasks. The Transformer removes the need for recurrent or convolutional layers typically used in encoder-decoder models, and instead connects the encoder and decoder with attention mechanisms. The model achieves superior results in terms of translation quality, parallelization, and training time on two machine translation tasks. It also generalizes well to other tasks, such as English constituency parsing. The authors provide detailed experimental results and variations of the model to evaluate the importance of different components."
    # paper.keywords = ['Transformer', 'attention mechanisms', 'sequence transduction tasks', 'recurrent', 'convolutional layers', 'encoder-decoder models', 'translation quality', 'machine translation tasks', 'English constituency parsing', 'experimental results', 'importance of different components']
    # paper.keywords_explanations = {'English constituency parsing': 'English constituency parsing is a task in natural language processing that involves identifying the syntactic structure of sentences and dividing them into constituent phrases. The paper mentions that the Transformer, a network architecture based on attention mechanisms, performs well in English constituency parsing along with other tasks.', 'attention mechanisms': 'Attention mechanisms are a key part of the Transformer network architecture. They allow the model to focus on different parts of the input sequence when generating an output sequence. This removes the need for recurrent or convolutional layers and improves translation quality, parallelization, and training time. The effectiveness of attention mechanisms is demonstrated through detailed experiments and variations of the model.', 'translation quality': "Translation quality refers to the level of accuracy and fluency in the translated output. In the context of the paper, the authors introduce a new network architecture called the Transformer, which achieves superior translation quality compared to traditional models. They achieve this by using attention mechanisms to connect the encoder and decoder, eliminating the need for recurrent or convolutional layers. The model's translation quality is evaluated through experimental results and comparisons with other models.", 'convolutional layers': 'Convolutional layers are a type of layer used in convolutional neural networks (CNNs) that apply filters or kernels to input data in order to extract features. These layers are commonly used in computer vision tasks for analyzing images or sequences of data. They allow the network to detect patterns and spatial relationships in the data by convolving the input with different filters and pooling the results. This helps in capturing local patterns and learning hierarchical representations of the input data.', 'experimental results': 'Experimental results refer to the outcomes obtained by conducting experiments to evaluate the performance and effectiveness of a particular model or approach. In the context of the paper explaining the Transformer network architecture, the experimental results would include the findings and measurements derived from testing the model on various tasks, such as machine translation and English parsing. These results demonstrate the superiority of the Transformer in terms of translation quality, parallelization, training time, and its ability to generalize to different tasks. The authors further provide variations of the model and conduct experiments to analyze and determine the significance of different components within the Transformer.', 'Transformer': 'In simple terms, the Transformer is a new type of network architecture that uses attention mechanisms to perform tasks involving sequences of data. It replaces the traditional recurrent or convolutional layers used in encoder-decoder models and connects the encoder and decoder with attention mechanisms instead. The Transformer has been shown to achieve excellent results in machine translation tasks, offering advantages in translation quality, parallelization, and training time. It also performs well on other tasks, like English parsing. The authors back up their claims with detailed experiments and variations of the model to assess the significance of various components.', 'recurrent': 'In the context of neural networks, "recurrent" refers to a specific type of layer or architecture that is commonly used for sequence transduction tasks. Recurrent layers are designed to process sequential data by allowing information to be passed from one step to the next, making them suitable for tasks like natural language processing or speech recognition. However, the Transformer network, introduced in the paper, does not rely on recurrent layers. Instead, it utilizes attention mechanisms to connect the encoder and decoder, which leads to improved translation quality, parallelization capabilities, and faster training time. The Transformer model also demonstrates good performance on various tasks beyond machine translation.', 'sequence transduction tasks': 'Sequence transduction tasks refer to tasks where a sequence of input elements is transformed into a sequence of output elements. The Transformer network architecture, introduced in the paper, is specifically designed for these tasks. Unlike traditional encoder-decoder models that use recurrent or convolutional layers, the Transformer uses attention mechanisms to connect the encoder and decoder. This eliminates the need for sequential processing and allows for better translation quality, faster parallelization, and reduced training time. The Transformer model also performs well on other tasks, such as English constituency parsing, and the authors provide extensive experimental results to analyze the impact of different components of the model.', 'machine translation tasks': 'Machine translation tasks refer to the process of automatically translating text or speech from one language to another using computational techniques. The Transformer is a network architecture that improves the quality, efficiency, and training time of machine translation. It replaces traditional recurrent or convolutional layers in encoder-decoder models with attention mechanisms, which connect the encoder and decoder. The Transformer achieves superior translation quality, parallelization, and training time on two specific machine translation tasks. Furthermore, it can effectively handle other tasks, such as English constituency parsing. The authors of the paper provide comprehensive experimental results and variations of the model to assess the significance of various components.', 'encoder-decoder models': 'Encoder-decoder models are a type of neural network architecture commonly used in sequence transduction tasks, such as machine translation. These models consist of an encoder and a decoder. The encoder processes the input sequence and converts it into a fixed-length representation, while the decoder generates the output sequence based on this representation. In traditional encoder-decoder models, recurrent or convolutional layers are used for encoding and decoding. However, the Transformer architecture introduced in the paper removes the need for these layers and instead uses attention mechanisms to connect the encoder and decoder. This results in improved translation quality, faster training time, and better parallelization. The Transformer model can also be applied to other tasks and exhibits good generalization. The paper provides detailed experimental results and explores various variations of the model to analyze the importance of different components.', 'importance of different components': 'The different components in the Transformer network architecture play a crucial role in achieving superior results in sequence transduction tasks. By using attention mechanisms instead of recurrent or convolutional layers, the need for complex computations is reduced, resulting in improved translation quality, parallelization, and reduced training time. The Transformer generalizes well to various tasks, highlighting the importance of these components in enhancing performance. The authors assess the significance of each component through detailed experimental results and variations of the model.'}
    html = paper.to_html()
    st.markdown(html, unsafe_allow_html=True)

def upload_pdf():
    paper_pdf = st.file_uploader("Upload your paper", type="pdf")
    if paper_pdf:
        with open(PAPER_PDF_PATH / paper_pdf.name, "wb") as f:
            f.write(paper_pdf.getbuffer())
        st.success("Uploaded successfully!")
    return paper_pdf

st.set_page_config(page_title="Home", page_icon=":house:", layout="wide")
st.markdown(css, unsafe_allow_html=True)


paper_pdf = upload_pdf()
if paper_pdf:
    tab1, tab2 = st.tabs(["Explanation", "Paper"])
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            with st.spinner("Generating explanation..."):
                write_summary(PAPER_PDF_PATH / paper_pdf.name)
        with col2:
            pass
    with tab2:
        write_pdf(PAPER_PDF_PATH / paper_pdf.name)


