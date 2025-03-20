# pt-tutor
Welcome to Fala Português! 

## About Fala Português! 

This is a Portuguese tutoring platform designed with the following principles:
1. Real-time feedback is super valuable _during_ foreign language conversations
2. New vocabulary should be introduced gradually, with emphasis dedicated to previously used vocabulary so that learning is re-enforced
3. Language learning is most effective when it's categorized to real life circumstances
4. Games are fun and everyone loves a good little scoreboard 

## Setup

### Activating Poetry virtual env
Use Poetry for package management. 

#### If you DO NOT have Poetry installed yet
Run:
```bash
pip install poetry 

# ensure Poetry is available by checking version
poetry --version  
```

#### If you already have Poetry installed
Run:
```bash
# to create a virtual env
poetry shell 

# to load packages
poetry install 
```

### Updating virtual env
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

### Using OpenAI
First create a `.env` file to include the relevant keys.

Then add OpenAI credentials:
```bash
OPENAI_API_KEY=<your OpenAI API key>
OPENAI_ORG_ID=<your OpenAI Org ID>
```

## Using the app 
```bash
streamlit run pt_tutor/app.py
```

## Roadmap 
### Outstanding tasks for Release 1 (March 2025)
- [X] Improve primary chat window interface
  - [X] Chat input at the bottom, chat history of size 500 pixes above
  - [X] User is dark red; Bot is dark green
  - [X] Adding corrections under user input in slightly different font
  - [X] Improve (remove?) icons
  - [X] Show rolling message history
- [X] Collect vocab words by topic [PT Tutor vocab](https://docs.google.com/spreadsheets/d/15A-ee4YKTUvd9vptD1-wfwPkyFaGftiOaIzQfeDx9F8/edit?gid=1330781019#gid=1330781019)
  - [X] Dining out 
  - [X] Weekend recap 
  - [X] Weather
- [X] Scorecard
  - [X] Update scorer to check against category vocab 
  - [X] 3 successful uses = mastery
  - [X] Add progress bar (mastered words / total vocab)
  - [X] Add ability to see unmastered vocab
  - [X] Add progress saver
- [X] Update prompt to focus on mastered vocab to reinforce learning
- [X] Parameterize topic 
- [X] Single word vocab only
- [X] Save last correct word
- [X] Host on website
- [ ] Parameterize user 
- [ ] Save progress via Google Sheets

### Planned for Release 2 (April 2025)
- [ ] Add voice option
- [ ] Add toggle so user can choose text or voice interaction
- [ ] Accommodate multiple word vocab
- [ ] Add 2 more categories (5 total)
- [ ] Include non-present verb vocab 

### Planned for Release 3 (May 2025)
- [ ] Add "Beginner Mode" where you speak English and response is in Portuguese 
