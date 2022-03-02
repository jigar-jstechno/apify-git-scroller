# First, specify the base Docker image.
# You can see the Docker images from Apify at https://hub.docker.com/r/apify/.
# You can also use any other image from Docker Hub.
#FROM apify/actor-python:3.9
FROM ubuntu:21.04
# Second, copy just requirements.txt into the actor image,
# since it should be the only file that affects "pip install" in the next step,
# in order to speed up the build
WORKDIR "/opt"
COPY requirements.txt ./
#RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz
#RUN tar -xvzf geckodriver*
#RUN chmod +x geckodriver
#RUN apt-get install unzip firefox
#RUN wget -N https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm
#RUN apt-get install alien -y
#RUN alien –i ./google-chrome-stable_current_x86_64.rpm
#RUN apt install ./google-chrome-stable_current_x86_64.rpm

#RUN wget -N http://chromedriver.storage.googleapis.com/2.26/chromedriver_linux64.zip
#RUN wget -N https://chromedriver.storage.googleapis.com/98.0.4758.102/chromedriver_linux64.zip
#RUN unzip chromedriver_linux64.zip
#RUN chmod +x chromedriver
#RUN apt-get install -y libgbm1 gconf-service libasound2 libatk1.0-0 libcairo2 libcups2 libfontconfig1 libgdk-pixbuf2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libxss1 fonts-liberation  libnss3 lsb-release xdg-utils apt-utils
#RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
#RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install

#RUN apt-get install -y \
#	apt-transport-https \
#	ca-certificates \
#	curl \
#	gnupg \
#	--no-install-recommends \
#	&& curl -sSL https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
#	&& echo "deb https://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
#	&& apt-get update && apt-get install -y \
#	google-chrome-stable \
#	fontconfig \
#	fonts-ipafont-gothic \
#	fonts-wqy-zenhei \
#	fonts-thai-tlwg \
#	fonts-kacst \
#	fonts-symbola \
#	fonts-noto \
#	fonts-freefont-ttf \
#	--no-install-recommends \
#	&& apt-get purge --auto-remove -y curl gnupg \
#	&& rm -rf /var/lib/apt/lists/*
#RUN apt install libglib2.0-dev libnss3 libgconf-2-4 libfontconfig1 snap chromium-browser -y
#RUN snap install chromium-browser
#RUN snap isntall chromium-chromedriver
#RUN deb http://deb.debian.org/debian experimental main
RUN apt-get update
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Kolkata
RUN apt-get install build-essential aptitude apt-utils -yf
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections
RUN apt-get install python3 python3-pip libjpeg-dev zlib1g-dev -yf   
# RUN python3 -m venv env
# RUN . env/bin/activate
#RUN source env\Scripts\activate

RUN apt-get install -yf git curl build-essential wget unzip xvfb
RUN apt-get install -yf fonts-liberation libasound2 libatk-bridge2.0-0 libatk1.0-0 libatspi2.0-0 libcups2 libdbus-1-3 libdrm2 libgbm1 libgtk-3-0 libnspr4 libnss3 libxcomposite1 libxdamage1 libxfixes3 libxkbcommon0 libxrandr2 xdg-utils
RUN curl https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o /chrome.deb
RUN dpkg -i /chrome.deb || apt-get install -yf
RUN rm /chrome.deb
RUN pip3 install apify-client pyvirtualdisplay xvfbwrapper pygifsicle
RUN pip3 install pygifsicle

RUN apt-get install gifsicle
# Install chromedriver for Selenium
#RUN curl https://chromedriver.storage.googleapis.com/2.31/chromedriver_linux64.zip -o /usr/local/bin/chromedriver
#RUN wget https://chromedriver.storage.googleapis.com/99.0.4844.35/chromedriver_linux64.zip
#RUN unzip chromedriver_linux64.zip
#RUN chmod +x /usr/local/bin/chromedriver
#RUN ln -s /usr/src/app/chromedriver /usr/local/share/chromedriver
#RUN ln -s /usr/src/app/chromedriver /usr/local/bin/chromedriver


#RUN ln -s /usr/src/app/chromedriver /usr/local/share/chromedriver 
#RUN cp /usr/src/app/geckodriver /bin/sh/geckodriver
#RUN geckodriver --version

#RUN wget -N https://chromedriver.storage.googleapis.com/99.0.4844.35/chromedriver_linux64.zip
RUN wget -N https://chromedriver.storage.googleapis.com/98.0.4758.102/chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip
RUN chmod +x chromedriver
#RUN ln -s chromedriver /usr/local/share/chromedriver
RUN cp chromedriver /usr/local/bin/chromedriver
RUN cp chromedriver /usr/local/share/chromedriver
RUN export PATH="/opt":$PATH
RUN pwd
RUN ls .
RUN git clone https://github.com/apify/apify-python;cd apify-python;python3 setup.py;cd ..

# Install the packages specified in requirements.txt,
# Print the installed Python version, pip version
# and all installed packages with their versions for debugging
RUN echo "Python version:" \
 && python3 --version \
 && echo "Pip version:" \
 && pip3 --version \
 && echo "Installing dependencies from requirements.txt:" \
 && pip3 install -r requirements.txt \
 && echo "All installed Python packages:" \
 && pip3 freeze

# Next, copy the remaining files and directories with the source code.
# Since we do this after installing the dependencies, quick build will be really fast
# for most source file changes.
COPY . ./

# Specify how to launch the source code of your actor.
# By default, the main.py file is run
CMD python3 final.py