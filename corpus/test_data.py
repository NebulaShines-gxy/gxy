import os
import random
import shutil

# 文件夹路径
wav_txt_folder = "I:\\corpus_sil"
csv_folder = "I:\\corpus_sil_dlc_"
test_folder = "I:\\test"
train_folder = "I:\\train"
# 获取文件名列表
wav_txt_files = os.listdir(wav_txt_folder)
csv_files = os.listdir(csv_folder)

# 选择20%作为测试集
num_test_files = int(len(wav_txt_files) * 0.2)
test_files = random.sample(wav_txt_files, num_test_files)

# 移动测试集文件到新文件夹
for file_name in test_files:
    base_name = os.path.splitext(file_name)[0]
    # 移动wav和txt文件
    shutil.move(os.path.join(wav_txt_folder, file_name), os.path.join(test_folder, file_name))
    # 移动csv文件
    csv_file_name = base_name + ".csv"
    shutil.move(os.path.join(csv_folder, csv_file_name), os.path.join(test_folder, csv_file_name))

# 剩下的文件作为训练集
for file_name in wav_txt_files:
    if file_name not in test_files:
        base_name = os.path.splitext(file_name)[0]
        # 移动wav和txt文件
        shutil.move(os.path.join(wav_txt_folder, file_name), os.path.join(train_folder, file_name))
        # 移动csv文件
        csv_file_name = base_name + ".csv"
        shutil.move(os.path.join(csv_folder, csv_file_name), os.path.join(train_folder, csv_file_name))
