


## Setup 
1. Make .env from .example.env and set your COHERE_API_KEY in the .env
2. If using VSCode, you may want to set your formatter. Your settings.json might include 
```
"[python]": {
    "editor.formatOnType": true,
    "editor.defaultFormatter": "ms-python.black-formatter"
}
```

3. Run the following.
```
poetry shell
poetry install
pre-commit install
pytest
```

Check that the pytest tests pass. If they do, you are good to go!

## Usage
When you open a new terminal, ensure you run the following.
```
poetry shell
```

If you want to pip install package XYZ run
```
poetry add XYZ
```

# TODO
* add in all summarised principles
* add validation to all stages (ie cannot continue if user input is not valid, or if user does not make a selection at dropdown, etc)
* add 'last substage' function
* 'force' go to bottom of chat after dropdown 