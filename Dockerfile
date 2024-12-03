FROM rasa/rasa:3.6.20-full

USER root

WORKDIR /app

COPY ./ /app/

CMD ["run", "--enable-api", "--cors", "*"]