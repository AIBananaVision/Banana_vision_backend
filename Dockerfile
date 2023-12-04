FROM python:3.11

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./docker_requirements.txt .

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r docker_requirements.txt

COPY ./app .

EXPOSE 8000

CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
