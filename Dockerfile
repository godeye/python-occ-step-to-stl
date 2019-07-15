FROM mattshax/pythonocc
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
# COPY Miniconda3-latest-Linux-x86_64.sh /code/
# RUN bash Miniconda3-latest-Linux-x86_64.sh
# RUN pip install -r requirements.txt
COPY . /code/
# RUN sh -c '/bin/echo -e "yes\nyes" | install-curl.sh'
RUN yes | sudo apt-get update
RUN sudo apt-get install curl -y
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python get-pip.py
RUN pip install -r requirements.txt
COPY . /code/