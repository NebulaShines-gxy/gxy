import os

folder_path = 'H:\\corpus\\files\\zjl'  # 文件夹路径

# 获取文件夹名字
folder_name = os.path.basename(folder_path)

# 遍历文件夹中的所有文件
for filename in os.listdir(folder_path):
    # 构建新的文件名
    new_filename = os.path.join(folder_path, folder_name + '_' + filename)
    # 重命名文件
    os.rename(os.path.join(folder_path, filename), new_filename)
