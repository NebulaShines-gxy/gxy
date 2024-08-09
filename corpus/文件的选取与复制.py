import os
import shutil
source_folder = r'H:\corpus\files\gxy_sil_1'  # 源文件夹路径
destination_folder = r'H:\corpus\cesi'  # 目标文件夹路径
# 确保目标文件夹存在，如果不存在则创建
if not os.path.exists(destination_folder):
    os.makedirs(destination_folder)
# 遍历源文件夹中的所有文件
for filename in os.listdir(source_folder):
    file_path = os.path.join(source_folder, filename)
    # 检查文件类型是否为CSV、TXT或WAV
    if filename.endswith('.csv') or filename.endswith('.txt') or filename.endswith('.wav'):
        # 复制文件到目标文件夹
        shutil.copy(file_path, destination_folder)