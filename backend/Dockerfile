FROM python:3
ADD . /backend
COPY . /backend
WORKDIR /backend
RUN pip install -r requirements.txt
CMD python app.py