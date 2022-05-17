FROM python:3.8.7-slim-buster

WORKDIR /code
COPY requirements.txt /etc/

RUN apt-get clean && apt-get update && apt-get install -y make && \
    pip install -r /etc/requirements.txt \
                --no-cache-dir

COPY ./ /code
COPY init.sh /code

EXPOSE 9879

RUN chmod +x /code/init.sh
CMD ["/code/init.sh"]