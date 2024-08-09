import os
from collections import defaultdict

# 指定包含500个txt文件的文件夹路径
folder_path = 'H:/corpus/files/wf_sil'

# 创建一个字典来存储第一行内容和文件名的映射
first_line_to_filenames = defaultdict(list)

# 遍历文件夹中的每个txt文件
for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r', encoding='gbk', errors='ignore') as file:
            first_line = file.readline().strip()  # 读取第一行并去除首尾空白
        # 将第一行内容添加到字典中，并将文件名添加到对应的列表中
        first_line_to_filenames[first_line].append(filename)

# 找到具有相同第一行的文件
duplicate_files = {line: filenames for line, filenames in first_line_to_filenames.items() if len(filenames) > 1}

# 打印具有相同第一行的文件名
for line, filenames in duplicate_files.items():
    print(f'以下文件具有相同的第一行 ({len(filenames)} 个文件):')
    for filename in filenames:
        print(filename)
