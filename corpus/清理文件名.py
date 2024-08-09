import os

# 指定包含500个文件的文件夹路径
folder_path = r'H:/corpus/files/jcx'

# 获取文件夹中的所有文件
file_list = os.listdir(folder_path)

# 创建一个字典，用于存储每种文件类型的计数
file_count = {}

# 遍历文件夹中的所有文件
for filename in file_list:
    # 获取文件的扩展名
    file_name, file_extension = os.path.splitext(filename)
    
    # 如果文件扩展名不在计数字典中，则初始化计数为1
    if file_extension not in file_count:
        file_count[file_extension] = 1
    
    # 构建新文件名
    new_filename = f"File{file_count[file_extension]}{file_extension}"
    
    # 更新计数
    file_count[file_extension] += 1
    
    # 构建旧文件和新文件的完整路径
    old_file_path = os.path.join(folder_path, filename)
    new_file_path = os.path.join(folder_path, new_filename)
    
    # 重命名文件
    os.rename(old_file_path, new_file_path)
    print(f"重命名文件: {old_file_path} -> {new_file_path}")

