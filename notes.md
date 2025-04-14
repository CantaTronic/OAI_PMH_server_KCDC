# venv and requirements
```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

# Run server
`uvicorn main:app --host 0.0.0.0 --port 8000`

# Docker

## build image
`sudo docker build -t oai-pmh .`

## run container
`sudo docker run --name oai-pmh-kcdc -p 8000:8000 -d oai-pmh`

# Swagger
автоматич документация к апи + тестирование запросов
`http://0.0.0.0:8000/docs`

# Parameters
Тестирование API

## OAI-PMH Verbs:
- ListMetadataFormats
- ListIdentifiers
- GetRecord
- ListRecords

## metadataPrefix
oai_dc



