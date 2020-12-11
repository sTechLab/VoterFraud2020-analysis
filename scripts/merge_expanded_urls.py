import os
import json
import tldextract

directory = "./data/expanded_urls/run-2/"
merged_url_map = {}
expanded_urls = set()
total = 0
for filename in os.listdir(directory):
    i = 0
    if '.json' in filename:
        with open(directory + filename, "r") as f:
            expanded_url_map = json.load(f)

            for url, v in expanded_url_map.items():
                url_info = v.copy()
                expanded_url_info = url_info["expansion_history"][-1]
                url_info["expanded_url"] = expanded_url_info
                if "url" in expanded_url_info:
                    expanded_urls.add(expanded_url_info["url"])
                    domain_parts = tldextract.extract(expanded_url_info["url"])
                    expanded_url_info["domain"] = {
                        "subdomain": domain_parts.subdomain,
                        "domain": domain_parts.domain,
                        "suffix": domain_parts.suffix
                    }
                del url_info["expansion_history"]
                merged_url_map[url] = url_info
                i += 1

        print("{} unique URLs processed".format(i))
    total += i

print("{} unique URLs processed in total".format(total))
print("found {} unique expanded URLs".format(len(expanded_urls)))

with open(directory + 'expanded_url_map.json', 'w') as f:
    f.write(json.dumps(merged_url_map) + "\n")