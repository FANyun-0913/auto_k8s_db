import yaml
import os


def generate_secret(config):
    # 定义变量
    name = config['name']
    namespace = config['namespace']
    mysql_root_password = config['mysql_root_password']

    # 定义YAML数据结构
    yaml_data = {
        "apiVersion": "v1",
        "data": {
            "mysql_root_password": mysql_root_password
        },
        "kind": "Secret",
        "metadata": {
            "name": "mysql-password",
            "namespace": namespace
        }
    }

    # 将数据结构转换为YAML字符串
    yaml_string = yaml.dump(yaml_data)

    # 指定完整的文件路径
    file_path = os.path.join("/kube/config/yaml", name, "mysql-password-secret.yaml")

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
    generate_secret(config)
