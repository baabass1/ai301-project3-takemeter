# TakeMeter: Soccer Post Classification with DistilBERT

## Overview

This project builds a text classification system for posts from the Reddit community r/soccer. The goal is to automatically classify soccer-related posts into meaningful categories using a fine-tuned DistilBERT model and compare its performance against a zero-shot large language model baseline.

I chose r/soccer because it is one of the largest sports communities on Reddit and contains a diverse mix of news, match highlights, statistics, and fan discussions. This variety makes it a strong candidate for a text classification task.

---

# Community Choice and Reasoning

The r/soccer community contains millions of soccer fans discussing matches, players, statistics, transfers, highlights, and news. Unlike many online communities that focus on a single content type, r/soccer contains multiple distinct categories of posts that can reasonably be separated through machine learning classification.

The subreddit provides a mixture of:

* News and announcements
* Goal highlights
* Statistical records and achievements
* Fan reactions and celebrations
* Match discussions

This diversity made it a good choice for building and evaluating a text classification model.

---

# Label Taxonomy

## media

General soccer news, interviews, fan moments, celebrations, reactions, photos, announcements, discussions, or other non-statistical content.

### Examples

* "Lamine Yamal raises Palestine Flag during parade"
* "Norway's football team official photo for World Cup 2026"

---

## goal_clip

Posts describing a goal, scoring highlight, or match clip.

### Examples

* "USA [1] - 1 Germany - Antonee Robinson great goal 37'"
* "Argentina [3] - 0 Algeria - Lionel Messi 76' hat-trick"

---

## stats

Posts focused on records, statistics, numerical achievements, historical comparisons, or performance metrics.

### Examples

* "15 - Curaçao's Eloy Room recorded 15 saves against Ecuador"
* "Arsenal completed less than 200 passes in 120 minute match in UCL final"

---

# Data Collection

Data was collected from r/soccer using Reddit JSON endpoints.

Files collected:

* soccer_raw.json
* soccer_raw_2.json
* soccer_raw_3.json

The collected posts were manually reviewed and assigned one of three labels:

* media
* goal_clip
* stats

The final dataset was stored as:

```text id="swstch"
soccer_dataset.csv
```

---

# Dataset Statistics

| Label     | Count |
| --------- | ----: |
| media     |   193 |
| goal_clip |    26 |
| stats     |    16 |
| Total     |   235 |

The dataset is highly imbalanced, with over 82% of examples belonging to the media category.

---

# Difficult-to-Label Examples

## Example 1

Post:

> Diogo Jota's last career goal

Decision:

Although the post contains the word "goal", it refers to a memorable soccer moment rather than a goal highlight clip. It was labeled as media.

---

## Example 2

Post:

> 15 - Curaçao's Eloy Room recorded 15 saves against Ecuador

Decision:

This post communicates a statistical achievement and record rather than a match event. It was labeled as stats.

---

## Example 3

Post:

> Argentina [3] - 0 Algeria - Lionel Messi 76' hat-trick

Decision:

The scoreline and timestamp indicate a scoring event and match highlight. It was labeled as goal_clip.

---

# Fine-Tuning Approach

## Base Model

The project uses:

```text id="5fshcw"
distilbert-base-uncased
```

from Hugging Face Transformers.

DistilBERT was selected because it is smaller and faster than BERT while maintaining strong classification performance.

---

## Training Setup

Dataset split:

| Split      | Examples |
| ---------- | -------: |
| Train      |      164 |
| Validation |       35 |
| Test       |       36 |

The dataset was tokenized using the DistilBERT tokenizer and converted into Hugging Face datasets.

---

## Hyperparameter Decision

The following hyperparameters were used:

* Epochs: 3
* Learning Rate: 2e-5
* Training Batch Size: 16
* Evaluation Batch Size: 32
* Weight Decay: 0.01
* Warmup Steps: 50

A learning rate of 2e-5 was selected because it is a common and stable starting point for fine-tuning transformer models.

---

# Baseline Description

A zero-shot baseline was evaluated using Groq's Llama 3.3 70B model.

Prompt used:

```text id="9wrn2h"
You are classifying posts from r/soccer.

media:
General soccer news, interviews, fan moments, celebrations, reactions, photos, announcements, discussions, or non-statistical content.

goal_clip:
Posts describing a goal, scoring highlight, or match clip.

stats:
Posts focused on records, statistics, numerical achievements, historical comparisons, or performance metrics.

Respond with ONLY ONE of these labels:

media
goal_clip
stats
```

Each test example was sent individually to the model and predictions were compared against ground-truth labels.

---

# Evaluation Results

## Fine-Tuned DistilBERT

### Accuracy

**80.6%**

### Per-Class Metrics

| Label     | Precision | Recall |   F1 |
| --------- | --------: | -----: | ---: |
| media     |      0.81 |   1.00 | 0.89 |
| goal_clip |      0.00 |   0.00 | 0.00 |
| stats     |      0.00 |   0.00 | 0.00 |

