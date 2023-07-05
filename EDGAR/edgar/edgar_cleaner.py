from bs4 import BeautifulSoup
import re
import os

def clean_html_text(html_text):
    """ Takes in html text and returns a cleaned string """

    regex = re.compile(r'<[^>]+>') 
    tags_removed= regex.sub('', html_text)
    clean_string= re.sub(r"[^A-Za-z0-9]", " ", tags_removed.lower())
    return clean_string

def write_clean_html_text_files(input_folder, dest_folder):
    """ Takes in a folder of html files and returns text files to the destination"""
    
    file_types = ['html','htm']
    for file in os.listdir(input_folder):
        
        input_file_path = os.path.join(input_folder, file)
        with open(input_file_path, 'r') as content_of_file:
            if any([x in file for x in file_types]):          
                soup = BeautifulSoup(content_of_file, 'html.parser')
                text = soup.get_text()
                cleaned_file_string=clean_html_text(text)                      
            else:
                cleaned_file_string=clean_html_text(content_of_file.read())
        
        file_name = file.split('.')
        file_name = f'{file_name[0]}.txt'
        file_path = os.path.join(dest_folder, file_name)
        
        with open(file_path, 'w') as my_file:
            my_file.write(cleaned_file_string)

