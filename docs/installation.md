---
title: Installation & Prerequisites
layout: default
nav_order: 2
---

# Installation & Prerequisites

## How this repo works

You install this repository **once** on your machine. It acts as the shared engine for all your triadic comparison experiments. Each individual study lives in its own subdirectory under `my_studies/` — you never need to re-install or duplicate the repo for a new study.

```
triplet_experiment_template/   ← install this once
└── my_studies/
    ├── study_A/               ← your first study
    └── study_B/               ← your second study
```

The generator script reads a study's `experiment.yaml`, assembles the experiment files, and writes them into the study directory. See [How to Set Up a New Experiment](how-to-new-experiment) for the full walkthrough.

---

## Components

This project has three independent components, each with its own dependencies. Install only what you need for the tasks you plan to do.

| Component | What it does | Requires |
|-----------|-------------|---------|
| Experiment setup | Generates `config.js` and `stimuli.js` from `experiment.yaml` | Node.js |
| Experiment preview | Serves the experiment locally for testing | Node.js or Python |
| JavaScript tests | Runs the `utils.js` / `config.js` / `stimuli.js` unit tests | Node.js |
| Docs preview | Builds and serves this documentation site locally | Ruby |

For data analysis, see the [tripletTools R package](https://knowledge-and-concepts-lab.github.io/tripletTools/index.html).

---

## Node.js

Required for: experiment setup (`npm run setup`), JS tests (`npm test`), and serving the experiment locally (`npx serve`).

### Install

1. Go to [nodejs.org](https://nodejs.org) and download the **LTS** installer for Windows.
2. Run the installer, accepting all defaults. Ensure "Add to PATH" is checked.
3. Open a new terminal and verify:

```bash
node --version   # should print v20 or higher
npm --version    # should print 10 or higher
```

### Project setup

From the project root, install the project's Node dependencies once:

```bash
npm install
```

This installs `js-yaml` (used by the generator script) and `vitest` (used by the test suite).

---

## Ruby

Required for: previewing the documentation site locally.

Not needed to run the experiment or run tests — only install this if you want to work on the documentation.

### Install

1. Go to [rubyinstaller.org/downloads](https://rubyinstaller.org/downloads/) and download the latest **Ruby+Devkit x64** installer (the recommended version is highlighted).
2. Run the installer, accepting all defaults. Leave "Add Ruby executables to your PATH" checked.
3. At the final screen, leave the checkbox ticked to run `ridk install`. In the window that opens, type `3` and press Enter to install MSYS2 and MINGW development tools. Wait for it to complete, then close the window.
4. Open a **new** terminal and verify:

```bash
ruby --version    # should print ruby 3.x.x
bundle --version  # should print Bundler version 2.x.x
```

### Install documentation dependencies

From the `docs/` directory, install the Ruby gems once:

```bash
cd docs
bundle install
```

### Preview the docs locally

```bash
bundle exec jekyll serve
```

Then open `http://localhost:4000`. Jekyll will watch for file changes and rebuild automatically.

---

## Python (optional)

Python is an alternative way to serve the experiment locally for testing. It is not required if you have Node.js installed (you can use `npx serve` instead).

### Check if Python is already installed

```bash
python --version
```

Python 3.x is pre-installed on many Windows systems. If the command is not found, download the installer from [python.org](https://www.python.org/downloads/) and ensure "Add Python to PATH" is checked during installation.

### Serve the experiment with Python

```bash
cd experiment
python -m http.server 8000
```

Then open `http://localhost:8000`.
