import os
import shutil
import unittest
import edgar_downloader
import ref_data
import edgar_cleaner
import edgar_sentiment_wordcount
import requests
import sys
from io import StringIO
import py_test
import pandas as pd
from unittest.mock import patch


def test_write_page():

    test_dir = 'test_dir'
    os.mkdir(test_dir)
    # We define the url and the path
    url = 'https://example.com'
    file_path = os.path.join(test_dir, 'example.html')
    edgar_downloader.write_page(url, file_path)
    assert os.path.isfile(file_path)
    # We assert that the file at file_path was created successfully

    # Check the content of the file is as expected
    with open(file_path, 'r') as file:
        content = file.read()
        assert 'Example Domain' in content
    
    shutil.rmtree(test_dir)

def test_download_files_10k():

    ticker = 'AAPL'
    dest_folder = 'dest_folder'
    os.mkdir(dest_folder)
    edgar_downloader.download_files_10k(ticker, dest_folder)
    # Obtain a list of all files in the dest folder, and then check they're named correctly
    files = os.listdir(dest_folder)
    for file_name in files:
        assert file_name.startswith(f'{ticker}_10-K')
        assert file_name.endswith(('.html','.htm','.txt'))

    shutil.rmtree(dest_folder)
    
def test_no_content():

    test_dir = 'test_dir'
    os.mkdir(test_dir)
    expected_message = 'The request was successful, but there is no content to send back in the response payload'
    stdout = sys.stdout 
    sys.stdout = captured_output = StringIO()

    edgar_downloader.write_page(r'https://httpbin.org/status/204', test_dir)

    printed_output = captured_output.getvalue().strip()
    sys.stdout = stdout
    assert expected_message in printed_output

    shutil.rmtree(test_dir)

def test_exception_raised():

    test_dir = 'test_dir'
    os.mkdir(test_dir)
    url = r'https://httpbin.org/status/404'
    with py_test.raises(Exception):
        edgar_downloader.write_page(url, test_dir)

    
    shutil.rmtree(test_dir)

def test_not_in_sp100():

    test_dir = 'test_dir'
    os.mkdir(test_dir)
    ticker = 'WRONG'
    with py_test.raises(Exception):
        edgar_downloader.download_files_10k(ticker, test_dir)

    shutil.rmtree(test_dir)

def test_get_yahoo_data():
    start_date = '2022-01-01'
    end_date = '2022-01-05'
    ticker = 'AAPL'
    #Process AAPL data across 5 days
    data = ref_data.get_yahoo_data(start_date,end_date,ticker)
    print(data)
    expected_columns = ['ticker_symbol','1daily_return','2daily_return','3daily_return','5daily_return','10daily_return']
    #Assert the dataframe, correct rows and columns have been created
    assert type(data) == pd.DataFrame
    assert len(data) == 2
    for column in expected_columns:
        assert column in data.columns

def test_get_sp100(requests_mock):
    expected_tickers = ['AAPL','TSLA','AIG']
    #Create a mock html input containing S&P tickers
    mock_html = """
    <table class="wikitable sortable">
        <tr>
            <th>Ticker</th>
            <th>Company</th>
        </tr>
        <tr>
            <td>AAPL</td>
            <td>Apple Inc.</td>
        </tr>
        <tr>
            <td>TSLA</td>
            <td>Tesla, Inc.</td>
        </tr>
        <tr>
            <td>AIG</td>
            <td>American International Group, Inc.</td>
        </tr>
    </table>
    """
    #Extract tickers from mock input
    with patch('requests.get') as mock_get:
        mock_response = mock_get.return_value
        mock_response.text = mock_html
        tickers = ref_data.get_sp100()
    
    #Assert that tickers is a list and contains the right tickers
    assert type(tickers) == list
    assert len(tickers) == len(expected_tickers)
    for ticker in expected_tickers:
        assert ticker in expected_tickers

def test_get_sentiment_word_dict():
    expected_keys = ['Positive','Negative','Uncertainty','Litigious','Constraining','Strong_Modal','Weak_Modal']
    #Generate a dictionary from the LM dictionary
    sentiment_dict = ref_data.get_sentiment_word_dict()
    #Assert the object type and row length
    assert type(sentiment_dict) == dict
    assert len(sentiment_dict) == 7
    #Assert the columns names, word lists and word type
    for key in expected_keys:
        assert key in sentiment_dict
        assert type(sentiment_dict[key]) == list

        for word in sentiment_dict[key]:
            assert type(word) == str

def test_clean_html_text():
    html_text = '<title>aapl-20220924</title>'
    #Test if the tags are no longer in the html and there are no special characters in the text
    list_of_characters = ['!', '<' ,'/', '<title>']
    actual_output = edgar_cleaner.clean_html_text(html_text)

    for item in list_of_characters:
        assert item not in actual_output

def test_write_clean_html_text_files(tmpdir):
    #Make a temp input and destination folders and create temporary HTML file
    input_folder = tmpdir.mkdir('input')
    dest_folder = tmpdir.mkdir('destination')
    html_file_path = input_folder.join('test.html')
    html_file_path.write('<p> Example text<b>TML</b> file.')

    edgar_cleaner.write_clean_html_text_files(str(input_folder), str(dest_folder))
    text_file_path = dest_folder.join('test.txt')
    #Check that the destination folder contains the text file 
    assert text_file_path.exists()

    with open(str(text_file_path), 'r') as file:
        cleaned_file = file.read()

    #Assert that the cleaned text from the html file is equal to the actual output
    #Assert that the text does not contain HTML tags 
    assert cleaned_file == ' example texttml file '
    list_of_characters2 = ['<', '>']

    for item in list_of_characters2:
        assert item not in cleaned_file 

def test_write_document_sentiments(tmp_path):
    input_folder = tmp_path / "input"
    input_folder.mkdir()

    #Creation of three mock input files
    file1 = input_folder / "AAPL_20210515.txt"
    file2 = input_folder / "GOOG_20210515.txt"
    file3 = input_folder / "MSFT_20210515.txt"

    #Each file contains a singular word of a given type
    file1.write_text("winner")
    file2.write_text("abandon")
    file3.write_text("almost")

    output_file = tmp_path / "output.csv"

    #Process the three files
    edgar_sentiment_wordcount.write_document_sentiments(input_folder, output_file)

    #Determine if a file has been created and is of file type
    assert output_file.exists()
    assert output_file.is_file()

    df = pd.read_csv(output_file)

    #Check the data has been generated correctly
    assert len(df) == 3
    assert df[df['Symbol'] == 'AAPL']['Positive'].values[0] == 1
    assert df[df['Symbol'] == 'GOOG']['Negative'].values[0] == 1
    assert df[df['Symbol'] == 'MSFT']['Uncertainty'].values[0] == 1



# if __name__ == '__main__':
#     test_write_page()
#     test_download_files_10k()
#     test_no_content()
#     test_exception_raised()
#     test_not_in_sp100()
   