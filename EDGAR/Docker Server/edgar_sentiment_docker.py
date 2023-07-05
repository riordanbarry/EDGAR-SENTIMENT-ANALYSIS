import os
import pandas as pd
import ref_data

def write_document_sentiments(input_file):

    sentiment_word_dict = ref_data.get_sentiment_word_dict()

    positive = sentiment_word_dict['Positive']
    pos_count = 0
    negative = sentiment_word_dict['Negative']
    neg_count = 0
    uncertainty = sentiment_word_dict['Uncertainty']
    uncert_count = 0
    litigious = sentiment_word_dict['Litigious']
    lit_count = 0
    strong_modal = sentiment_word_dict['Strong_Modal']
    str_count = 0
    weak_modal = sentiment_word_dict['Weak_Modal']
    weak_count = 0
    constraining = sentiment_word_dict['Constraining']
    cons_count = 0

    df = pd.DataFrame(columns=['Symbol','ReportType','FilingDate','Negative','Positive','Uncertainty','Litigious','Constraining','Strong_Modal','Weak_Modal'])
    
    row_count = 0  
    ticker = input_file.split('/')[2].split('_')[0]
    file_type = input_file.split('_',-1)[1]
    date = input_file.rsplit('_',1)[-1].split('.',1)[0].rsplit('_',1)[-1]
    df.loc[row_count,'Symbol'] = ticker
    df.loc[row_count,'ReportType'] = file_type
    df.loc[row_count,'FilingDate'] = date
    with open(input_file,'r') as file_content:
        for line in file_content:
            words = line.split()
            for i in range(0,len(words)):
                if words[i] in positive:
                    pos_count +=1
                if words[i] in negative:
                    neg_count +=1
                if words[i] in uncertainty:
                    uncert_count +=1
                if words[i] in litigious:
                    lit_count +=1
                if words[i] in strong_modal:
                    str_count +=1
                if words[i] in weak_modal:
                    weak_count +=1
                if words[i] in constraining:
                    cons_count +=1
    df.loc[row_count,'Negative'] = neg_count
    df.loc[row_count,'Positive'] = pos_count
    df.loc[row_count,'Uncertainty'] = uncert_count
    df.loc[row_count,'Litigious'] = lit_count
    df.loc[row_count,'Constraining'] = cons_count
    df.loc[row_count,'Strong_Modal'] = str_count
    df.loc[row_count,'Weak_Modal'] = weak_count
    pos_count = 0
    neg_count = 0
    uncert_count = 0
    lit_count = 0
    cons_count = 0
    strong_modal = 0
    weak_modal = 0
    return df

