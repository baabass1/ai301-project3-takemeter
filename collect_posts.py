import json
import pandas as pd

posts = []

for filename in [
    "soccer_raw.json",
    "soccer_raw_2.json",
    "soccer_raw_3.json"
]:
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)

    for post in data["data"]["children"]:
        title = post["data"]["title"]

        flair = str(post["data"].get("link_flair_text", "")).lower()

        if "goal" in flair:
            label = "goal_clip"
        elif "stats" in flair:
            label = "stats"
        elif "media" in flair:
            label = "media"
        else:
            label = "media"

        posts.append({
            "text": title,
            "label": label
        })

df = pd.DataFrame(posts)

# Remove duplicate titles
df = df.drop_duplicates(subset=["text"])

df.to_csv("soccer_dataset.csv", index=False)

print("Total examples:", len(df))
print(df["label"].value_counts())