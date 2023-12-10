# Dockerfile
FROM python:3.11-slim
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.9.0/wait /wait
RUN chmod +x /wait
WORKDIR /src
COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
# Copy code and run web server
COPY docker-entrypoint.sh /src/
RUN chmod +x /src/docker-entrypoint.sh
COPY src /src

EXPOSE 5555
CMD ["./docker-entrypoint.sh"]
