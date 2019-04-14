FROM python:3

WORKDIR /lrucache_api
COPY . /lrucache_api

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 80

CMD [ "python", "-m", "lrucache_api.cache_service" ]