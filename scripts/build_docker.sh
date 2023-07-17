docker build -t dnntesting -f Dockerfile .
docker run --name MetaHand -ti -v ${PWD}../:/root dnntesting:latest
apt-get update
apt-get install sudo pkg-config vim
