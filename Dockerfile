# Environment setup
FROM python:3.7
WORKDIR /app
COPY ./requirements.txt ./
RUN pip3 install -r requirements.txt

# Copy app
COPY ./app.py /app/
CMD python3 app.py
