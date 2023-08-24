cd ./app
docker build -t cdb-test-app --build-arg name=cdb-test-app .
docker run --name cdb-test cdb-test-app
cd ..