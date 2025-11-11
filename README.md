# pt-tutor
Welcome to `pt-tutor`, the repository powering the Fala Português app! 

# About Fala Português! 
Fala Português is a Portuguese tutoring platform designed with the following principles:
1. Real-time feedback is super valuable _during_ foreign language conversations
2. Translating a message hot off the press drives comprehension
3. New vocabulary should be introduced gradually, with emphasis dedicated to previously 
used vocabulary so that learning is re-enforced
4. Language learning is most effective when it's categorized to real life circumstances
5. Everyone loves a good little game 
6. Audio (listening, speaking) is essential

# Configuring the app

## First setting up 

### 1. Poetry 
This repo uses Poetry for package management. 

If you DO NOT have Poetry installed yet, run in Terminal:
```bash
pip install poetry 

# to ensure Poetry is available by checking version
poetry --version  
```

If you DO have Poetry installed already, run in Terminal:
```bash
# to create a virtual env
poetry env activate 
# and paste result, for me it's:
source /Users/sbastek/pt-tutor/.venv/bin/activate

# to load packages
poetry install 
```

### 2. OpenAI 
This repo uses OpenAI large language models. 

Follow these steps to obtain necessary credentials:
1. Create an account with OpenAI if you don't already have one 
2. Once logged in, go to your profile and select "View API Keys" 
3. Create your `OPEN_API_KEY` by clicking "Create new secret key".
Copy and save on your computer this API key. Note it starts with `sk-...`
4. To get your `OPENAI_ORG_ID`, click back on your profile icon, select "Manage Account",
go to "Settings", and locate and save the `Organization ID` within Organization settings. 
Note it starts with `org-`


Next, create a `.env` file in the root directory of this report to house the revelant fields below. 

Finally, add in to `.env` the obtained credentials:
```bash
OPENAI_API_KEY=<your OpenAI API key>
OPENAI_ORG_ID=<your OpenAI Org ID>
```

### 3. Google Cloud
Google Cloud is used for speech-to-text and text-to-speech considering its 
library of European Portuguese voices. 

To use these capabilities, 
1. Create a Google Cloud profile
2. Create a Service Account 
3. Download a JSON file with all credentials
4. Store credentials in data/.streamlit/secrets.toml for local dev and 
   Streamlit > Settings > Secrets for cloud access.

## Updating  
Update packages with: 
```bash
poetry update
```

Add new package dependencies with: 
```bash
poetry add <package-name>  

# development dependency
poetry add -dev <package-name>
```

# Using the app 
To load the app locally, simply run the command below in Terminal.
```bash
streamlit run pt_tutor/app.py
```
