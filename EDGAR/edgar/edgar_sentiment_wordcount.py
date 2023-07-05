import os
import pandas as pd
import ref_data
import datetime 

def write_document_sentiments(input_folder, output_file): 
    """ For an input folder of .txt files returns a csv file with sentiment analysis """

    #Creates a dictionary of the LM dictionary
    sentiment_word_dict = ref_data.get_sentiment_word_dict()  
    #Extracts lists of word types from the dictionary 
    positive = sentiment_word_dict['Positive'] 
    #Initialises sentiment counters to 0 
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

    #Creates an empty dataframe with the required columns name
    df = pd.DataFrame(columns=['Symbol','ReportType','FilingDate','Negative','Positive','Uncertainty','Litigious','Constraining','Strong_Modal','Weak_Modal'])
    
    #Initialising a counter to index the empty dataframe
    row_count = 0 

    #Iterates through all files in the input folder   
    for file in os.listdir(input_folder):  
        #Extracts and assigns information from the filename for storage 
        ticker = file.rsplit('_')[0]
        date = file.rsplit('_',1)[-1].rsplit('.',1)[0]  
        file_type = file.split('_',-1)[1] 
        df.loc[row_count,'Symbol'] = ticker
        df.loc[row_count,'ReportType'] = file_type  
        df.loc[row_count,'FilingDate'] = date
        input_file_path = os.path.join(input_folder, file)
        with open(input_file_path,'r') as file_content: 
            #Iterates through each line of the .txt file
            for line in file_content: 
                words = line.split()
                #Adjust the word type counts for each word within the current line
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
        #Assign the sentiment counters to the relevant dataframe column
        df.loc[row_count,'Negative'] = neg_count
        df.loc[row_count,'Positive'] = pos_count
        df.loc[row_count,'Uncertainty'] = uncert_count
        df.loc[row_count,'Litigious'] = lit_count
        df.loc[row_count,'Constraining'] = cons_count
        df.loc[row_count,'Strong_Modal'] = str_count
        df.loc[row_count,'Weak_Modal'] = weak_count
        #Increase the row index
        row_count +=1
        #Reset the sentiment counters
        neg_count = 0
        pos_count = 0 
        uncert_count = 0
        lit_count = 0
        str_count = 0 
        cons_count = 0
        weak_count = 0
    #Convert filing date from string to datetime    
    df['FilingDate'] = pd.to_datetime(df['FilingDate'])
    #Output the data to the specified .csv path
    df.to_csv(output_file,sep=',',index=False)
    
