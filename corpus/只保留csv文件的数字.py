import os
import csv

# 输入文件夹路径
folder_path = "I:\corpus_"
# 输出文件夹路径
output_folder = "I:\corpus_"
# 创建输出文件夹
os.makedirs(output_folder, exist_ok=True)

def remove_last_items(filename, separator='_', num_items=4):
    parts = filename.split(separator)
    if len(parts) <= num_items:
        return ""
    base_name = separator.join(parts[:-num_items])
    file_extension = os.path.splitext(filename)[-1]
    return base_name + file_extension


for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        with open(os.path.join(folder_path, filename), mode='r', newline='') as in_file:
            reader = csv.reader(in_file)
            # 跳过前两行
            next(reader)
            next(reader)
            next(reader)
            # 读取剩余行
            rows = list(reader)
            # 去掉前两列
            rows = [row[1:] for row in rows]
            # 写入到新文件中
            filename = remove_last_items(filename)

            output_file_path = os.path.join(output_folder, filename)
            with open(output_file_path, mode='w', newline='') as out_file:
                writer = csv.writer(out_file)
                writer.writerows(rows)

