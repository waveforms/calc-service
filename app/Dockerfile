FROM python:3.7

EXPOSE 5000

WORKDIR /app

COPY requirements.txt /app
RUN pip install -r requirements.txt


COPY / /app/


RUN ls -la /app/*


ENV foo=/bar
ENV FLASK_APP=calcservice.py
ENV FLASK_ENV=development

CMD cd backend &&  python -m flask run --host 0.0.0.0
