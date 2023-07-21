## API 
import os
import subprocess

class DNNTest(object):
    def __init__(self, container_name="DNNTesting"):
        self.container_name = container_name

    def numerical_analysis(self, model_name):
        if not model_name.endswith(".pbtxt"):
            raise ValueError(f"Invalid model: {model_name}. The model format should be pbtxt")
        cmd = f"docker exec {self.container_name} /bin/sh -c 'python analysis_main.py ./computation_graphs_and_TP_list/computation_graphs/{model_name}'"
        result = subprocess.check_output(cmd, shell=True)
        return result

    def detect_yolov7(self, img_path, weights_path, size=320, confidence=0.25):
        assert img_path.endswith(".jpg")
        cmd = f"docker exec {self.container_name}  /bin/sh -c 'cd MetaHand && CONDA_PREFIX=/opt/conda/envs/metahand PATH=/opt/conda/envs/metahand/bin:$PATH /opt/conda/envs/metahand/bin/python -m scripts.evaluation.detect_parallel_yolov7 " \
              f"--img_dir {img_path} " \
              f"--weights_path {weights_path} " \
              f"--size {size} " \
              f"--confidence {confidence} " \
              f"--jobs=8'"
        subprocess.call(cmd, shell=True)
        img_name = os.path.basename(img_path)
        res_path = f"./MetaHand/tools/yolov7/runs/detect/{img_name}/{img_name}"
        return res_path

    def train_yolov7(self, proj_name="pilotstudy", data_path="/root/MetaHand/tools/yolov7/pilotstudy/data.yaml", img_size=640, batch_size=42, num_workers=4, cfg_path="cfg/training/yolov7.yaml"):
        # The path can be an absolute path or relative path with the root to be ./MetaHand/tools/yolov7
        if not os.path.exists(data_path):
            if not os.path.exists(data_path.replace("/root", os.getcwd())):
                raise ValueError(f"The data path: {data_path} does not exist!")
        cmd = f'podman exec {self.container_name}  /bin/sh -c \'cd MetaHand/tools/yolov7 && /opt/conda/envs/metahand/bin/python -m torch.distributed.launch ' \
              f'--nproc_per_node 3 --master_port 9527 train.py --workers {num_workers} --device 1,0,2 ' \
              f'--sync-bn --batch-size {batch_size} --data {data_path} ' \
              f'--img {img_size} --cfg {cfg_path} --weights "" ' \
              f'--name {proj_name} --hyp data/hyp.scratch.p5.yaml\''
        subprocess.call(cmd, shell=True)

    def mutate_image(self, img_dir):
        pass


if __name__ == "__main__":
    container_name = "DNNTesting"
    dnnTest = DNNTest(container_name)
    # dnnTest.numerical_analysis("TensorFuzz.pbtxt")
    path = dnnTest.detect_yolov7("/root/MetaHand/tools/yolov7/pilotstudy/images/val/ff1af9a2-frame2811.jpg", "/root/MetaHand/tools/yolov7/runs/train/pilotstudy/weights/best.pt")
    print(path)
    # dnnTest.train_yolov7(proj_name="pilotstudy", data_path="/root/MetaHand/tools/yolov7/pilotstudy/data.yaml")
