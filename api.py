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
        cmd = f"docker exec {self.container_name}  /bin/sh -c 'cd MetaHand && python -u -m scripts.evaluation.detect_parallel_yolov7" \
              f"--img_dir ${img_path} " \
              f"--weights_path ${weights_path} " \
              f"--size ${size} " \
              f"--confidence ${confidence} " \
              f"--jobs=8'"

        cmd = f"cd MetaHand && python -u -m scripts.evaluation.detect_parallel_yolov7 " \
              f"--img_dir ${img_path} " \
              f"--weights_path ${weights_path} " \
              f"--size ${size} " \
              f"--confidence ${confidence} " \
              f"--jobs=8"
        subprocess.call(cmd, shell=True)

    def train_yolov7(self, train_path, valid_path):
        pass
    
    def mutate_image(self, img_dir):
        pass


if __name__ == "__main__":
    container_name = "DNNTesting"
    dnnTest = DNNTest(container_name)
    # dnnTest.numerical_analysis("TensorFuzz.pbtxt")
    dnnTest.detect_yolov7("./MetaHand/tools/yolov7/coco/images/val2017/000000289222.jpg", "./MetaHand/tools/yolov7/runs/train/yolov7/weights/best.pt")
