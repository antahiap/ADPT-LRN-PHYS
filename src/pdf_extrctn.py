from PyPDF2 import PdfReader
import json
import glob
import os
import re


class PDFFileReader():

    def __init__(self):

        self.src_dir = 'data/article_pdf'
        self.dst_txt = 'data/article_pdf/txt/'
        self.dst_img = 'data/article_pdf/img/'

    def read_pdf(self):

        pdf_list = glob.glob(os.path.join(self.src_dir, '*.16622.pdf'))

        for self.pdf_file_path in pdf_list:
            input(self.pdf_file_path)
            pdf_file_name = os.path.basename(self.pdf_file_path)
            self.pdf_file_name, _ = os.path.splitext(pdf_file_name)

            self.pdf_reader = PdfReader(open(self.pdf_file_path, 'rb'))
            self.num_pages = len(self.pdf_reader.pages)

            self.pdf_img()
            self.pdf_to_txt()
    
    def pdf_img(self):
        for page_number in range(self.num_pages):
            page = self.pdf_reader.pages[page_number]
            count = 0

            for image_file_object in page.images:

                img_path = f'{self.dst_img}{self.pdf_file_name}_{count}_{image_file_object.name}'
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
        
        # match section headings with the numaber
        pattern_1 =  r'\n(\d\.?\d?\.?\d?\.? [A-Z][\-A-Za-z *]+)\n'
        matches_1 = overlap_matches(pattern_1, self.text) 
        
        # get the text of each section
        text_sec = get_text(matches_1, self.text)

        # match section headings splited numaber
        pattern_2 =  r'(\d\.?\d?\.?\d?\.?) ([A-Z][\-A-Za-z *]+)'

        pdf_strcture = []
        missing = []
        for mi, match in enumerate(matches_1):
            match_split = re.findall(pattern_2, match, re.DOTALL)[0]
            section_number = match_split[0].strip('.').split('.')
            section_name = match_split[1]

            pos = [None for x in section_number]

            for j in range(len(section_number)):
                pos[j] = int(section_number[j])-1

            json_tmplt = {
                    'id': match_split[0],
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

        file_path = self.dst_txt + f'{self.pdf_file_name}.json'
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(out_data, json_file, indent=4) 

    def pdf_to_txt(self):

        text = ""

        def visitor_body(text, cm, tm, fontDict, fontSize):

            y = tm[5]
            x = tm[4]
            if y > 40 and y < 800:
                if x > 35 and x <1000:
                    parts.append(text)
        
        for page_num in range(self.num_pages):
            parts = []

            page = self.pdf_reader.pages[page_num]  #pdf_reader.getPage(page_num)
            page.extract_text(
                visitor_text=visitor_body)

            # remove page number
            if not parts[-1].endswith('\n'): parts= parts[:-1]
            text += "".join(parts)
        
        self.text = text
        content_dic = self.split_sections()

        txt_path = f"{self.dst_txt}{self.pdf_file_name}.txt"
        with open(txt_path, "w", encoding="utf-8") as output_file:
            output_file.write(text)
        

if __name__ == '__main__':


    pdf_src =PDFFileReader()
    pdf_src.read_pdf()

