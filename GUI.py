from tkinter import *
from PIL import Image, ImageTk
from KNN import compute_
from get_data import data_get
import numpy as np
from logistic import sigmoid
import torch
from neural import SimpleNN

def get_value():
    value1 = float(entry1.get())
    value2 = float(entry2.get())
    value3 = float(entry3.get())
    value4 = float(entry4.get())
    value5 = float(entry5.get())
    value1 = (value1 - 0)/6
    value2 = (value2 - 0)/4.4
    value3 = (value3 - 0)/3.9
    value4 = (value4 - 0)/4.5
    value5 = (value5 - 45)/28
    matrix = np.array([[value1, value2, value3, value4, value5]])
    return matrix

def open_new_window(predictions):
    new_window = Toplevel(root)
    new_window.geometry("120x80")
    if predictions == 1:
        label = Label(new_window, text="齿轮箱工作正常", justify="center")
    else:
        label = Label(new_window, text="齿轮箱发生异常", justify="center")
    label.place(relx=0.12, rely=0.3, anchor=NW)

def logistic():
    theta = np.load("F:\My_Work\大数据课程\大作业\logistic_theta.npy")
    x = get_value()
    h_val = sigmoid(x @ theta)
    predictions = (h_val >= 0.5).astype(int)
    open_new_window(predictions)
    return 0

def neural():
    x = get_value()
    x = torch.FloatTensor(x)
    model = SimpleNN()
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    x = x.to(device)
    #model = torch.load('F:\My_Work\大数据课程\大作业\entire_weights.pth')
    model.load_state_dict(torch.load('model_weights.pth', map_location=device))
    model.to(device)
    model.eval()
    y = model(x)
    y = (y >= 0.5).float().view(-1)
    print(y)
    open_new_window(int(y))
    return 0

def knn():
    X_train, y_train, X_val, y_val, X_test, y_test = data_get(r'F:\My_Work\大数据课程\大作业\10.0_subset.csv', 1)
    x = get_value()
    x_pred = int(compute_(X_train, y_train, x))
    open_new_window(x_pred)
    return 0

root = Tk()
root.title("齿轮箱预测")
root.geometry("640x480")

'''添加背景图片'''
image_path = "F:\\My_Work\\大数据课程\\大作业\\R.jpg"
image = Image.open(image_path)
tk_image = ImageTk.PhotoImage(image)
# 创建Label用于背景图片
background_label = Label(root, image=tk_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

image_path_2 = "F:\\My_Work\\大数据课程\\大作业\\OIP.jpg"
image_2 = Image.open(image_path_2)
image_2 = image_2.resize((164, 64))
tk_image_2 = ImageTk.PhotoImage(image_2)
# 创建Label用于背景图片
background_label_2 = Label(root, image=tk_image_2)
background_label_2.place(x=0, y=0, relwidth=0.26, relheight=0.13)



'''设置传感器参数标签及输入框'''
a1 = Label(root, text="a1:")
a2 = Label(root, text="a2:")
a3 = Label(root, text="a3:")
a4 = Label(root, text="a4:")
a1.place(relx=0.1, rely=0.3,  anchor=NW)
a2.place(relx=0.1, rely=0.4,  anchor=NW)
a3.place(relx=0.5, rely=0.3,  anchor=NW)
a4.place(relx=0.5, rely=0.4, anchor=NW)

entry1 = Entry(root, width=30)
entry2 = Entry(root, width=30)
entry3 = Entry(root, width=30)
entry4 = Entry(root, width=30)
entry1.place(relx=0.15, rely=0.3,  anchor=NW)
entry2.place(relx=0.15, rely=0.4,  anchor=NW)
entry3.place(relx=0.55, rely=0.3,  anchor=NW)
entry4.place(relx=0.55, rely=0.4,  anchor=NW)
entry1.insert(0, '输入-5.8——5.5之间的数')
entry2.insert(0, '输入-3.2——3.0之间的数')
entry3.insert(0, '输入-2.9——2.6之间的数')
entry4.insert(0, '输入-3.1——3.7之间的数')


'''设置载荷'''
load = Label(root, text="load:")
load.place(relx=0.15, rely=0.5,  anchor=NW)
entry5 = Entry(root, width=50)
entry5.place(relx=0.25, rely=0.5,  anchor=NW)
entry5.insert(0, '请输入0到90之间的一个间距为10的整数')

'''添加按钮'''
logistic_btn = Button(root, text="逻辑回归", command=logistic)
neural_btn = Button(root, text="神经网络", command=neural)
knn_btn = Button(root, text="k近邻算法", command=knn)

logistic_btn.place(relx=0.2, rely=0.6,  anchor=NW)
neural_btn.place(relx=0.4, rely=0.6,  anchor=NW)
knn_btn.place(relx=0.6, rely=0.6,  anchor=NW)

root.mainloop()

