FROM eclipse-temurin:21-jdk
WORKDIR /app
COPY CsvParser.java data.csv product.csv ./
ENTRYPOINT [ "java", "CsvParser.java" ]
CMD [ "data.csv" ]