import numpy as np
from get_data import data_get
from result_get import calculate_
from pca import pca_2

def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def cost_function(X, y, theta):
    m = len(y)
    h = sigmoid(X @ theta)
    cost = (-1/m) * np.sum(y * np.log(h) + (1 - y) * np.log(1 - h))
    return cost

def gradient_descent(X, y, theta, learning_rate, iterations):
    m = len(y)
    cost_history = np.zeros(iterations)
    for i in range(iterations):
        h = sigmoid(X @ theta)
        gradient = X.T @ (h - y) / m
        theta -= learning_rate * gradient
        cost_history[i] = cost_function(X, y, theta)
    return theta, cost_history

if __name__ == '__main__':
    X_train, y_train, X_val, y_val, X_test, y_test = data_get(r'F:\My_Work\大数据课程\大作业\std_result.csv', 1)
# X_train, picked_eig_vector1 = pca_2(X_train, 2)
# X_val, picked_eig_vector2 = pca_2(X_val, 2)
# X_test, picked_eig_vector3 = pca_2(X_test, 2)
    X_val, picked_eig_vector2 = pca_2(X_val, 3)
    X_train, picked_eig_vector1 = pca_2(X_train, 3)
    X_test, picked_eig_vector3 = pca_2(X_test, 3)
    '''进行训练'''
    theta = np.zeros(X_train.shape[1])
    learning_rate = 0.6
    iterations = 300
    accuracy_history = []
    loss = []
    theta, cost_history = gradient_descent(X_train, y_train, theta, learning_rate, iterations)
    h_val = sigmoid(X_test @ theta)
    print(h_val)
    print(theta)
    predictions = (h_val >= 0.5).astype(int)
    y_test = np.array(y_test, dtype=int)
    calculate_(predictions, y_test)
    np.save("logistic_theta.npy", theta)





