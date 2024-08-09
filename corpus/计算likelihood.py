import os
import pandas as pd

folder_path = "I:\corpus_sil_dlc_"
output_file = "I:\likehooid.csv"

# 获取文件夹中所有CSV文件的文件名
file_names = [f for f in os.listdir(folder_path) if f.endswith('.csv')]

with open(output_file, 'w') as f:
    for file_name in file_names:
        # 读取CSV文件
        file_path = os.path.join(folder_path, file_name)
        df = pd.read_csv(file_path)

        # 计算第3的倍数列的平均值
        cols_to_avg = [col for idx, col in enumerate(df.columns) if (idx + 1) % 3 == 0]
        avg_values = df[cols_to_avg].mean().mean()

        # 将结果写入csv文件
        f.write(f'{file_name},{avg_values}\n')


