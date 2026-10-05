# pip install apify-client
import os
from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("datagrit/google-news-rss-monitor").call(run_input={
    "queries": [
        "openai",
        "\"electric vehicles\""
    ],
    "editions": [
        "US:en"
    ],
    "timeRange": "1d",
    "maxItems": 20
})
items = client.dataset(run["defaultDatasetId"]).list_items().items
print(len(items), "records")
print(items[0] if items else None)
