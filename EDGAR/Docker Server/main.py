from fastapi import FastAPI, File, UploadFile
import edgar_cleaner_docker
import edgar_sentiment_docker
from fastapi.responses import FileResponse
import os


app = FastAPI()
#Define filename for csv output
csv_filename = "sentiment_analysis.csv"
#Specify directory within Docker container
output_dir = "/app"
csv_output = os.path.join(output_dir,csv_filename)

#Post method to allow the upload and processing of files by the user
@app.post('/upload')
async def file_upload(my_file: UploadFile = File(...)):
    #Create a new file to write the contents of the uploaded file
    file_name = f"{my_file.filename}"

    file_path = os.path.join(output_dir,file_name)

    with open(file_path, "wb") as file:
        file.write(await my_file.read())

    file_path = f"/app/{file_name}"
    #Carry out cleaning and sentiment analysis to return a dataframe
    txt_file_path = edgar_cleaner_docker.write_clean_html_text_files(file_path)
    df = edgar_sentiment_docker.write_document_sentiments(txt_file_path)
    #Convert the sentiment analysis data to a csv file at the specified path
    df.to_csv(csv_output,sep=',',header=False,index=False,mode='a')

    return {"dataframe" : file_path}

#Get method to download generated .csv file from Docker container
@app.get("/download")
async def download_file():
    return FileResponse(path=csv_output,filename="sentiment_analysis.csv",media_type="text/csv")

