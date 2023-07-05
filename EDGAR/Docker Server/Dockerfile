FROM python:3.10 
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY edgar_cleaner_docker.py .
COPY edgar_sentiment_docker.py .
COPY ref_data.py .
COPY main.py .
COPY Loughran-McDonald_MasterDictionary_1993-2021.csv .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port" ,"50"]