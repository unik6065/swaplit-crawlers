FROM python

WORKDIR /usr/src/app

RUN pip install Scrapy
RUN pip install scrapy-splash
RUN pip install six
RUN pip install Pillow
RUN pip install boto
RUN pip install python-swiftclient
RUN pip install python-keystoneclient
RUN pip install pyyaml
