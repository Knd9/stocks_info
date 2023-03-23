FROM python:3.9.9

ENV PYTHONUNBUFFERED 1

# create an user for running apps only, so it doesnt use root
RUN useradd stock -m

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /stock
WORKDIR /stock

COPY ./stock /stock

USER stock

CMD ["uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8080"]