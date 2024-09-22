


## Setup 
1. Install Poetry if not already installed
2. Make .env from .example.env and set your COHERE_API_KEY in the .env
3. If using VSCode, set your formatter. Your settings.json might include something like 
```
"[python]": {
    "editor.formatOnType": true,
    "editor.defaultFormatter": "ms-python.black-formatter"
}
```
poetry shell
poetry install

pytest 
```

If you want to pip install package XYZ run 
```
poetry add XYZ
```

## Todo
GitHub actions?
