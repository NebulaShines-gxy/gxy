import os

# 指定包含txt文件的文件夹路径
folder_path = r'H:\corpus\files\wf'

# 目标文本行
target_text = '录'

# 遍历文件夹中的每个txt文件
for filename in os.listdir(folder_path):
    if filename.endswith('.txt'):
        file_path = os.path.join(folder_path, filename)
        with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
            # 读取文件的第一行
            first_line = file.readline().strip()
            # 检查第一行是否包含目标文本
            if target_text in first_line:
                print(f'找到符合条件的文件: {filename}')
            #else:
                #print('没找到')
