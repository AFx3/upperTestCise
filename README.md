# UpperTestCise
This flie explain how to run the test for CISE Adaptor

# Virtual Environment Setup and Dependencies installation

## Virtual Environment Setup

### Install Python Virtual Environment Module
```bash
sudo apt install python3.10-venv
```
### Create a Virtual Environment
```bash
python3 -m venv venv
```
### Activate the Virtual Environment
```bash
source venv/bin/activate
```
## Install Dependencies
```bash
pip3 install -r requirements.txt
```

# Run this script to send request to adaptor
```bash
python3 p5.py
```

# run this script to receive requests
```bash
uvicorn app:app --host 10.50.1.181 --port 8000 --workers 1 --log-level debug
```
# NB
app_just_pull_req_tested.py contains the previous code to handle the pull request only (to run it, rename the file in app.py)