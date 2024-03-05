FROM python:3.11-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./services/facade /code/facade
COPY ./utils /code/utils

ENV PYTHONPATH=${PYTHONPATH}:/code:/code/facade

CMD ["uvicorn", "facade_controller:app", "--host", "0.0.0.0", "--port", "8000"]