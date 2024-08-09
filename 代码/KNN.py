import numpy as np
from get_data import data_get
from result_get import calculate_
from pca import pca_2
class KNNClassifier:
    def __init__(self, k=3):
        self.k = k
        self.x_train = None
        self.y_train = None

    def fit(self, x_train, y_train):
        self.x_train = x_train
        self.y_train = y_train
        return self

    def predict(self, x_predict):
        y_predict = [self._predict(x) for x in x_predict]
        return np.array(y_predict)

    def _predict(self, x):
        distances = [np.sqrt(np.sum((x_train - x) ** 2)) for x_train in self.x_train]
        nearest = np.argsort(distances)[:self.k]
        top_k_y = [self.y_train[index] for index in nearest]
        d = {}
        for cls in top_k_y:
            d[cls] = d.get(cls, 0) + 1
        d_list = list(d.items())
        d_list.sort(key=lambda x: x[1], reverse=True)
        return np.array(d_list[0][0])

    def __repr__(self):
        return "KNN(k={})".format(self.k)


def compute(x_train, y_train, x_test, y_test):
    random_indices_train = np.random.choice(X_train.shape[0], size=3000, replace=False)
    x_train = x_train[random_indices_train]
    y_train = y_train[random_indices_train]
    random_indices_test = np.random.choice(X_test.shape[0], size=100, replace=False)
    x_test = x_test[random_indices_test]
    y_test = y_test[random_indices_test]

    knn = KNNClassifier(3)
    print(knn.__repr__())
    knn.fit(x_train, y_train)
    x_pred = knn.predict(x_test)
    y_test = np.array(y_test, dtype=int)
    x_pred = np.array(x_pred, dtype=int)
    calculate_(x_pred, y_test)

def compute_(x_train, y_train, x_test):
    random_indices_train = np.random.choice(x_train.shape[0], size=30000, replace=False)
    x_train = x_train[random_indices_train]
    y_train = y_train[random_indices_train]
    knn = KNNClassifier(3)
    print(knn.__repr__())
    knn.fit(x_train, y_train)
    x_pred = knn.predict(x_test)
    return x_pred


if __name__ == '__main__':
    X_train, y_train, X_val, y_val, X_test, y_test = data_get(r'std_result.csv', 1)
    X_val, picked_eig_vector2 = pca_2(X_val, 3)
    X_train, picked_eig_vector1 = pca_2(X_train, 3)
    X_test, picked_eig_vector3 = pca_2(X_test, 3)
    compute(X_train, y_train, X_test, y_test)

