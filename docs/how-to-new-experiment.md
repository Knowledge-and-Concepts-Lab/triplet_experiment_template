---
title: How to Set Up a New Experiment
layout: default
nav_order: 3
---

# How to Set Up and Run a New Experiment

This guide walks through every step needed to adapt this template for a new triadic comparison experiment — from preparing stimuli to collecting and cleaning data.

---

## Overview

Each trial shows participants three images: one **target** (top) and two **choices** (bottom). Participants click (or press a key) to select which choice is most similar to the target. The experiment is built on [jsPsych](https://www.jspsych.org/) v7.3.4 and uses [jsPsych-Pipe](https://pipe.jspsych.org/) to save data server-side.

**The workflow for setting up a new experiment is:**

1. Create a study directory under `my_studies/`.
2. Copy `experiment.yaml` into it and edit your settings.
3. Add your stimuli images and consent form.
4. Run the generator — it copies the shared template files and writes `config.js` and `stimuli.js` into your study directory.
5. Test locally, then deploy the study directory.

**Never edit the generated `config.js` or `stimuli.js` directly** — they are overwritten every time you run the generator.

---

## File responsibilities

| File | Role |
|------|------|
| `my_studies/<study>/experiment.yaml` | **Edit this.** All researcher-facing settings in one place. |
| `scripts/generate_experiment.js` | Generator — run it with your study path to build the experiment. |
| `my_studies/<study>/js/config.js` | Auto-generated — do not edit. |
| `my_studies/<study>/js/stimuli.js` | Auto-generated — do not edit. |
| `my_studies/<study>/assets/stimuli/` | Your stimulus image files. |
| `my_studies/<study>/assets/consent/` | Your consent form image. |
| `my_studies/<study>/index.html` | Copied from the template by the generator. Only edit the shared template (`experiment/index.html`) if you need to change the demographic questions or overall flow, then re-run the generator to propagate the change. |

---

## Step 1: Install dependencies

If you have not already done so, install the Node dependencies from the repo root:

```bash
npm install
```

This only needs to be done **once** — not for each new study.

---

## Step 2: Create your study directory

```bash
mkdir my_studies/my_new_study
```

Then copy the template config into it:

```bash
cp experiment.yaml my_studies/my_new_study/experiment.yaml
```

---

## Step 3: Prepare your stimuli

### 3a. Add your images

Create `my_studies/my_new_study/assets/stimuli/` and copy your images there. Supported formats: `.png`, `.jpg`, `.jpeg`, `.gif`, `.bmp`, `.webp`, `.svg`. You need at least 3 images to run the experiment.

The generator scans this directory automatically and sorts files alphabetically — you do not need to list them anywhere.

### 3b. Set `stimuli_dir` in your `experiment.yaml`

```yaml
stimuli_dir: assets/stimuli
```

In study mode, `stimuli_dir` is relative to your study directory (not the repo root), so `assets/stimuli` points to `my_studies/my_new_study/assets/stimuli/`.

### 3c. Define your validation trials

Validation trials are predefined triplets used for quality control (e.g., cross-participant consistency checks). The `validation_trials` field in `experiment.yaml` is **optional**:

**Option 1 — auto-generate (default for new experiments)**

Omit `validation_trials` entirely, or set it to an empty list. The setup script will randomly select `n_validation_trials` triplets from your stimuli directory each time you run `npm run setup`:

```yaml
# validation_trials:   ← omit this, or write:
validation_trials: []
```

New triplets are drawn every time `npm run setup` runs, so re-running the script will produce a different random set.

**Option 2 — specify explicitly**

List the triplets you want. Paths are relative to `experiment/` (the same root as `index.html`). You must supply at least `n_validation_trials` entries; if you provide more, the experiment samples from them at runtime:

```yaml
validation_trials:
  - stimulus: assets/stimuli/your_target.png
    choice1:  assets/stimuli/option_a.png
    choice2:  assets/stimuli/option_b.png
  # ... add at least n_validation_trials entries
```

---

## Step 4: Configure the experiment

All settings live in your study's `experiment.yaml`. The sections below cover the ones you are most likely to change.

### Data pipeline (required)

Create a project at [pipe.jspsych.org](https://pipe.jspsych.org/) to get your experiment ID.

```yaml
experiment_id: "YOUR_PIPE_EXPERIMENT_ID"
filename_prefix: "your_study_name"
```

Each participant's data is saved as a CSV named `<filename_prefix>_<random_code>.csv`.

### SONA integration (required for credit granting)

Find these values in your SONA study's "Automated Credit Granting" settings.

```yaml
sona_base_url: "https://uwmadison.sona-systems.com/webstudy_credit.aspx"
sona_experiment_id: "YOUR_SONA_STUDY_ID"
sona_credit_token: "YOUR_CREDIT_TOKEN"
```

On completion, participants are automatically redirected to the SONA credit URL. Their SONA ID is read from the `?workerId=` URL parameter — make sure your SONA study appends it to the experiment URL.

### Trial counts

```yaml
n_random_trials: 550    # 3 random images — no correct answer
n_check_trials: 20      # attention checks — target repeats as one choice
n_validation_trials: 50 # drawn from your validation_trials list
n_main_trials: 620      # MUST equal the sum of the three above
```

The generator will error if `n_main_trials` does not equal the sum of the other three.

### Response mode

```yaml
response_mode: button      # "button" (default) or "keyboard"
response_keys: [f, j]     # left/right keys — only used in keyboard mode
```

### Timing

```yaml
min_rt_ms: 900             # responses faster than this trigger a speed warning
fixation_duration_ms: 500  # fixation cross duration before each trial
post_instruction_gap_ms: 2000
post_demographic_gap_ms: 1000
max_load_time_ms: 120000   # how long to wait for images to preload
```

### Consent form

```yaml
consent_image_path: "assets/consent/your_consent_form.png"
consent_button_text: "Consent & Continue"
```

### UI text

All participant-facing text is in `experiment.yaml`. Two fields support runtime placeholders:

- `instructions_html` — use `{{N_MAIN_TRIALS}}` and it will be replaced with the actual trial count.
- `secret_code_html` — use `{{SECRET_CODE}}` and it will be replaced with the participant's completion code.

The secret code is only shown when the `workerId` URL parameter is longer than `worker_id_min_length` characters (default: 7). This prevents it appearing during local testing.

---

## Step 5: Generate the experiment files

After editing your `experiment.yaml`, run the generator with the path to your study directory:

```bash
node scripts/generate_experiment.js my_studies/my_new_study
```

The generator:
- Copies `index.html` and `js/utils.js` from the shared template into your study directory.
- Validates your settings and reports any errors (mismatched trial counts, missing validation trials, stimuli directory not found, etc.).
- Writes `js/config.js` and `js/stimuli.js` into your study directory.

Re-run this command whenever you edit `experiment.yaml` or change your stimuli.

---

## Step 6: Test locally

The experiment must be served over HTTP — opening `index.html` as a `file://` URL will not work.

```bash
# Python (no install needed)
cd my_studies/my_new_study && python -m http.server 8000

# Node.js
npx serve my_studies/my_new_study
```

Open `http://localhost:8000` in your browser.

**Testing tips:**

- Add a fake worker ID to skip SONA: `http://localhost:8000?workerId=test1234`
- For a shorter test session, temporarily reduce `n_random_trials` in your `experiment.yaml` (and adjust `n_main_trials` to match), then re-run the generator.
- Run the unit test suite to verify utility functions are correct (run from the repo root):

```bash
npm test
```

---

## Step 7: Deploy

After running the generator, your study directory is a self-contained static site. Deploy it to any static file host:

- **GitHub Pages** — push the study directory to a `gh-pages` branch, or configure Pages to serve from that subdirectory.
- **Netlify / Vercel** — drag and drop the study directory or connect a repository containing it.
- **University web server** — upload the study directory via SFTP.

Ensure the host uses HTTPS, as jsPsych-Pipe requires it.

After deploying, give SONA the URL with the `%SURVEY_CODE%` placeholder appended as `?workerId=%SURVEY_CODE%` so SONA passes each participant's ID into the experiment automatically.

---

## Step 8: Collect and analyse data

### Downloading data

Log in to your [jsPsych-Pipe](https://pipe.jspsych.org/) project to download individual CSV files, or use the Pipe API to batch-download them.

### Analysing data

To clean and analyse data collected with this template, use the **tripletTools** R package:

[tripletTools documentation](https://knowledge-and-concepts-lab.github.io/tripletTools/index.html){: .btn .btn-blue }

The key function is `clean_triplet_data()`, which reads the raw CSVs, applies quality-control exclusions, and returns a model-ready dataset:

```r
library(tripletTools)
result <- clean_triplet_data(
  data_dir      = "path/to/downloaded/csvs",
  output_df     = "cleaned_data.csv",
  output_levels = "levels.csv"
)
```

See the [Data Analysis](data-cleaning) page for a description of the output format.

---

## Quick reference: experiment.yaml settings

| Setting | Default | Notes |
|---------|---------|-------|
| `stimuli_dir` | `assets/stimuli` | Path to images, relative to your study directory |
| `validation_trials` | *(list)* | Must have ≥ `n_validation_trials` entries |
| `page_title` | `"Triadic Judgment Task"` | Browser tab title |
| `response_mode` | `"button"` | `"button"` or `"keyboard"` |
| `response_keys` | `[f, j]` | Left/right keys for keyboard mode |
| `n_random_trials` | `550` | |
| `n_check_trials` | `20` | |
| `n_validation_trials` | `50` | |
| `n_main_trials` | `620` | Must equal sum of above three |
| `min_rt_ms` | `900` | Faster responses trigger speed warning |
| `fixation_duration_ms` | `500` | |
| `post_instruction_gap_ms` | `2000` | |
| `post_demographic_gap_ms` | `1000` | |
| `max_load_time_ms` | `120000` | |
| `fixation_symbol` | `"+"` | |
| `experiment_id` | — | From jsPsych-Pipe dashboard |
| `filename_prefix` | — | Prefix for saved CSV files |
| `sona_base_url` | UW-Madison URL | Change for other institutions |
| `sona_experiment_id` | — | From SONA study settings |
| `sona_credit_token` | — | From SONA automated credit granting |
| `secret_code` | — | Shown to participants on completion |
| `worker_id_min_length` | `7` | Min URL param length to show secret code |
| `consent_image_path` | — | Path to consent form image |
| `consent_button_text` | `"Consent & Continue"` | |
