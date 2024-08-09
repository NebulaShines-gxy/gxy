import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

df = pd.read_csv(r'1.5476245015549588_subset.csv')
df = df.sample(frac=0.005, random_state=42)
# 读取 CSV 文件
# 提取前三个维度作为 x、y、z 轴
x = df['a1']
y = df['a2']
z = df['a3']
# 提取第四个维度作为点的大小
size = df['a4']
# 提取最后一个维度作为颜色
color = df['failure']
# 创建 3D 散点图
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')

scatter = ax.scatter(x, y, z, c=color, s=size, cmap='viridis')

# 添加颜色条
cbar = plt.colorbar(scatter)
cbar.set_label('Dim5')

# 设置轴标签
ax.set_xlabel('Dim1')
ax.set_ylabel('Dim2')
ax.set_zlabel('Dim3')

plt.title('scatter without load, and load =90')
plt.show()
