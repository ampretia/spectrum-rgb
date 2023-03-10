FROM python:3.9
WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./aprox.txt /code
COPY ./colour_system.py /code
COPY ./main.py /code

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "3000"]