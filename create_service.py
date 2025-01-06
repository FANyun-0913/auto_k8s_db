# -*- coding: utf-8 -*-

import yaml
import os

def generate_service(config):
    # 定义变量
    name = config['name']
    namespace = config['namespace']
    node_port = config['node_port']

    # 定义YAML数据结构
    yaml_data = {
        "apiVersion": "v1",
        "kind": "Service",
        "metadata": {
            "name": name + "-svc",
            "namespace": namespace,
            "labels": {
                "app": "mysql"
            }
        },
        "spec": {
            "ports": [
                {
                    "port": 3306,
                    "name": "mysql",
                    "targetPort": 3306,
                    "nodePort": node_port
                }
            ],
            "selector": {
                "app": "mysql"
            },
            "type": "NodePort",
            "sessionAffinity": "ClientIP"
        }
    }

    # 将数据结构转换为YAML字符串
    yaml_string = yaml.dump(yaml_data)

    # 指定完整的文件路径
    file_path = os.path.join("/kube/config/yaml", name, name + "-svc" + ".yaml")

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
    generate_service(config)
