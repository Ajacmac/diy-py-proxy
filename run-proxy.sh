cd ./proxy
docker build -t proxy --build-arg name=proxy .
docker run -p 7500:7500 --name proxy-container proxy
cd ..