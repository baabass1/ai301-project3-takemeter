# Project Planning

## Community Selection

**Community:** r/soccer

I selected r/soccer because it is one of the largest sports communities on Reddit and contains a diverse range of post types including news, match highlights, statistics, and fan discussions. The variety of content makes it well suited for a text classification task.

---

## Classification Task

The goal of this project is to classify soccer-related Reddit posts into one of three categories.

### Label 1: media

General soccer news, interviews, reactions, celebrations, photos, announcements, fan content, and discussion posts.

**Examples**

* "Lamine Yamal raises Palestine Flag during parade"
* "Norway's football team official photo for World Cup 2026"

### Label 2: goal_clip

Posts describing goals, scoring highlights, or match clips.

**Examples**

* "USA [1] - 1 Germany - Antonee Robinson great goal 37'"
* "Argentina [3] - 0 Algeria - Lionel Messi 76' hat-trick"

### Label 3: stats

Posts focused on records, statistics, numerical achievements, historical comparisons, or performance metrics.

**Examples**

* "15 - Curaçao's Eloy Room recorded 15 saves against Ecuador"
* "Arsenal completed less than 200 passes in 120 minute match in UCL final"

---

## Data Collection Plan

Data will be collected from r/soccer using Reddit JSON endpoints.

Collection process:

1. Retrieve posts from multiple subreddit feeds.
2. Extract post titles.
3. Remove duplicate entries.
4. Manually review posts.
5. Assign labels based on the taxonomy above.
6. Save labeled data to a CSV file for training.

---

## Dataset Goals

Target dataset size:

* Minimum: 200 examples
* Target: 250 examples

Actual dataset collected:

| Label     | Count |
| --------- | ----: |
| media     |   193 |
| goal_clip |    26 |
| stats     |    16 |
| Total     |   235 |

---

## Model Selection

### Fine-Tuned Model

Model:

```text
distilbert-base-uncased
```

Reason for selection:

DistilBERT offers a strong balance between classification performance and computational efficiency. It is significantly smaller than BERT while maintaining competitive accuracy on text classification tasks.

---

## Baseline Model

Baseline:

```text
Groq Llama 3.3 70B
```

The baseline uses zero-shot prompting to classify posts without task-specific training.

The baseline will be compared against the fine-tuned DistilBERT model using the same test set.

---

## Evaluation Metrics

The project will evaluate:

* Accuracy
* Precision
* Recall
* F1-score
* Confusion Matrix

Performance will be measured on a held-out test set.

---

## Expected Challenges

1. Class imbalance due to the large number of media posts.
2. Distinguishing goal clips from general soccer news.
3. Identifying statistical posts that resemble match reports.
4. Limited dataset size for minority classes.

---

## Success Criteria

The project will be considered successful if the classifier can accurately distinguish between media, goal_clip, and stats posts and provide meaningful insight into the strengths and weaknesses of fine-tuning compared to a zero-shot baseline.
