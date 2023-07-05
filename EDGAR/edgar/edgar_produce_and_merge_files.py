import edgar_downloader
import edgar_cleaner
import ref_data
import edgar_sentiment_wordcount
import pandas as pd
import os 

def edgar_download_clean_sentiment_wordcount(ticker):


    if os.path.exists(f"C:/Users/BenProsser/Core Python/EDGAR/esmeralda-edgar-3/html_folder/{ticker}_html_files"):
        pass
    else:
        os.mkdir(f"C:/Users/BenProsser/Core Python/EDGAR/esmeralda-edgar-3/html_folder/{ticker}_html_files")
    if os.path.exists(f"C:/Users/BenProsser/Core Python/EDGAR/esmeralda-edgar-3/txt_folder/{ticker}_txt_files"):
        pass
    else:
        os.mkdir(f"C:/Users/BenProsser/Core Python/EDGAR/esmeralda-edgar-3/txt_folder/{ticker}_txt_files")
    if os.path.exists(r'C:\Users\BenProsser\Core Python\EDGAR\esmeralda-edgar-3\csv_files'):
        pass
    else:
        os.mkdir(r'C:\Users\BenProsser\Core Python\EDGAR\esmeralda-edgar-3\csv_files')
   
    html_path = f"C:/Users/BenProsser/Core Python/EDGAR/esmeralda-edgar-3/html_folder/{ticker}_html_files"
    txt_path = f"C:/Users/BenProsser/Core Python/EDGAR/esmeralda-edgar-3/txt_folder/{ticker}_txt_files"
    csv_path = f"C:/Users/BenProsser/Core Python/EDGAR/esmeralda-edgar-3/csv_files/{ticker}_sentiment_factors.csv"
    edgar_downloader.download_files_10k(ticker, html_path)
    edgar_cleaner.write_clean_html_text_files(html_path, txt_path)
    edgar_sentiment_wordcount.write_document_sentiments(txt_path, csv_path)


def merge_sentiment_and_financials(ticker):
    financial_df = ref_data.get_yahoo_data('1990-01-01', '2024-01-01', ticker)
    sentiment_df = pd.read_csv(f'csv_files/{ticker}_sentiment_factors.csv')
    sentiment_df['FilingDate'] = pd.to_datetime(sentiment_df['FilingDate'])

    merged_financials_and_sentiment = pd.merge(financial_df, sentiment_df, left_on = 'date', right_on = 'FilingDate')
    merged_financials_and_sentiment.drop(columns = ['ReportType', 'Symbol'], inplace = True)
    #print(merged_financials_and_sentiment)
    return merged_financials_and_sentiment




merge_sentiment_and_financials('AAPL')