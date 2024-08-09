import matplotlib.pyplot as plt
import numpy as np
from get_data import data_get

def pca_2(data, dim):
    data = np.array(data)
    N,D = np.shape(data)
    data = data - np.mean(data, axis=0, keepdims=True)
    C = np.dot(data.T, data)/N-1
    eig_values, eig_vector = np.linalg.eig(C)
    indexs_ = np.argsort(-abs(-eig_values))[:dim]
    print("Index:\n",indexs_)
    print('eig_values:\n', eig_values)
    print('eig_vector:\n', eig_vector)
    pick_eig_vector = eig_vector[:, indexs_]
    data_ndim = np.dot(data, pick_eig_vector)
    return data_ndim, pick_eig_vector

def draw_pic(datas, labs):
    plt.cla()
    unique_labs = np.unique(labs)
    colors = ['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'pink', 'cyan', 'brown', 'gray']
    p = []
    legends = []
    for i in range(len(unique_labs)):
        index = np.where(labs ==unique_labs[i])
        index = np.random.choice(index[0], size=200, replace=True, p=None)
        pi = plt.scatter(datas[index, 0], datas[index, 1], c=colors[i])
        p.append(pi)
        legends.append(unique_labs[i])
    plt.title('load = all')
    plt.legend(p, legends)
    plt.show()

if __name__ == '__main__':
    import csv
# 打开CSV文件

    X_train, y_train, X_val, y_val, X_test, y_test = data_get(r'std_result.csv', 1)
    labs = np.array(y_train)
    data_2d, picked_eig_vector = pca_2(X_train, 4)
    print(data_2d.shape)
    print(type(data_2d))
    print(labs.shape)
    print(type(labs))
    draw_pic(data_2d, labs)