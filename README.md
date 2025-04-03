# pt-tutor
Welcome to `pt-tutor`, the repo powering the Fala Português app! 

# About Fala Português! 
Fala Português is a Portuguese tutoring platform designed with the following principles:
1. Real-time feedback is super valuable _during_ foreign language conversations
2. New vocabulary should be introduced gradually, with emphasis dedicated to previously used vocabulary so that learning is re-enforced
3. Language learning is most effective when it's categorized to real life circumstances
4. Eeryone loves a good little progress bar 

# Configuring

## Initially setting up 

### 1. Poetry 
This repo uses Poetry for package management. 

If you DO NOT have Poetry installed yet, run in Terminal:
```bash
pip install poetry 

# ensure Poetry is available by checking version
poetry --version  
```

If you DO have Poetry installed already, run in Terminal:
```bash
# to create a virtual env
poetry shell 

# to load packages
poetry install 
```

### 2. OpenAI 
This repo uses OpenAI large language models. 

First create a `.env` file to house the revelant fields below. 

Then add to this file your OpenAI credentials:
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
## Planned for Release 2 (April 2025)
- [ ] Add voice experience
- [ ] Add toggle so user can choose text or voice interaction

## Planned for Release 3 (May 2025)
- [ ] Improve vocab recognition
  - [ ] Accommodate multiple word vocab
  - [ ] Include vocab variants (o/os/a/as, verb conjugations)
- [ ] Add "Beginner Mode" where you speak English and response is in Portuguese 
