import os

folder_path = "I:\\test"

# 获取所有文件名
files = os.listdir(folder_path)

# 分别存储 WAV、TXT 和 CSV 文件名
wav_files = [file for file in files if file.endswith(".wav")]
txt_files = [file for file in files if file.endswith(".txt")]
csv_files = [file for file in files if file.endswith(".csv")]

# 检查每个 WAV 文件是否存在对应的 TXT 和 CSV 文件
for wav_file in wav_files:
    base_name, _ = os.path.splitext(wav_file)
    txt_file = base_name + ".txt"
    csv_file = base_name + ".csv"
    if txt_file not in txt_files or csv_file not in csv_files:
        print(f"Missing files for WAV file: {wav_file}")

# 检查每个 TXT 文件是否存在对应的 WAV 和 CSV 文件
for txt_file in txt_files:
    base_name, _ = os.path.splitext(txt_file)
    wav_file = base_name + ".wav"
    csv_file = base_name + ".csv"
    if wav_file not in wav_files or csv_file not in csv_files:
        print(f"Missing files for TXT file: {txt_file}")

# 检查每个 CSV 文件是否存在对应的 WAV 和 TXT 文件
for csv_file in csv_files:
    base_name, _ = os.path.splitext(csv_file)
    wav_file = base_name + ".wav"
    txt_file = base_name + ".txt"
    if wav_file not in wav_files or txt_file not in txt_files:
        print(f"Missing files for CSV file: {csv_file}")

   

           