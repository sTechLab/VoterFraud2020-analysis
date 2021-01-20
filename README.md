# VoterFraud2020-analysis
This repository contains the code behind the data analysis presented in the VoterFraud2020 paper.

- [voterfraud2020.io](http://voterfraud2020.io), interactive web application for exploring the dataset
- [Figshare dataset publication](https://doi.org/10.6084/m9.figshare.13571084) with digital object identifier (DOI) **10.6084/m9.figshare.13571084**


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

