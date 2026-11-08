FROM python:3.13-slim

WORKDIR /app

COPY csv-parser.py data.csv product.csv ./

ENTRYPOINT [ "python", "csv-parser.py" ]

CMD [ "data.csv" ]