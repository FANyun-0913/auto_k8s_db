import yaml
import os


def generate_statefulset(config):
    # 定义变量
    name = config['name']
    namespace = config['namespace']
    image = config['image']

    # 定义YAML数据结构
    yaml_data = {
        "apiVersion": "apps/v1",
        "kind": "StatefulSet",
        "metadata": {
            "name": name,
            "namespace": namespace
        },
        "spec": {
            "selector": {
                "matchLabels": {
                    "app": "mysql"
                }
            },
            "serviceName": name + "-svc",
            "replicas": 1,
            "template": {
                "metadata": {
                    "labels": {
                        "app": "mysql"
                    }
                },
                "spec": {
                    "terminationGracePeriodSeconds": 10,
                    "containers": [
                        {
                            "args": [
                                "--character-set-server=utf8mb4",
                                "--collation-server=utf8mb4_unicode_ci",
                                "--lower_case_table_names=1",
                                "--default-time_zone=+8:00"
                            ],
                            "name": "mysql",
                            "image": image,
                            "ports": [
                                {
                                    "containerPort": 3306,
                                    "name": "mysql"
                                }
                            ],
                            "volumeMounts": [
                                {
                                    "name": name+"-data",
                                    "mountPath": "/var/lib/mysql"
                                }
                            ],
                            "env": [
                                {
                                    "name": "MYSQL_ROOT_PASSWORD",
                                    "valueFrom": {
                                        "secretKeyRef": {
                                            "key": "mysql_root_password",
                                            "name": "mysql-password"
                                        }
                                    }
                                }
                            ]
                        }
                    ],
                    "volumes": [
                        {
                            "name": name + "-data",
                            "persistentVolumeClaim": {
                                "claimName": name + "-pvc"
                            }
                        }
                    ]
                }
            }
        }
    }

    # 将数据结构转换为YAML字符串
    yaml_string = yaml.dump(yaml_data)

    # 指定完整的文件路径
    file_path = os.path.join("/kube/config/yaml", name, name + "-statefulset" + ".yaml")

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
    generate_statefulset(config)
