This is the documentation for the usage of deliverable APIs.
## Instruction For Build Environment

### Prepare all sources
```
git clone git@github.com:maybeLee/DNNTesting-Deliverables.git
cd DNNTesting-Deliverables
git clone git@github.com:maybeLee/MetaHand.git
git clone https://github.com/ForeverZyh/DEBAR.git
cd MetaHand/tools
git clone git@github.com:maybeLee/yolov7.git && cd ../../
cd DEBAR && \
curl -L -o dataset.zip 'https://drive.google.com/uc?export=download&id=1GBHFd-fPIBWqJOpIC8ZO8g3F1LoIZYNn' && \
unzip dataset.zip -d computation_graphs_and_TP_list && \
cd ../
```

### Build environments
```
# build container
docker build -t dnntesting -f MetaHand/Dockerfile .
docker run --ipc=host --name DNNTesting -ti -v ${PWD}:/root dnntesting:latest
apt-get update
apt-get install sudo pkg-config vim

# build debar environment
conda create -y -n debar python=3.5
conda activate debar
cd DEBAR && pip install -r requirements.txt
pip install --upgrade pip
pip install tensorflow==1.13.1
conda deactivate
cd ../

# build metahand environment
conda create -y -n metahand python=3.9
conda activate metahand
conda install -y pytorch==1.11.0 torchvision==0.12.0 torchaudio==0.11.0 cudatoolkit=11.3 -c pytorch
cd MetaHand && pip install -r requirements.txt && cd ../
cd MetaHand/tools/yolov7 && pip install -r requirements.txt

# exit the container while keeping it running
exit && docker start DNNTesting
```

### Initiate the interface
```
pip install -r requirements.txt
python gui.py
```

