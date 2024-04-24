# VoterFraud2020-analysis
This repository contains the code behind the data analysis presented in the VoterFraud2020 paper and [the website](https://voterfraud2020.io). It is primarily meant for internal use by the authors since the code requires the raw data to run, which we are unable to share. We hope that making this repository publicly available can be helpful for others who are performing a similar analysis.

- [voterfraud2020.io](http://voterfraud2020.io), interactive web application for exploring the dataset
- [Figshare dataset publication](https://doi.org/10.6084/m9.figshare.13571084) with digital object identifier (DOI) **10.6084/m9.figshare.13571084**



## Run the streamlit app
```
pip install -r requirements.txt
streamlit run app.py
```

## Full repository set up
```
pip install -r requirements_extra.txt
python -m spacy download en_core_web_lg
```

# For repository maintainers (stechlab)
The below instructions require special permissions.

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
gsutil signurl -r us -d 7d <private-key-file> gs://vote-safety-export/voterfraud2020-dataset/anonymized/retweets/2020-10.zip
gsutil signurl -r us -d 7d <private-key-file> gs://vote-safety-export/voterfraud2020-dataset/anonymized/retweets/2020-11.zip
gsutil signurl -r us -d 7d <private-key-file> gs://vote-safety-export/voterfraud2020-dataset/anonymized/retweets/2020-12.zip
gsutil signurl -r us -d 7d <private-key-file> gs://vote-safety-export/voterfraud2020-dataset/anonymized/tweets/2020-10.zip
gsutil signurl -r us -d 7d <private-key-file> gs://vote-safety-export/voterfraud2020-dataset/anonymized/tweets/2020-11.zip
gsutil signurl -r us -d 7d <private-key-file> gs://vote-safety-export/voterfraud2020-dataset/anonymized/tweets/2020-12.zip
```

**7 days (hydrated data):**
```
gsutil signurl -r us -d 7d <private-key-file> gs://vote-safety-export/voterfraud2020-dataset/hydrated/retweets/2020-10.zip
gsutil signurl -r us -d 7d <private-key-file> gs://vote-safety-export/voterfraud2020-dataset/hydrated/retweets/2020-11.zip
gsutil signurl -r us -d 7d <private-key-file> gs://vote-safety-export/voterfraud2020-dataset/hydrated/retweets/2020-12.zip
gsutil signurl -r us -d 7d <private-key-file> gs://vote-safety-export/voterfraud2020-dataset/hydrated/tweets/2020-10.zip
gsutil signurl -r us -d 7d <private-key-file> gs://vote-safety-export/voterfraud2020-dataset/hydrated/tweets/2020-11.zip
gsutil signurl -r us -d 7d <private-key-file> gs://vote-safety-export/voterfraud2020-dataset/hydrated/tweets/2020-12.zip
gsutil signurl -r us -d 7d <private-key-file> gs://vote-safety-export/voterfraud2020-dataset/hydrated/users/users.zip
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
Data columns (total: 25 columns, 7,603,103 tweets):
 #   Column                            Dtype  
---  ------                            -----  
 0   tweet_id                          str 
 1   user_community                    0 | 1 | 2 | 3 | 4 | null
 2   user_active_status                "active" | "suspended" | "deleted"
 3   retweet_count_metadata            int  
 4   quote_count_metadata              int  
 5   retweet_count_by_community_0      int  
 6   quote_count_by_community_0        int  
 7   retweet_count_by_community_1      int  
 8   quote_count_by_community_1        int  
 9   retweet_count_by_community_2      int  
 10  quote_count_by_community_2        int  
 11  retweet_count_by_community_3      int  
 12  quote_count_by_community_3        int  
 13  retweet_count_by_community_4      int  
 14  quote_count_by_community_4        int  
 15  retweet_count_by_suspended_users  int  
 16  quote_count_by_suspended_users    int  
 17  user_id                           str  
 18  quote_tweet                       str | null (id of the quoted tweet if this tweet is a quote)
 19  hashtags                          str[] 
 20  has_media                         bool   
 21  timestamp                         date 
 22  text                              str 
 23  urls                              str[] 
 24  resolved_urls                     str[] (excludes urls that start with twitter.com/. Fallback to urls if the url was not possible to resolve) 
Pandas memory usage: 1.4+ GB
```
### /hydrated/retweets/
```
Data columns (total: 3 columns, 25,566,698 retweets):
 #   Column        Dtype 
---  ------        ----- 
 0   retweeted_id  str 
 1   user_id       str
 2   timestamp     date
Pandas memory usage: 780.2+ MB
```
### /hydrated/users/

- **Total users**: 2,559,018
- **Users with metadata**: 2,460,175

Some of the user metadata is missing since we didn't pull metadata for retweeting users.
As long as the user tweeted at least once within our dataset, their metadata is included.

For users that only retweeted other users, we retroactively pulled their metadata on February 1st.
For tweeting users, their metadata was pulled when we first streamed a tweet from this user or when we first streamed a retweet of this user's tweet (whichever comes first).

If you are interested in when the metadata was pulled for each user you can look at the timestamp column in the retweets or tweets tables.

```
 #   Column                                  Dtype  
---  ------                                  -----  
 0   user_id                                 str  
 1   user_community                          0 | 1 | 2 | 3 | 4 | null
 2   user_active_status                      "active" | "suspended" | "deleted" 
 3   closeness_centrality_detractor_cluster  float | null
 4   closeness_centrality_promoter_cluster   float | null
 5   retweet_count_by_community_0            int  
 6   quote_count_by_community_0              int  
 7   retweet_count_by_community_1            int  
 8   quote_count_by_community_1              int  
 9   retweet_count_by_community_2            int  
 10  quote_count_by_community_2              int  
 11  retweet_count_by_community_3            int  
 12  quote_count_by_community_3              int  
 13  retweet_count_by_community_4            int  
 14  quote_count_by_community_4              int  
 15  retweet_count_by_suspended_users        int  
 16  quote_count_by_suspended_users          int  
 17  name                                    str 
 18  handle                                  str 
 19  created_at                              date 
 20  verified                                bool 
 21  description                             str 
 22  followers_count                         int
 23  location                                str
Pandas memory usage: 488.1+ MB
```
### /anonymized/tweets/
```
../data/data-share/anonymized/tweets/
Data columns (total 25 columns, 7,603,103 tweets):
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
Pandas memory usage: 2.8+ GB
```
### /anonymized/retweets/
```
Data columns (total: 3 columns, 25,566,698 retweets):
 #   Column          Dtype 
---  ------          ----- 
 0   retweeted_id    int64 
 1   hashed_user_id  object
 2   timestamp       object
Pandas memory usage: 780.2+ MB
```
