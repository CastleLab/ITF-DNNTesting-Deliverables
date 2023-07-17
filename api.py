## API 
import os


class DNNTest(object):
    def __init__(self, container_name="DNNTesting"):
        self.container_name = container_name

    def numerical_analysis(self, model_path):
        if not model_path.endswith(".pbtxt"):
            raise ValueError(f"Invalid model: {model_path}. The model format should be pbtxt")
        os.system(f"podman exec {container_name} /bin/sh -c 'cd DEBAR && /opt/conda/envs/debar/bin/python analysis_main.py ./computation_graphs_and_TP_list/computation_graphs/{model_path}'")
    
    def train_yolov7(self, train_path, valid_path):
        pass
    
    def mutate_image(self, img_dir):
        pass


if __name__ == "__main__":
    container_name = "DNNTesting"
    dnnTest = DNNTest(container_name)
    dnnTest.numerical_analysis("TensorFuzz.pbtxt")

