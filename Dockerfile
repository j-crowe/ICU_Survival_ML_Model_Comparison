FROM gcr.io/tensorflow/tensorflow:latest-gpu

RUN apt-get update; \
        apt-get install -y \
    	python python-pip \
	python-numpy python-scipy \
	build-essential python-dev python-setuptools \
	emacs24 python-skimage \
	libssl-dev

#RUN update-alternatives --set libblas.so.3 \
#    /usr/lib/atlas-base/atlas/libblas.so.3; \
#    update-alternatives --set liblapack.so.3 \
#    /usr/lib/atlas-base/atlas/liblapack.so.3

RUN pip install -U scikit-learn
RUN pip install -U keras
RUN pip install -U flask
RUN pip install -U pandas
RUN pip install -U bs4
# We need to install the security extras for Python < 2.7.9
RUN pip install --upgrade requests[security]

VOLUME /tfModel/

EXPOSE 8888:8888
ENTRYPOINT /bin/bash