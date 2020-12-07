## Data format

Key, value JSON map where key is one of the following (depending on the file): 
- the url
- the youtube url
- the domain name

The value consists of:
- **tweet_ids**: ids of the tweets mentioning the url
- **aggregated_retweet_count**: summed retweet_count of the tweet id’s retweet count metadata field
- **aggregated_quote_count**: summed quote_count of the tweet id’s retweet count metadata field

Some normalizing of the key has been done to merge duplicate entries (see [the notebook](/notebooks/media_analysis.ipynb) for reference)