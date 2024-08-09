import numpy as np
import pandas as pd

def data_get(file_path, if_load = 1):
    data = pd.read_csv(file_path)
    if if_load == 1:
        X = data[['a1', 'a2', 'a3', 'a4', 'load']]
    else:
        X = data[['a1', 'a2', 'a3', 'a4']]
    # print(X)
    y = data['failure']
    # print(y)
    X = np.c_[np.ones(X.shape[0]), X]
    '''数据集的划分'''
    # 设置训练集和测试集的比例
    train_ratio = 0.7
    test_ratio = 0.1
    val_ratio = 0.2
    num_samples = len(y)
    num_train_samples = int(train_ratio * num_samples)
    num_test_samples = int(test_ratio * num_samples)
    num_val_samples = int(val_ratio * num_samples)
    shuffled_indices = np.random.permutation(num_samples)
    # 划分训练集
    train_indices = shuffled_indices[:num_train_samples]
    X_train = X[train_indices, :]
    y_train = y[train_indices]
    # 划分验证集
    val_indices = shuffled_indices[num_train_samples:num_train_samples + num_val_samples]
    X_val = X[val_indices, :]
    y_val = y[val_indices ]
    # 划分测试集
    test_indices = shuffled_indices[num_train_samples + num_val_samples:]
    X_test = X[test_indices, :]
    y_test = y[test_indices]

    y_train = np.array(y_train)
    y_val = np.array(y_val)
    y_test = np.array(y_test)

    return  X_train[:, 1:], y_train, X_val[:, 1:], y_val, X_test[:, 1:], y_test

if __name__ == '__main__':
    X_train, y_train, X_val, y_val, X_test, y_test = data_get(r'std_result.csv', 1)
    print(X_train.shape)
    print(y_train)