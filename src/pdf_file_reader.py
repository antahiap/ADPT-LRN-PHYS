from PyPDF2 import PdfReader
import json
import glob
import os
import re
from pathlib import Path
from constants import PAPER_IMG_PATH, PAPER_TXT_PATH


class PDFFileReader():
    def __init__(self, 
                 pdf_file_path, 
                 write_json=False,
                 write_text=False
                 ):
        self.pdf_file_path = pdf_file_path
        self.pdf_file_name = pdf_file_path.stem
        self.write_json = write_json
        self.write_text = write_text

    def batch_read_pdf(self, src_dir):
        pdf_list = glob.glob(os.path.join(src_dir, '*.pdf'))

        for self.pdf_file_path in pdf_list:
            input(self.pdf_file_path)
            pdf_file_name = os.path.basename(self.pdf_file_path)
            self.pdf_file_name, _ = os.path.splitext(pdf_file_name)

            self.pdf_reader = PdfReader(open(self.pdf_file_path, 'rb'))
            self.num_pages = len(self.pdf_reader.pages)

            self.pdf_img()
            self.pdf_to_txt()
    
    def read_pdf(self):
        pdf_file = open(self.pdf_file_path, 'rb')
        self.pdf_reader = PdfReader(pdf_file)
        self.num_pages = len(self.pdf_reader.pages)

        self.pdf_img()
        txt_dic = self.pdf_to_txt()
        return txt_dic
    
    def pdf_img(self):
        for page_number in range(self.num_pages):
            page = self.pdf_reader.pages[page_number]
            count = 0
            for image_file_object in page.images:
                img_path = PAPER_IMG_PATH / f'{self.pdf_file_name}_{count}_{image_file_object.name}'
                with open(img_path,  "wb") as fp:
                    fp.write(image_file_object.data)
                    count += 1
                
    def split_sections(self):

        def overlap_matches(pattern, text):
            offset = 0
            matches = []

            while True:
                # Search for matches starting from the current offset
                match = re.search(pattern, text[offset:])

                if not match:
                    break
                
                # Get the matched substring and add it to the list of matches
                matches.append(match.group(1))

                # Update the offset to search for the next match
                offset += match.start() + 1
            return(matches)

        def get_text(matches, text):
            text_sec = []
            for i in range(len(matches)):
                start = matches_1[i]

                if i==len(matches_1)-1:
                    end = 'Reference'
                else:
                    end = matches_1[i+1]

                text_i = text.split(start)[1].split(end)
                text_i = text_i[0]
                text_sec.append(text_i.strip())

            return(text_sec)
        
        # Get Abstract
        pattern_0 = r'(Abstract)\n'
        abstract = re.findall(pattern_0, self.text, flags= re.DOTALL | re.IGNORECASE)
        
        # match section headings with the numaber
        pattern_1 =  r'\n(\d\.?\d?\.?\d?\.? [A-Z].+)\n'
        matches_1 = abstract + overlap_matches(pattern_1, self.text) 
        
        # get the text of each section
        text_sec = get_text(matches_1, self.text)

        # match section headings splited numaber
        pattern_2 =  r'(\d\.?\d?\.?\d?\.?) ([A-Z][\-A-Za-z *]+)'

        missing = []
        pdf_strcture = []
        for mi, match in enumerate(matches_1):

            try:
                match_split = re.findall(pattern_2, match, re.DOTALL)[0]
                section_number = match_split[0].strip('.').split('.')
                section_name = match_split[1]
                id = match_split[0]

                pos = [None for x in section_number]
                for j in range(len(section_number)):
                    pos[j] = int(section_number[j]) -1

            except IndexError:
                section_name = match
                text_sec[mi] = re.findall(
                    r'([A-Za-z0-9 \n\.\-\,\;\(\)]+)', text_sec[mi])[0]
                pos = [0]
                id = ''


            json_tmplt = {
                    'id': id,
                    'section': section_name,
                    'text': text_sec[mi],
                    'subsection': []
                }
            
            
            if len(pos) == 1:
                pdf_strcture.append(json_tmplt)
            elif len(pos) == 2:
                pdf_strcture[pos[0]]['subsection'].append(json_tmplt)  
            elif len(pos) == 3:
                pdf_strcture[pos[0]]['subsection'][pos[1]]['subsection'].append(json_tmplt)                
            elif len(pos) == 4:
                pdf_strcture[pos[0]]['subsection'][pos[1]]['subsection'].append(json_tmplt)  
            else:
                missing.append(json_tmplt)

        out_data = pdf_strcture + [{'missing': missing}]
        out_data = out_data + [{'title': self.title}]

        file_path = PAPER_TXT_PATH / f'{self.pdf_file_name}.json'
        if self.write_json:
            with open(file_path, 'w', encoding='utf-8') as json_file:
                json.dump(out_data, json_file, indent=4) 
        
        return out_data

    def pdf_to_txt(self):
        text = ""
        TITLE =[]

        def visitor_body(text, cm, tm, fontDict, fontSize):
            y = tm[5]
            x = tm[4]
            title=[]

            if y > 40 and y < 800:
                if x > 35 and x <1000:
                    parts.append(text)

                    if fontSize >15 and fontSize<20:
                        TITLE.append(text) #.strip())
        
        for page_num in range(self.num_pages):
            parts = []

            page = self.pdf_reader.pages[page_num]  #pdf_reader.getPage(page_num)
            page.extract_text(
                visitor_text=visitor_body)

            # remove page number
            if not parts[-1].endswith('\n'): parts= parts[:-1]
            text += "".join(parts)
        
        self.text = text
        self.title=''.join(TITLE)
        content_dic = self.split_sections()

        txt_path = self.get_text_path()
        if self.write_text:
            with open(txt_path, "w", encoding="utf-8") as output_file:
                output_file.write(text)
        return(content_dic)

    def get_text_path(self):
        return PAPER_TXT_PATH / f"{self.pdf_file_name}.txt"
    
    def get_json(self):
        with open(PAPER_TXT_PATH / f'{self.pdf_file_name}.json', 'r') as f:
            data = json.load(f)
        return data

if __name__ == '__main__':
    pdf_src =PDFFileReader(Path("data/article_pdf/1706.03762.pdf"))
    # pdf_src.batch_read_pdf('data/article_pdf/')
    pdf_src.read_pdf()
