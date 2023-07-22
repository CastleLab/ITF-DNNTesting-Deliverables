## API 
import os
import subprocess
import shutil

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

    def evaluate_yolov7(
            self, data_dir="/root/MetaHand/tools/yolov7/pilotstudy",
            weights_path="/root/MetaHand/tools/yolov7/runs/train/pilotstudy_640/weights/best.pt",
            mutate_type="ObjectGaussianMutation",
            mutate_ratio="03",
            threshold=0.3
    ):
        log_dir = f"/root/MetaHand/logs/yolov7/{mutate_type}"
        output_dir = "/root/MetaHand/tools/yolov7/runs/detect"
        mutate_name = f"object_gaussian_160_fixMutRatio_centerXY_{mutate_ratio}"
        mutate_image = f"{data_dir}/{mutate_type}/{mutate_name}"
        origin_image = f"{data_dir}/images/train"
        origin_label = f"{data_dir}/labels/train"
        MR = 2
        os.makedirs(log_dir.replace("/root/", ""), exist_ok=True)
        os.makedirs(output_dir.replace("/root/", ""), exist_ok=True)
        cmd = f"podman exec {self.container_name} /bin/sh -c " \
              f"'" \
              f"cd MetaHand && CONDA_PREFIX=/opt/conda/envs/metahand PATH=/opt/conda/envs/metahand/bin:$PATH " \
              f"/opt/conda/envs/metahand/bin/python -u -m scripts.evaluation.evaluate " \
              f"-oi={origin_image} " \
              f"-mi={mutate_image} " \
              f"-ol={origin_label} " \
              f"-olf=yolov7 " \
              f"-w={weights_path} " \
              f"-od={output_dir} " \
              f"--dataset=yolov7 " \
              f"--mr={MR} " \
              f"--jobs=8 " \
              f"--threshold={threshold} > {log_dir}/{mutate_name}_{threshold}.log" \
              f"'"
        subprocess.call(cmd, shell=True)
        violation_path = f"/root/MetaHand/{mutate_name}_violations.txt"
        return violation_path

    def repair_yolov7(
            self,
            data_dir="/root/MetaHand/tools/yolov7/pilotstudy",
            weights_path="/root/MetaHand/tools/yolov7/runs/train/pilotstudy_640/weights/best.pt",
            mutate_type="ObjectGaussianMutation",
            mutate_ratio="03",
            threshold=0.3,
            img_size=640,
    ):
        violation_path = self.evaluate_yolov7(data_dir=data_dir, weights_path=weights_path, mutate_type=mutate_type, mutate_ratio=mutate_ratio)
        mutate_name = f"object_gaussian_160_fixMutRatio_centerXY_{mutate_ratio}"
        base_dir = f"/root/MetaHand/tools/yolov7/runs/train/{mutate_type}/{mutate_name}_{threshold}"
        v7_base = f"./runs/train/{mutate_type}/{mutate_name}_{threshold}"
        os.makedirs(base_dir.replace("/root/", ""), exist_ok=True)
        shutil.move(violation_path.replace("/root/", ""), os.path.join(base_dir.replace("/root/", ""), f"{mutate_name}_violations.txt"))

        # new train file will be saved in ./{base_dir}/train.txt
        cmd = f"podman exec {self.container_name} /bin/sh -c " \
              f"'" \
              f"cd MetaHand && CONDA_PREFIX=/opt/conda/envs/metahand PATH=/opt/conda/envs/metahand/bin:$PATH " \
              f"/opt/conda/envs/metahand/bin/python -u -m scripts.train.prepare_train_data " \
              f"--source_path={base_dir}/{mutate_name}_violations.txt " \
              f"--origin_source_path={data_dir}/train.txt " \
              f"--target_dir={base_dir} " \
              f"--dataset=yolov7 " \
              f"'"
        subprocess.call(cmd, shell=True)
        train_txt = f"{v7_base}/train.txt"
        src_yaml = os.path.join(data_dir, "data.yaml")
        dst_yaml = os.path.join(base_dir, "data.yaml")
        shutil.copy(src_yaml.replace("/root/", ""), dst_yaml.replace("/root/", ""))
        with open(dst_yaml, "r") as file:
            content = file.read().rstrip().splitlines()
        new_yaml = ""
        for line in content:
            if line.startswith("train:"):
                new_yaml += f"train: {train_txt}\n"
            else:
                new_yaml += line + "\n"
        with open(dst_yaml, "w") as file:
            file.write(new_yaml)
        self.train_yolov7(proj_name=f"yolov7_{mutate_name}", data_path=dst_yaml, img_size=img_size)


    def mutate_image(self, img_dir):
        pass


if __name__ == "__main__":
    container_name = "DNNTesting"
    dnnTest = DNNTest(container_name)
    # dnnTest.numerical_analysis("TensorFuzz.pbtxt")
    # path = dnnTest.detect_yolov7("/root/MetaHand/tools/yolov7/pilotstudy/images/val/ff1af9a2-frame2811.jpg", "/root/MetaHand/tools/yolov7/runs/train/pilotstudy/weights/best.pt")
    # dnnTest.train_yolov7(proj_name="pilotstudy", data_path="/root/MetaHand/tools/yolov7/pilotstudy/data.yaml")
    dnnTest.repair_yolov7()
