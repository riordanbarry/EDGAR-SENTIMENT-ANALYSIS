import requests
from bs4 import BeautifulSoup
import ref_data
import os

def write_page(url,file_path):

    headers = {'User-Agent': 'TomWalton'}
    r = requests.get(url,headers=headers)
    if r.status_code == 200:
        text_data = r.text
        with open(file_path,'w') as file:
            file.write(text_data)
    elif r.status_code == 201:
            print('The request was successful, and a nbew resource has been created as a result.')
    elif r.status_code == 204:
            print('The request was successful, but there is no content to send back in the response payload')
    else:
         raise Exception('The HTTP request was unsuccessful.')


def download_files_10k(ticker, dest_folder):

    if ticker not in ref_data.get_sp100():
         raise Exception('Please enter a comapny ticker that is within the S&P100')
    
    if not os.path.exists(dest_folder):
         raise FileNotFoundError(f"Destination folder {dest_folder} not found.")
    
    url = f'https://www.sec.gov//cgi-bin/browse-edgar?action=getcompany&CIK={ticker}&type=10-K&dateb=&owner=exclude&count=100'
    url_base = "https://www.sec.gov"
    headers = {'User-Agent': 'TomWalton'}
    r= requests.get(url,headers=headers)

    if r.status_code == 200:
        soup = BeautifulSoup(r.text,'html.parser')
        table = soup.find('table',{'summary':'Results'})
        rows = table.find_all('tr')[1:]
        filing_dates = []

        for row in rows:
            cols = row.find_all('td')
            filing_dates.append(cols[3].text.strip())

        urls = []
        for entry in soup.select("a[href*='/Archives/edgar/data/'][href$='.htm']"):
            urls.append(entry['href'])

        for entry in soup.select("a[href*='/Archives/edgar/data/'][href$='.html']"):
            urls.append(entry['href'])
    elif r.status_code == 201:
            print('The request was successful, and a new resource has been created as a result.')
    elif r.status_code == 204:
            print('The request was successful, but there is no content to send back in the response payload')
    else:
        raise Exception('Unsuccessful HTTP request.')
    
    report_urls = []
    for url in urls:
        new_url = url_base + url
        report_urls.append(new_url)

    html_urls = []
    for url in report_urls:
        headers = {'User-Agent': 'TomWalton'}
        r= requests.get(url,headers=headers)

        if r.status_code == 200:
            soup = BeautifulSoup(r.text,'html.parser')
            table = soup.find("table",summary = "Document Format Files")
            table_rows = table.find_all("tr")[1:]

            for row in table_rows:
                cells = row.find_all("td")
                if "10-K" in cells[3].text:
                    if cells[2].find("a")["href"].endswith(('html','htm','txt')):
                        document_link = url_base + cells[2].find("a")["href"]
                        if r'ix?doc=/' in document_link:
                            document_link = document_link.replace(r'ix?doc=/','')
                        
                        html_urls.append(document_link)
                        break
                elif cells[1].text == 'Complete submission text file':
                    document_link = url_base + cells[2].find("a")["href"]
                    html_urls.append(document_link)
        elif r.status_code == 201:
            print('The request was successful, and a new resource has been created as a result.')
        elif r.status_code == 204:
            print('The request was successful, but there is no content to send back in the response payload')
        else:
            raise Exception('The HTTP request was not successful.')
        
    file_paths = []

    for i in range(0,len(html_urls)):
        url_split = html_urls[i].rsplit('.',1)
        file_paths.append(os.path.join(dest_folder, f'{ticker}_10-K_{filing_dates[i]}.{url_split[1]}'))

    for i in range(0,len(file_paths)):
        write_page(html_urls[i],file_paths[i])

