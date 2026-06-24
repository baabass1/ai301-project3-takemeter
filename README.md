# ai301-project3-takemeter
AI301 Project 3 - TakeMeter

# TakeMeter: Soccer Post Classification with DistilBERT

## Overview

This project builds a text classification system for posts from the Reddit community r/soccer. The goal is to automatically classify posts into meaningful categories using a fine-tuned DistilBERT model and compare its performance against a zero-shot large language model baseline.

I chose r/soccer because it is one of the largest sports communities on Reddit and contains a diverse mix of news, match highlights, statistics, and fan discussions. This variety makes it a good community for a text classification task.

---

## Classification Labels

### media

General soccer news, interviews, fan moments, celebrations, reactions, photos, announcements, discussions, or non-statistical content.

Examples:

* "Lamine Yamal raises Palestine Flag during parade"
* "Norway's football team official photo for World Cup 2026"
* "Diogo Jota's last career goal"

### goal_clip

Posts describing a goal, scoring highlight, or match clip.

Examples:

* "USA [1] - 1 Germany - Antonee Robinson great goal 37'"
* "Argentina [3] - 0 Algeria - Lionel Messi 76' hat-trick"
* "Australia [1] - 0 Turkiye - Nystrom Irankunda 27'"

### stats

Posts focused on records, statistics, numerical achievements, historical comparisons, or performance metrics.

Examples:

* "15 - Curaçao's Eloy Room recorded 15 saves against Ecuador"
* "Arsenal completed less than 200 passes in 120 minute match in UCL final"
* "Manchester United has been eliminated from League Cup by Grimsby Town"

---

## Data Collection

Data was collected from r/soccer using Reddit JSON endpoints.

Files used:

* soccer_raw.json
* soccer_raw_2.json
* soccer_raw_3.json

The collected posts were manually labeled into three categories:

* media
* goal_clip
* stats

### Dataset Statistics

| Label     | Count |
| --------- | ----: |
| media     |   193 |
| goal_clip |    26 |
| stats     |    16 |
| Total     |   235 |

---

## Difficult Classification Examples

### Example 1

Post:

> "Diogo Jota's last career goal"

Challenge:

This post contains the word "goal" but refers to a newsworthy moment rather than a goal highlight clip. It was labeled as media.

### Example 2

Post:

> "15 - Curaçao's Eloy Room recorded 15 saves against Ecuador"

Challenge:

The post looks like a match report, but its primary purpose is communicating a record statistic. It was labeled as stats.

### Example 3

Post:

> "Argentina [3] - 0 Algeria - Lionel Messi 76' hat-trick"

Challenge:

The scoreline and timestamp strongly indicate a goal highlight despite also containing match information. It was labeled as goal_clip.

---

## Model

### Fine-Tuned Model

Model:

* DistilBERT (distilbert-base-uncased)

Hyperparameters:

* Epochs: 3
* Learning Rate: 2e-5
* Batch Size: 16
* Weight Decay: 0.01
* Warmup Steps: 50

Data Split:

* Train: 164 examples
* Validation: 35 examples
* Test: 36 examples

---

## Baseline Model

For comparison, I evaluated a zero-shot baseline using Groq's Llama 3.3 70B model.

Prompt summary:

* Define the three categories
* Provide one example for each category
* Ask the model to output only the label name

This baseline required no task-specific training.

---

## Results

### Fine-Tuned DistilBERT

Accuracy:

80.6%

Classification Report:

| Label     | Precision | Recall |   F1 |
| --------- | --------: | -----: | ---: |
| media     |      0.81 |   1.00 | 0.89 |
| goal_clip |      0.00 |   0.00 | 0.00 |
| stats     |      0.00 |   0.00 | 0.00 |

### Zero-Shot Baseline (Groq)

Accuracy:

88.9%

Classification Report:

| Label     | Precision | Recall |   F1 |
| --------- | --------: | -----: | ---: |
| media     |      0.96 |   0.90 | 0.93 |
| goal_clip |      0.57 |   1.00 | 0.73 |
| stats     |      1.00 |   0.67 | 0.80 |

### Comparison

| Model                   | Accuracy |
| ----------------------- | -------: |
| Groq Zero-Shot Baseline |    88.9% |
| Fine-Tuned DistilBERT   |    80.6% |

Difference:

-8.3 percentage points

---

## Error Analysis

Several errors occurred because the dataset was highly imbalanced.

### Error 1

Text:

> "USA [1] - 1 Germany - Antonee Robinson great goal 37'"

True Label:
goal_clip

Predicted:
media

Reason:

The model learned to heavily favor the media class because it dominated the training data.

### Error 2

Text:

> "15 - Curaçao's Eloy Room recorded 15 saves against Ecuador"

True Label:
stats

Predicted:
media

Reason:

The model struggled to recognize statistical record patterns due to the small number of stats examples.

### Error 3

Text:

> "Arsenal completed less than 200 passes in 120 minute match in UCL final"

True Label:
stats

Predicted:
media

Reason:

The model associated match-related language with media instead of identifying numerical performance information.

---

## Confusion Matrix

The confusion matrix is included as:

`confusion_matrix.png`

The matrix shows that the model correctly classified most media posts but struggled to distinguish minority classes.

---

## Reflection

This project demonstrated that fine-tuning does not always outperform larger foundation models. Despite training a DistilBERT classifier, the zero-shot Groq baseline achieved higher accuracy.

The main challenge was class imbalance. Over 82% of the dataset belonged to the media category, causing the model to favor that label during prediction. Future improvements would include collecting a larger dataset, balancing class frequencies, applying class weighting, and experimenting with additional training epochs.

---

## Spec Reflection

This project helped me understand the complete machine learning workflow, including data collection, labeling, dataset preparation, model fine-tuning, evaluation, and error analysis. I also learned the importance of strong baselines and how dataset quality can significantly affect model performance.

---

## AI Usage Disclosure

I used ChatGPT as a development assistant for:

* Debugging Python code
* Understanding Hugging Face fine-tuning workflows
* Troubleshooting Git and GitHub issues
* Reviewing evaluation results
* Improving project documentation

All dataset collection, labeling decisions, model training, evaluation, and final project verification were completed by me.
