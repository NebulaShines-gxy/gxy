'''二分类的统计'''

def calculate_(pred, true):
    total = len(pred)
    total_true = 0
    total_false = 0
    acc_1 = 0
    acc_0 = 0
    for i in range(total):
        if true[i] == 1:
            total_true += 1
            if pred[i] == 1:
                acc_1 += 1
        else:
            total_false += 1
            if pred[i] == 0:
                acc_0 += 1
    acc = float((acc_1 + acc_0)/total)
    acc_1 = float(acc_1/total_true)
    acc_0 = float(acc_0/total_false)
    print('总的正确率：', acc*100, '%')
    print('1的正确率：', acc_1*100, '%')
    print('0的正确率：', acc_0*100, '%')


if __name__ == '__main__':
    '''这是一个验证实例'''
    import numpy as np
    a = [1, 0, 1, 0, 1, 1]
    b = [1, 1, 0, 0, 1, 1]
    a = np.array(a)
    b = np.array(b)
    calculate_(a, b)