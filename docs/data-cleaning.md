---
title: Data Analysis
layout: default
nav_order: 4
---

# Data Analysis

Data collected with this experiment template can be analysed using the **tripletTools** R package, which provides functions for cleaning, standardising, and modelling triadic comparison data.

[View tripletTools documentation](https://knowledge-and-concepts-lab.github.io/tripletTools/index.html){: .btn .btn-blue }

---

## What tripletTools provides

| Function | Purpose |
|----------|---------|
| `clean_triplet_data()` | Reads raw jsPsych CSV exports, applies quality-control exclusions, and returns a model-ready dataset |
| `clean_triadic_comparisons()` | Standardises legacy datasets from various column formats to the standard format |
| `filter_incomplete()` | Removes participants with too few trials |
| `filter_fast_responders()` | Removes participants with suspiciously fast mean reaction times |
| `filter_failed_catch()` | Removes participants who failed too many attention-check trials |
| `assign_sample_sets()` | Assigns trials to train/test splits for embedding models |

---

## Output format

Each participant's data is saved as a CSV by jsPsych-Pipe (or downloaded locally during testing). The key columns written by the experiment are:

| Column | Description |
|--------|-------------|
| `worker_id` | Participant identifier (from the `?workerId=` URL parameter, or a random session code for local runs) |
| `trial_category` | Trial type: `"random"`, `"check"`, or `"validation"` |
| `stimulus` | Target image path |
| `choices` | JSON array of the two choice image paths |
| `response` | Index of the chosen option (0 = left, 1 = right) |
| `rt` | Reaction time in milliseconds |
| `correct` | Whether the catch trial was answered correctly (check trials only) |
