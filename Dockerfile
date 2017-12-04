FROM python:3.5
WORKDIR /
ADD . /
RUN pip install --upgrade -r requirements.txt
ENTRYPOINT ["python", "bot.py"]
