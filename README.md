# pt-tutor
Welcome to `pt-tutor`, the repository powering the Fala Português app! 

# About Fala Português! 
Fala Português is a Portuguese tutoring platform designed with the following principles:
1. Real-time feedback is super valuable _during_ foreign language conversations
2. New vocabulary should be introduced gradually, with emphasis dedicated to previously 
used vocabulary so that learning is re-enforced
3. Language learning is most effective when it's categorized to real life circumstances
4. Eeryone loves a good little progress bar 

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

# Roadmap 
## Planned for Release 2 (Aug 29 2025)
- [ ] Add voice experience
- [ ] Add toggle so user can choose text or voice interaction

## Planned for Release 3 (Aug 31 2025)
- [ ] Add "Translate last response" button
- [ ] Add "Enhanced Corrector" feedback showing ideal phrasing 

## Planned for Release 4 (Sep 7 2025)
- [ ] Add "Beginner Mode" where you speak English and response is in Portuguese 

## Planned for Release 5 (Sep 14 2025)
- [ ] Add ability to submit custom topic with auto-generated words
- [ ] Improve vocab recognition
  - [ ] Accommodate multiple word vocab
  - [ ] Include vocab variants (o/os/a/as, verb conjugations)
