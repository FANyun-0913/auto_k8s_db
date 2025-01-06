import yaml
import os


def generate_pv(config):
    # 定义变量
    name = config['name']
    namespace = config['namespace']
    storage_capacity = config['storage_capacity']

    # 定义目录路径
    directory_path = "/nfs/" + name
    print(directory_path)

    # 检查目录是否存在，如果不存在则创建
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)
        print(f"创建目录 {directory_path} ")
    else:
        print(f" {directory_path} 已存在")

    # 定义YAML数据结构
    yaml_data = {
        "apiVersion": "v1",
        "kind": "PersistentVolume",
        "metadata": {
            "name": name + "-pv",
            "namespace": namespace
        },
        "spec": {
            "capacity": {
                "storage": storage_capacity
            },
            "accessModes": [
                "ReadWriteMany"
            ],
            "nfs": {
                "server": "172.24.223.63",
                "path": "/nfs/" + name
            },
            "storageClassName": "nfs"
        }
    }

    # 将数据结构转换为YAML字符串
    yaml_string = yaml.dump(yaml_data)

    # 指定完整的文件路径
    file_path = os.path.join("/kube/config/yaml", name, name + "-pv.yaml")

    # 检查目录是否存在，如果不存在则创建
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))

    # 将YAML字符串写入文件
    with open(file_path, 'w') as file:
        file.write(yaml_string)

    print("模板yaml已生成:", file_path)


if __name__ == "__main__":
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)['variables']
    generate_pv(config)
