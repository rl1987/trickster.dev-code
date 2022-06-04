FROM python:3-slim

RUN pip3 install scrapy scrapyrt

RUN mkdir /books_to_scrape
ADD . /books_to_scrape
WORKDIR /books_to_scrape

EXPOSE 9080

ENTRYPOINT ["scrapyrt", "-i", "0.0.0.0"]
