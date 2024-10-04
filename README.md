# cpd-portal

## Installation Guide

Follow the steps below to install and run the project on your local machine.

### Prerequisites

- **Python 3.x**: Make sure Python is installed on your machine. You can download it from [python.org](https://www.python.org/downloads/).
- **Git**: Ensure that Git is installed on your machine. You can download it from [git-scm.com](https://git-scm.com/downloads).

### Step 1: Clone the Repository

First, clone the repository to your local machine using the following command:

```bash
git clone git@github.com:btg-automations/cpd-portal.git
```

### Step 2: Navigate into the Repository

Change into the project directory:

```bash
cd cpd-portal
```

### Step 3: Create a Virtual Environment

Create a virtual environment to isolate the project's dependencies:

```bash
python -m venv .venv
```

### Step 4: Activate the Virtual Environment
Windows:
```bash
.\venv\Scripts\activate

```
MacOS/Linux:
```bash
source venv/bin/activate
```

You should see (.venv) beside your username in your terminal.

### Step 5: Install the Required Packages:
Install the necessary packages from the requirements.txt file:
```bash
pip install -r requirements.txt
```

### Step 6: Add the Data Files
Create or add in `users.json` and `cpd_records.json` in the `\data` directory of the repository

### Step 7: Run the Application:
```bash
streamlit run main.py
```
