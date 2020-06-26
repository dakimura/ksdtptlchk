FROM python:3.7

RUN apt-get update && apt-get install -y unzip vim

#install google-chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add && \
    echo 'deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main' | tee /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && \
    apt-get install -y google-chrome-stable

WORKDIR /app

ADD . /app

#install ChromeDriver
RUN mkdir /opt/chrome
# ADD https://chromedriver.storage.googleapis.com/2.45/chromedriver_linux64.zip /opt/chrome/
ADD https://chromedriver.storage.googleapis.com/83.0.4103.39/chromedriver_linux64.zip /opt/chrome/
RUN cd /opt/chrome/ && \
    unzip chromedriver_linux64.zip

ENV PATH $PATH:/opt/chrome
RUN cd /app

RUN pip install --trusted-host pypi.python.org -r requirements.txt

#CMD ["python", "app.py"]