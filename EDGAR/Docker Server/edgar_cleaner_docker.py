from bs4 import BeautifulSoup
import re

def clean_html_text(html_text):
    regex = re.compile(r'<[^>]+>')
    tags_removed= regex.sub('', html_text)
    clean_string= re.sub(r"[^A-Za-z0-9]", " ", tags_removed.lower())
    return clean_string

def write_clean_html_text_files(input_file):
    file_types = ['html','htm']

    with open(input_file, 'r') as content_of_file:
        if any([x in input_file for x in file_types]):          
            soup = BeautifulSoup(content_of_file, 'html.parser')
            text = soup.get_text()
            cleaned_file_string=clean_html_text(text)                      
        else:
            cleaned_file_string=clean_html_text(content_of_file.read())
    
    file_name = input_file.split('.')
    file_name = f'{file_name[0]}.txt'
    
    with open(file_name, 'w') as my_file:
        my_file.write(cleaned_file_string)

    return file_name
