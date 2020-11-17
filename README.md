# voter-fraud-analysis

## [Link to the live demo application](http://35.208.173.244/)

## Repository set up
```
pip install -r requirements.txt
python -m spacy download en_core_web_lg
```

### Run the streamlit app
```
streamlit run app.py
```

## Creating a new dump for analysis

1. Run [dataflow jobs](https://console.cloud.google.com/dataflow/jobs?project=vote-safety&authuser=2) to export the Datastore to a bucket. Create a new folder in the bucket for the current date (EXPORT_TAG).
2. Copy the data from the bucket to your machine (run this for each DATA_KIND) 
   ```
    gsutil cp -r gs://vote-safety-export/dataflow-export/<EXPORT_TAG>/<DATA_KIND>\*.json ./bucket-export/vote-safety-dataflow/<EXPORT_TAG>/<DATA_KIND>/
    ```

3. Parse and combine the exported data using `python load_dataflow_export.py`