---

## Zero-Shot Baseline (Groq)

### Accuracy

**88.9%**

### Per-Class Metrics

| Label     | Precision | Recall |   F1 |
| --------- | --------: | -----: | ---: |
| media     |      0.96 |   0.90 | 0.93 |
| goal_clip |      0.57 |   1.00 | 0.73 |
| stats     |      1.00 |   0.67 | 0.80 |

---

## Results Comparison

| Model                   | Accuracy |
| ----------------------- | -------: |
| Groq Zero-Shot Baseline |    88.9% |
| Fine-Tuned DistilBERT   |    80.6% |

The fine-tuned model underperformed the zero-shot baseline by 8.3 percentage points.

---

# Confusion Matrix

## Confusion Matrix Table

| True Label | Predicted: media | Predicted: goal_clip | Predicted: stats |
| ---------- | ---------------: | -------------------: | ---------------: |
| media      |               29 |                    0 |                0 |
| goal_clip  |                4 |                    0 |                0 |
| stats      |                3 |                    0 |                0 |

The confusion matrix shows that the model predicted every test example as the majority class (media). This behavior is consistent with the class imbalance present in the training dataset.

The visual confusion matrix is included as:

```text id="vxv73v"
confusion_matrix.png
```

---

# Sample Classifications

| Post                                                                    | Predicted Label | Confidence | Correct |
| ----------------------------------------------------------------------- | --------------- | ---------- | ------- |
| Norway's football team official photo for World Cup 2026                | media           | 0.81       | Yes     |
| USA [1] - 1 Germany - Antonee Robinson great goal 37'                   | media           | 0.39       | No      |
| Arsenal completed less than 200 passes in 120 minute match in UCL final | media           | 0.40       | No      |
| Lamine Yamal raises Palestine Flag during parade                        | media           | 0.85       | Yes     |
| 15 - Curaçao's Eloy Room recorded 15 saves against Ecuador              | media           | 0.41       | No      |

### Example of a Correct Classification

The model correctly classified:

> Norway's football team official photo for World Cup 2026

as media because the post describes a newsworthy soccer-related event and does not contain a goal highlight or statistical achievement.

---

# Error Analysis

## Wrong Prediction 1

Post:

> USA [1] - 1 Germany - Antonee Robinson great goal 37'

True Label: goal_clip

Predicted Label: media

Confidence: 0.39

Analysis:

The model learned to strongly favor the majority media class and failed to recognize goal highlight patterns.

---

## Wrong Prediction 2

Post:

> Arsenal completed less than 200 passes in 120 minute match in UCL final

True Label: stats

Predicted Label: media

Confidence: 0.40

Analysis:

The post contains a performance statistic, but the model associated match-related language with the media category.

---

## Wrong Prediction 3

Post:

> 15 - Curaçao's Eloy Room recorded 15 saves against Ecuador, the most on record since 1966

True Label: stats

Predicted Label: media

Confidence: 0.41

Analysis:

The model failed to recognize record-setting statistical language because there were relatively few stats examples available during training.

---

# Reflection

My goal was to build a model capable of distinguishing between general soccer content, goal highlights, and statistical posts. While the model achieved 80.6% accuracy, the results show that it primarily learned the dominant media category rather than the distinctions between all three classes.

The most important lesson from this project is that higher overall accuracy does not necessarily indicate better classification performance. The confusion matrix revealed that the model classified every test example as media, which produced reasonable accuracy because media dominated the dataset.

The Groq zero-shot baseline outperformed the fine-tuned DistilBERT model. This demonstrates that large language models can perform very well on small classification tasks even without task-specific training.

Future improvements would include:

* Collecting more goal_clip examples
* Collecting more stats examples
* Balancing class frequencies
* Applying class weighting
* Increasing dataset size

---

# Spec Reflection

One aspect of the specification that helped me was the requirement to compare a fine-tuned model against a baseline. Without the baseline, I might have concluded that 80.6% accuracy represented strong performance. The baseline revealed that the fine-tuned model actually underperformed compared to a zero-shot LLM.

One way my implementation diverged from the original intention was the severe class imbalance in the dataset. Although I collected over 200 examples, most belonged to the media category. This imbalance heavily influenced the model's predictions and limited its ability to learn minority classes.

---

# AI Usage Disclosure

I used ChatGPT as a development assistant throughout this project.

Specific uses included:

1. Debugging Reddit data collection issues after receiving HTTP 403 errors and developing an alternative JSON download workflow.

2. Troubleshooting Git and GitHub issues, including diagnosing failed pushes caused by accidentally committing a 777 MB model checkpoint directory and safely removing those files from repository history.

3. Reviewing model evaluation results and helping interpret the effects of class imbalance on classification performance.

4. Assisting with README organization and documentation formatting.

All final labeling decisions, dataset construction, model training, evaluation, and project submission decisions were completed by me.
