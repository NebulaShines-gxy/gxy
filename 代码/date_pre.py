import pandas as pd

'''输出显示'''
#显示所有列
pd.set_option('display.max_columns',None)
#显示所有行
pd.set_option('display.max_rows',None)
#设置value的显示长度
pd.set_option('max_colwidth', 1000)
#设置1000列时才换行
pd.set_option('display.width', 100000)

'''文件加载'''
# 用pandas加载CSV文件
file_path_1 = r"b30hz.csv" # 替换成您的CSV文件路径
data_1 = pd.read_csv(file_path_1)
file_path_2 = r"h30hz.csv" # 替换成您的CSV文件路径
data_2 = pd.read_csv(file_path_2)
# 显示数据的前几行
statistics_1= data_1.describe()
print("数据统计信息1：\n", statistics_1)
statistics_2 = data_2.describe()
print("数据统计信息2：\n", statistics_2)

'''缺失值处理'''
# 检查整个数据集是否有缺失值
has_missing_values = data_1.isnull().any().any()
print("\n是否有缺失值：", has_missing_values)
# 检查整个数据集是否有缺失值
has_missing_values = data_2.isnull().any().any()
print("\n是否有缺失值：", has_missing_values)

'''数据进行合并'''
result = pd.concat([data_1, data_2], axis=0, ignore_index=True)
print(result.describe())
result.to_csv('merged_data.csv', index=False)

'''标准化处理'''
columns_to_standardize = ['a1', 'a2', 'a3', 'a4', 'load']
mean_values = result[columns_to_standardize].mean()
std_dev_values = result[columns_to_standardize].std()
result[columns_to_standardize] = (result[columns_to_standardize] - mean_values) / std_dev_values
print(result.describe())
result.to_csv('std_result.csv', index=False)
unique_values = result['load'].unique()
for value in unique_values:
    subset = result[result['load'] == value]
    print(subset.to_csv(f"{value}_subset.csv", index=False))
print("分割完成")
