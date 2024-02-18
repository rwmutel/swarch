FROM python:3.11-slim

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./task_4 /code/task_4

# CMD ["python", "task_4/concurrent_no_locks.py"]
# CMD ["python", "task_4/concurrent_pessimistic.py"]
CMD ["python", "task_4/concurrent_optimistic.py"]