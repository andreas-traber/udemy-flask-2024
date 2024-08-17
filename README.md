# udemy-flask-2024

## Introduction

This code was created while doing https://www.udemy.com/course/rest-api-flask-and-python/
### Note
Since this comes from a basics course, there are obviously a few issues with the code. E.g. the store-tags-items datamodel, secrets should not be stored in a py-file, there are no unittests(It was tested using [Insomnia](https://app.insomnia.rest/))

## Building
### Virtual Environment
**Note:** This project was developed using python 3.12.3
```
python -m venv venv 
source venv/bin/activate
pip install -r requirements.txt
```

### Docker Compose
```
docker compose build 
```

## Running
### Virtual Environment
Make sure, you are have activated the environment with `source venv/bin/activate`

```
flask run
```

### Docker Compose
```
docker compose up 
```
