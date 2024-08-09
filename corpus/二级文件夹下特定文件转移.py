import os
import shutil

# 源文件夹路径
source_folder = "I:\corpus\pressess"

# 目标文件夹路径
destination_folder = "I:\corpus_dlc"

# 遍历源文件夹中的所有文件夹
for root, dirs, files in os.walk(source_folder):
    # 遍历当前文件夹中的所有文件
    for file in files:
        # 如果文件是CSV文件
        if file.endswith('.csv'):
            # 构造源文件路径
            source_file_path = os.path.join(root, file)
            # 构造目标文件路径
            destination_file_path = os.path.join(destination_folder, file)
            # 复制文件
            shutil.copy(source_file_path, destination_file_path)
