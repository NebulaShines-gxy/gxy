import os
import codecs

folder_path = r'I:\train_1'  # 文件夹路径

# 遍历文件夹中的所有txt文件
for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):
        file_path = os.path.join(folder_path, filename)
        # 读取文件内容
        with codecs.open(file_path, 'r', encoding='ansi', errors='ignore') as file:
            content = file.read()
        # 将文件内容写入新文件，以UTF-8编码保存
        with codecs.open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)
