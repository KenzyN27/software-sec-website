FROM python:3.12.1-slim
WORKDIR /Website
COPY . /Website
RUN pip install --no-cache-dir -r packages.txt
EXPOSE 5001
RUN openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365 -subj "/CN=localhost"
ENV NAME World
CMD ["python","dockermain.py","--cert=cert.pem","--key=key.pem"]