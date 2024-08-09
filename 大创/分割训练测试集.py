import os
import random
import shutil

# 文件夹路径
wav_txt_folder = "I:\\corpus_"
csv_folder = "I:\\corpus_"
test_folder = "I:\\test_1"
train_folder = "I:\\train_1"

# 获取所有 WAV 文件名
wav_files = [file for file in os.listdir(wav_txt_folder) if file.endswith(".wav")]

# 确保 WAV 文件名对应的 TXT 和 CSV 文件名相同

wav_files = [file for file in os.listdir(wav_txt_folder) if file.endswith(".wav")]
txt_files = [file for file in os.listdir(wav_txt_folder) if file.endswith(".txt")]
csv_files = [file for file in os.listdir(csv_folder) if file.endswith(".csv")]
# 选择20%作为测试集

num_test_files = int(len(wav_files) * 0.2)
test_indices = random.sample(range(len(wav_files)), num_test_files)
test_wav_files = [wav_files[i] for i in test_indices]
test_txt_files = [txt_files[i] for i in test_indices]
test_csv_files = [csv_files[i] for i in test_indices]

# 复制测试集文件到新文件夹
for wav_file, txt_file, csv_file in zip(test_wav_files, test_txt_files, test_csv_files):
    # 复制 WAV 文件
    shutil.copy(os.path.join(wav_txt_folder, wav_file), os.path.join(test_folder, wav_file))
    # 复制 TXT 文件
    shutil.copy(os.path.join(wav_txt_folder, txt_file), os.path.join(test_folder, txt_file))
    # 复制 CSV 文件
    shutil.copy(os.path.join(csv_folder, csv_file), os.path.join(test_folder, csv_file))

# 剩下的文件作为训练集
for wav_file, txt_file, csv_file in zip(wav_files, txt_files, csv_files):
    if (wav_file, txt_file, csv_file) not in zip(test_wav_files, test_txt_files, test_csv_files):
        # 复制 WAV 文件
        shutil.copy(os.path.join(wav_txt_folder, wav_file), os.path.join(train_folder, wav_file))
        # 复制 TXT 文件
        shutil.copy(os.path.join(wav_txt_folder, txt_file), os.path.join(train_folder, txt_file))
        # 复制 CSV 文件
        shutil.copy(os.path.join(csv_folder, csv_file), os.path.join(train_folder, csv_file))

