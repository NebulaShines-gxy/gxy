import os
import shutil

source_folder = 'H:\\corpus\\files\\wf_sil_1'
target_folder = 'G:\\corpus_sil'

# 遍历源文件夹中的所有文件
for file_name in os.listdir(source_folder):
    source_file_path = os.path.join(source_folder, file_name)
    destination_file = os.path.join(target_folder, file_name)
    print(destination_file)
    if not os.path.exists(destination_file):
        print(file_name)
        shutil.copyfile(source_file_path, destination_file)
    

