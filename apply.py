import os
import subprocess
import yaml

def apply_yaml_files(directory, name):
    # 定义需要按顺序应用的文件名列表
    file_order = [
        f"{name}-pv.yaml",
        f"{name}-pvc.yaml",
        "mysql-password-secret.yaml",
        f"{name}-svc.yaml",
        f"{name}-statefulset.yaml"
    ]

    # 获取目录中的所有YAML文件
    yaml_files = [f for f in os.listdir(directory) if f.endswith('.yaml')]

    # 创建一个字典来存储文件名和文件路径的映射
    file_map = {file: os.path.join(directory, file) for file in yaml_files}

    # 按指定的顺序应用文件
    for file_name in file_order:
        if file_name in file_map:
            file_path = file_map[file_name]
            print(f"Applying {file_path}")
            try:
                # 使用kubectl apply命令应用YAML文件
                result = subprocess.run(['kubectl', 'apply', '-f', file_path], check=True, stdout=subprocess.PIPE,
                                        stderr=subprocess.PIPE)
                print(result.stdout.decode())
            except subprocess.CalledProcessError as e:
                print(f"Error applying {file_path}:")
                print(e.stderr.decode())
        else:
            print(f"File {file_name} not found in directory {directory}")


if __name__ == "__main__":
    # 指定YAML文件所在的目录
    # 从配置文件中读取name变量
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)['variables']
    name = config['name']
    directory = f"/kube/config/yaml/{name}"
    apply_yaml_files(directory, name)
