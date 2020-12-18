# Readme
### Collected URLs
- [14 Nov dump (Oct 23rd - Nov 14th)](./14-nov/)
- [16 Dec dump (Oct 23rd - Dec 16th)](./16-dec/)

### Data format
Key, value JSON map where key is one of the following (depending on the file): 
- the url
- the youtube url
- the domain name

The value consists of:
- **tweet_ids**: ids of the tweets mentioning the url
- **aggregated_retweet_count**: summed retweet_count of the tweet id’s retweet count metadata field
- **aggregated_quote_count**: summed quote_count of the tweet id’s retweet count metadata field


Some normalizing of the key has been done to merge duplicate entries (see [the notebook](/notebooks/media_analysis.ipynb) for reference)

### expanded_url_map

**expanded_url_map.json** contains **all_urls.json** with URLs expanded to their "final" destination using [this script](/scripts/expand_urls.py).

*Example entries:*
```json
{
    "https://youtu.be/wmzdsq1qjas": {
        "aggregated_quote_count": 0,
        "aggregated_retweet_count": 2,
        "tweet_ids": [
            "1325620660018802688"
        ],
        "expanded_url": {
            "status_code": 200,
            "url": "https://www.youtube.com/watch?v=wmzdsq1qjas&feature=youtu.be",
            "domain": {
                "subdomain": "www",
                "domain": "youtube",
                "suffix": "com"
            }
        }
    },
    "https://zoomnewsonline.com/election-officers-reject-trumps-claims-of-fraud/": {
        "aggregated_quote_count": 0,
        "aggregated_retweet_count": 0,
        "tweet_ids": [
            "1327586275499642880"
        ],
        "expanded_url": {
            "error": "request exception"
        }
    },
}
```