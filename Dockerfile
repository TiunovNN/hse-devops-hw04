# Dockerfile
FROM python:3.11
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.9.0/wait /wait
RUN chmod +x /wait
WORKDIR /src
COPY requirements.txt /requirements.txt
RUN pip install -r requirements
# Copy code and run web server
COPY src /src
EXPOSE 80
CMD ["./docker-entrypoint.sh"]
