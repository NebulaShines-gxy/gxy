# 读取文件名
input_file = r'F:\My_Work\大创\trans.txt'
output_file = 'F:\My_Work\大创\output_trans.txt'

# 打开输入文件和输出文件
with open(input_file, 'r', encoding='utf-8') as input_file, open(output_file, 'w', encoding='utf-8') as output_file:
    # 遍历每一行
    for line in input_file:
        # 分割每行，以空格为分隔符
        parts = line.split(' ', 1)
        
        # 如果成功分割，并且有两个部分，就取第二部分写入输出文件
        if len(parts) == 2:
            output_file.write(parts[1])
        else:
            # 如果没有编号，就直接写入整行
            output_file.write(line)

