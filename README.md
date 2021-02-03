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


# Sharing the dataset with [signed URLs](https://cloud.google.com/storage/docs/gsutil/commands/signurl)

**Bucket:** vote-safety-export

**7 days (anonymized data):**
```
gsutil signurl -d 7d <private-key-file> gs://vote-safety-export/voterfraud2020-dataset/anonymized/retweets/2020-10.zip
gsutil signurl -d 7d <private-key-file> gs://vote-safety-export/voterfraud2020-dataset/anonymized/retweets/2020-11.zip
gsutil signurl -d 7d <private-key-file> gs://vote-safety-export/voterfraud2020-dataset/anonymized/retweets/2020-12.zip
gsutil signurl -d 7d <private-key-file> gs://vote-safety-export/voterfraud2020-dataset/anonymized/tweets/2020-10.zip
gsutil signurl -d 7d <private-key-file> gs://vote-safety-export/voterfraud2020-dataset/anonymized/tweets/2020-11.zip
gsutil signurl -d 7d <private-key-file> gs://vote-safety-export/voterfraud2020-dataset/anonymized/tweets/2020-12.zip
```

**7 days (hydrated data):**
```
gsutil signurl -d 7d <private-key-file> gs://vote-safety-export/voterfraud2020-dataset/hydrated/retweets/2020-10.zip
gsutil signurl -d 7d <private-key-file> gs://vote-safety-export/voterfraud2020-dataset/hydrated/retweets/2020-11.zip
gsutil signurl -d 7d <private-key-file> gs://vote-safety-export/voterfraud2020-dataset/hydrated/retweets/2020-12.zip
gsutil signurl -d 7d <private-key-file> gs://vote-safety-export/voterfraud2020-dataset/hydrated/tweets/2020-10.zip
gsutil signurl -d 7d <private-key-file> gs://vote-safety-export/voterfraud2020-dataset/hydrated/tweets/2020-11.zip
gsutil signurl -d 7d <private-key-file> gs://vote-safety-export/voterfraud2020-dataset/hydrated/tweets/2020-12.zip
gsutil signurl -d 7d <private-key-file> gs://vote-safety-export/voterfraud2020-dataset/hydrated/users/users.zip
```


