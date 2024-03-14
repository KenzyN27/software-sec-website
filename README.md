This is a software security project.

Execute the docker container with:
docker run -d -p 5000:5000 softwaresecwebsite

To delete containers
docker rm -v -f $(docker ps -qa)

To delete images
docker rmi -f $(docker images -aq)

open gitbash and run
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
for cert/key