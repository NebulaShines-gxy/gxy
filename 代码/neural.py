import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.utils.data import DataLoader, TensorDataset
import numpy as np
from torch.autograd import Variable
import matplotlib.pyplot as plt
from get_data import data_get
from pca import pca_2, draw_pic


'''定义神经网络模型'''
class SimpleNN(nn.Module):
    def __init__(self):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(5, 128)
        self.relu1 = nn.ReLU()
        self.dropout1 = nn.Dropout(0.5)
        self.fc2 = nn.Linear(128, 64)
        self.relu2 = nn.ReLU()
        self.dropout2 = nn.Dropout(0.5)
        self.fc3 = nn.Linear(64, 1)
        self.sigmoid = nn.Sigmoid()

    def forward(self, x):
        x = self.fc1(x)
        x = self.relu1(x)
        x = self.dropout1(x)
        x = self.fc2(x)
        x = self.relu2(x)
        x = self.dropout2(x)
        x = self.fc3(x)
        x = self.sigmoid(x)
        return x

if __name__ == '__main__':
    '''数据预处理'''
    X_train, y_train, X_val, y_val, X_test, y_test = data_get(r'std_result.csv', 1)
    # X_train, picked_eig_vector1 = pca_2(X_train, 2)
    # X_val, picked_eig_vector2 = pca_2(X_val, 2)
    # X_test, picked_eig_vector3 = pca_2(X_test, 2)

    # y_train = y_train.values
    # y_val = y_val.values
    # y_test = y_test.values

    # draw_pic(X_train, y_train)
    # draw_pic(X_val, y_val)
    # draw_pic(X_test, y_test)
    # 转换为PyTorch的Tensor
    X_train = torch.FloatTensor(X_train)
    y_train = torch.FloatTensor(y_train)
    X_val = torch.FloatTensor(X_val)
    y_val = torch.FloatTensor(y_val)
    X_test = torch.FloatTensor(X_test)
    y_test = torch.FloatTensor(y_test)
    print(y_val)
    # 创建数据加载器
    train_dataset = TensorDataset(X_train, y_train)
    train_dataloader = DataLoader(train_dataset, batch_size=3200, shuffle=True)
    val_dataset = TensorDataset(X_val, y_val)
    val_dataloader = DataLoader(val_dataset, batch_size=3200, shuffle=True)
    test_dataset = TensorDataset(X_test, y_test)
    test_dataloader = DataLoader(test_dataset, batch_size=1, shuffle=True)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print("Using device:", device)
    model = SimpleNN()
    model.to(device)
    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)
    # 训练模型
    val_accuracy_list = []
    num_epochs = 50
    for epoch in range(num_epochs):
        model.train()
        for inputs, labels in train_dataloader:
            inputs, labels = inputs.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels.view(-1, 1))
            loss.backward()
            optimizer.step()
            # 在验证集上评估
        val_accuracy = 0
        for val_inputs, val_labels in val_dataloader:
            val_inputs, val_labels = val_inputs.to(device), val_labels.to(device)
            val_outputs = model(val_inputs)
            val_predicted_labels = (val_outputs >= 0.5).float().view(-1)
            val_accuracy += torch.sum(val_predicted_labels == val_labels) / len(val_labels)
        val_accuracy_list.append(val_accuracy)
        val_accuracy /= len(val_dataloader)
        print('valdition________________________________________________________________')
        print('epoch:', epoch+1, 'accuracy:', val_accuracy*100, '%')

    x_values = range(len(val_accuracy_list))
    epoch_list = [tensor.item() for tensor in val_accuracy_list]
    plt.plot(x_values, epoch_list, marker='o', linestyle='-', color ='red')
    plt.title('accuracy_epoch')
    plt.xlabel('epoch_number')
    plt.ylabel('epoch_acc')
    plt.show()

    with torch.no_grad():
        model.eval()
        test_accuracy = 0.0
        for test_inputs, test_labels in test_dataloader:
            test_inputs, test_labels = test_inputs.to(device), test_labels.to(device)
            test_outputs = model(test_inputs)
            test_predicted_labels = (test_outputs >= 0.5).float().view(-1)
            test_accuracy += torch.sum(test_predicted_labels == test_labels) / len(test_labels)
        test_accuracy /= len(test_dataloader)
        print(f'Test Accuracy: {test_accuracy.item()*100}%')

    torch.save(model, 'entire_model.pth')


