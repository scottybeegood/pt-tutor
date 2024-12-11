# pt-tutor
Portuguese tutoring app

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
Add new package dependencies with: 
```bash
poetry add <package-name>  

# development dependency
poetry add -dev <package-name>
```

### Using OpenAI
First create a `.env` file to include the relevant keys.

Add your `OPENAI_API_KEY` and ``

Then add OpenAI credentials:
```bash
OPENAI_API_KEY=<your OpenAI API key>
OPENAI_ORG_ID=<your OpenAI Org ID>
```

## Using the app 
### to run Jupyter notebooks:
```bash
poetry run jupyter lab
```

### to run Python files: 
```bash
poetry run python <filename> 

# to run the dash_app.py app
poetry run python pt_tutor/dash_app.py
```