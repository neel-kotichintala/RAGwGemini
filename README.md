# Setup
For setting up to run the code properly after completion. We will be forking, cloning the repository and then creating a virtual environment. 

# Getting Started with the Project

Welcome! This guide will help you **fork** this repository and set it up on your **local machine** so you can start working on your solution.

---

## Step 1: Fork the Repository

1. Go to the main page of this repository (the one you’re viewing right now).  
2. In the top-right corner of the page, click the **Fork** button.  
3. Choose your personal GitHub account.  
4. GitHub will create a **copy of this repo under your account** — this is now your workspace.  

> You will make *all changes* in your own forked repository.

---

## Step 2: Clone Your Fork Locally

Once your fork is created, you’ll want to download it to your computer.

1. Go to your forked repo on GitHub.  
2. Click the green **Code** button, then copy the HTTPS or SSH link.  
3. Open your terminal and run:

```bash
# Example (HTTPS)
git clone https://github.com/<your-username>/<repo-name>.git

# Example (SSH)
git clone git@github.com:<your-username>/<repo-name>.git
```

## 3.Package Installation
In the same directory as the rest of your files, open the terminal and run the following commands:

ON MAC/LINUX:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

ON WINDOWS (POWERSHELL):
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 4. Google AI API Setup

### 4.a Create Google Cloud Project on
https://console.cloud.google.com/

### 4.b Create Google AI API Key 
[Create API Key & Create New Project](https://aistudio.google.com/u/2/api-keys)
> **Note:** Click on "Create API Key" then create a new cloud project

### 4.c Add API Key to .env file 

## Running the Server
After completely filling in the question marks in the main.py file, you are ready for running the server!
Ensure that you are inside the virtual environment created above (Check for (.venv) in the beginning of your prompt, otherwise activate the venv using the command given above)
Then run

ON MAC/LINUX
```bash
python3 -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

ON WINDOWS (POWERSHELL)
```bash
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

## Trying it out!
If everything works correctly, the backend and frontend should be running together on http://127.0.0.1:8000
