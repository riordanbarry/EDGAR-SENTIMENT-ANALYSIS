import requests
import os
import csv
import pandas as pd

#Specify the endpoints for the API
upload_url = "http://localhost:50/file"
download_url = "http://localhost:50/download"

#Singular input point from the user pointing to folder containing downloaded files
folder_path = r"C:\html_files"

#Iterate through raw files in the input folder
for file_path in os.listdir(folder_path):
    input_file_path = os.path.join(folder_path, file_path)
    with open(input_file_path, "rb") as file:
        #Assess whether the base file is .txt or .htm/l
        if input_file_path.rsplit('.',-1)[1] == 'txt':
            files = {"my_file": (input_file_path, file)}
        else:
            files = {"my_file": (input_file_path, file, "text/html")}
        #Call the post request at the specified endpoint to upload the file
        post_response = requests.post(upload_url, files=files)
        if post_response.status_code != 200:
            print("API Post Request Failed")
        #Get request to download the .csv file generated in the container
        get_response = requests.get(download_url)
        if get_response.status_code != 200:
            print("API Get Request Failed")
        with open("sentiment_analysis.csv","wb") as file:
            file.write(get_response.content)
        
#CSV module used to insert the required columns names and aggregate sentiment
filename = "sentiment_analysis.csv"
column_names = ['Symbol','ReportType','FilingDate','Negative','Positive','Uncertainty','Litigious','Constraining','Strong_Modal','Weak_Modal']
rows = []
with open(filename,'r',newline='') as file:
    reader = csv.reader(file)
    for row in reader:
        rows.append(row)

rows.insert(0,column_names)

df = pd.DataFrame(rows[1:],columns=column_names)

sentiment_sum = df[column_names[3:]].astype(float).sum()

max_sentiment = sentiment_sum.idxmax()

df['Aggregate Sentiment'] = max_sentiment

rows = [df.columns.tolist()] + df.values.tolist()

with open(filename,'w',newline='') as file:
    writer = csv.writer(file)
    writer.writerows(rows)

