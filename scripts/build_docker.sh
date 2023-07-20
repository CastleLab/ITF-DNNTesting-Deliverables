docker build -t dnntesting -f MetaHand/Dockerfile .
docker run --ipc=host --name DNNTesting -ti -v ${PWD}:/root dnntesting:latest
apt-get update
apt-get install sudo pkg-config vim
