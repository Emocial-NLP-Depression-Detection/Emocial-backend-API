FROM nvidia/cuda:11.0-cudnn8-runtime-ubuntu16.04
ENV PATH="/root/miniconda3/bin:${PATH}"
ARG PATH="/root/miniconda3/bin:${PATH}"
ARG TWITTER_CONSUMER_KEY
ARG TWITTER_CONSUMER_SECRET
ARG TWITTER_ACCESS_TOKEN
ARG TWITTER_ACCESS_TOKEN_SECRET
ARG DJANGO_SECRET


ENV TWITTER_CONSUMER_KEY=$TWITTER_CONSUMER_KEY
ENV TWITTER_CONSUMER_SECRET=$TWITTER_CONSUMER_SECRET
ENV TWITTER_ACCESS_TOKEN=$TWITTER_ACCESS_TOKEN
ENV TWITTER_ACCESS_TOKEN_SECRET=$TWITTER_ACCESS_TOKEN_SECRET
ENV DJANGO_SECRET=$DJANGO_SECRET

RUN apt-get update && apt-get install -y htop python3-dev wget gcc mono-mcs
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh && mkdir root/.conda && sh Miniconda3-latest-Linux-x86_64.sh -b && rm -f Miniconda3-latest-Linux-x86_64.sh

RUN conda create -y -n ml python=3.8

RUN mkdir /code

COPY . code/
WORKDIR /code/
RUN /bin/bash -c "source activate ml && pip3 install -r requirements.txt"
RUN /bin/bash -c "source activate ml && python3 manage.py migrate"
CMD /bin/bash -c "source activate ml && python3 manage.py runserver 0.0.0.0:8000"
EXPOSE 8000