## Loading the hydrated dataset chunks
[See this notebook for an example](https://github.com/sTechLab/VoterFraud2020/blob/main/example_statistics.ipynb)
```python
# First unzip the chunks you wish to load

def load_chunks(directory):
    chunk_dfs = []
    for name in sorted(os.listdir(directory)):
        sub_directory = os.path.join(directory, name)
        if os.path.isdir(sub_directory):
            for filename in sorted(os.listdir(sub_directory)):
                with open(os.path.join(sub_directory, filename), "r", encoding="utf-8") as f:
                    chunk = pd.read_csv(f, encoding = "utf-8")
                    chunk_dfs.append(chunk)
        elif name.endswith(".csv"):
            chunk = pd.read_csv(os.path.join(directory, name), encoding = "utf-8")
            chunk_dfs.append(chunk)

    return pd.concat(chunk_dfs)


load_chunks("/path/to/tweets")
load_chunks("/path/to/retweets")
load_chunks("/path/to/users")
```

## Dataset column info
### /hydrated/tweets/
```
(7603103, 25)
<class 'pandas.core.frame.DataFrame'>
Int64Index: 7603103 entries, 0 to 52584
Data columns (total 25 columns):
 #   Column                            Dtype  
---  ------                            -----  
 0   tweet_id                          int64  
 1   user_community                    float64
 2   user_active_status                object 
 3   retweet_count_metadata            int64  
 4   quote_count_metadata              int64  
 5   retweet_count_by_community_0      int64  
 6   quote_count_by_community_0        int64  
 7   retweet_count_by_community_1      int64  
 8   quote_count_by_community_1        int64  
 9   retweet_count_by_community_2      int64  
 10  quote_count_by_community_2        int64  
 11  retweet_count_by_community_3      int64  
 12  quote_count_by_community_3        int64  
 13  retweet_count_by_community_4      int64  
 14  quote_count_by_community_4        int64  
 15  retweet_count_by_suspended_users  int64  
 16  quote_count_by_suspended_users    int64  
 17  user_id                           int64  
 18  quote_tweet                       float64
 19  hashtags                          object 
 20  has_media                         bool   
 21  timestamp                         object 
 22  text                              object 
 23  urls                              object 
 24  resolved_urls                     object 
dtypes: bool(1), float64(2), int64(16), object(6)
memory usage: 1.4+ GB
```
### /hydrated/retweets/
```
(25566698, 3)
<class 'pandas.core.frame.DataFrame'>
Int64Index: 25566698 entries, 0 to 203826
Data columns (total 3 columns):
 #   Column        Dtype 
---  ------        ----- 
 0   retweeted_id  int64 
 1   user_id       int64 
 2   timestamp     object
dtypes: int64(2), object(1)
memory usage: 780.2+ MB
```
### /hydrated/users/

Total users: 2,559,018
Users with metadata: 2,460,175

Some of the user metadata is missing since we didn't pull metadata for retweeting users.
As long as the user tweeted at least once within our dataset, their metadata is included.

For retweeting users, we retroactively pulled their metadata on February 1st.

```
(2559018, 24)
<class 'pandas.core.frame.DataFrame'>
Int64Index: 2559018 entries, 0 to 59017
Data columns (total 24 columns):
 #   Column                                  Dtype  
---  ------                                  -----  
 0   user_id                                 int64  
 1   user_community                          float64
 2   user_active_status                      object 
 3   closeness_centrality_detractor_cluster  float64
 4   closeness_centrality_promoter_cluster   float64
 5   retweet_count_by_community_0            int64  
 6   quote_count_by_community_0              int64  
 7   retweet_count_by_community_1            int64  
 8   quote_count_by_community_1              int64  
 9   retweet_count_by_community_2            int64  
 10  quote_count_by_community_2              int64  
 11  retweet_count_by_community_3            int64  
 12  quote_count_by_community_3              int64  
 13  retweet_count_by_community_4            int64  
 14  quote_count_by_community_4              int64  
 15  retweet_count_by_suspended_users        int64  
 16  quote_count_by_suspended_users          int64  
 17  name                                    object 
 18  handle                                  object 
 19  created_at                              object 
 20  verified                                object 
 21  description                             object 
 22  followers_count                         float64
 23  location                                object 
dtypes: float64(4), int64(13), object(7)
memory usage: 488.1+ MB
```
### /anonymized/tweets/
```
../data/data-share/anonymized/tweets/
(15206206, 25)
<class 'pandas.core.frame.DataFrame'>
Int64Index: 15206206 entries, 0 to 52584
Data columns (total 25 columns):
 #   Column                            Dtype  
---  ------                            -----  
 0   tweet_id                          int64  
 1   user_community                    float64
 2   user_active_status                object 
 3   retweet_count_metadata            int64  
 4   quote_count_metadata              int64  
 5   retweet_count_by_community_0      int64  
 6   quote_count_by_community_0        int64  
 7   retweet_count_by_community_1      int64  
 8   quote_count_by_community_1        int64  
 9   retweet_count_by_community_2      int64  
 10  quote_count_by_community_2        int64  
 11  retweet_count_by_community_3      int64  
 12  quote_count_by_community_3        int64  
 13  retweet_count_by_community_4      int64  
 14  quote_count_by_community_4        int64  
 15  retweet_count_by_suspended_users  int64  
 16  quote_count_by_suspended_users    int64  
 17  hashed_user_id                    object 
 18  quote_tweet                       float64
 19  hashtags                          object 
 20  has_media                         bool   
 21  timestamp                         object 
 22  text                              object 
 23  urls                              object 
 24  resolved_urls                     object 
dtypes: bool(1), float64(2), int64(15), object(7)
memory usage: 2.8+ GB
```
### /anonymized/retweets/
```
(25566698, 3)
<class 'pandas.core.frame.DataFrame'>
Int64Index: 25566698 entries, 0 to 203826
Data columns (total 3 columns):
 #   Column          Dtype 
---  ------          ----- 
 0   retweeted_id    int64 
 1   hashed_user_id  object
 2   timestamp       object
dtypes: int64(1), object(2)
memory usage: 780.2+ MB
```