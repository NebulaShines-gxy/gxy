import math  
  
# 假设你有一个se对象，它有一个set_angles方法（这通常是一个自定义的类或库）  
# 你也需要导入Serial和time库（如果你正在使用它们）  
# from serial import Serial  # 如果你正在使用串口通信  
# import time as time  # 如果你正在使用delay函数  
  
def arm_pose(x, y, z, Roll, step):  
    idlist = [1, 2, 3, 4]  # 关节ID列表  
    angle0 = [135, 135, 135.6, 135.1]  # 初始角度列表  
    s_degree = [0, 0, 0, 0]  # 计算后的角度列表  
  
    # 机械臂连杆长度  
    l1 = 85  
    l2 = 136  
    l3 = 75  
    l4 = 103  
  
    # 计算第一个关节角度  
    theta1 = -math.atan2(x, y)  
  
    # 计算变量a和b  
    a = x * math.sin(theta1) - y * math.cos(theta1)  
    b = z - l1  
  
    # 计算A, B, C  
    A = math.pow(a, 2) + math.pow(b, 2) + math.pow(l3 + l4, 2) - math.pow(l2, 2) + 2 * b * (l3 + l4)  
    B = -4 * a * (l3 + l4)  
    C = math.pow(a, 2) + math.pow(b, 2) + math.pow(l3 + l4, 2) - math.pow(l2, 2) - 2 * b * (l3 + l4)  
  
    # 计算theta23  
    if A == 0:  
        theta23 = 2 * math.atan2(-C, B)  
    else:  
        discriminant = math.pow(B, 2) - 4 * A * C  
        if discriminant < 0:  
            print(-1)  # 打印错误信息到控制台，而不是通过串口  
            return  45, 135, 225
        else:  
            theta23 = 2 * math.atan2(-B - math.sqrt(discriminant), 2 * A)  
  
    # 计算theta2和theta3  
    theta2 = math.atan2(a - (l3 + l4) * math.sin(theta23), b - (l3 + l4) * math.cos(theta23))  
    theta3 = theta23 - theta2  
  
    # 打印关节角度  
    #print(f"{theta1 * 180 / math.pi:.2f}, {theta2 * 180 / math.pi:.2f}, {theta3 * 180 / math.pi:.2f}, {Roll}")  
  
    # 转换为度并设置角度  
    s_degree[0] = angle0[0] + theta1 * 180 / math.pi  
    s_degree[1] = angle0[1] - theta2 * 180 / math.pi  
    s_degree[2] = angle0[2] - theta3 * 180 / math.pi  # 注意这里你可能需要根据机械臂的实际情况来调整正负号  
    s_degree[3] = angle0[3] + Roll  
  
    # 打印设置的角度  
    #print(f"{s_degree[0]:.2f}, {s_degree[1]:.2f}, {s_degree[2]:.2f}, {s_degree[3]:.2f}")  
    return s_degree[0], s_degree[1], s_degree[2]
    # 假设se对象存在并且有一个set_angles方法  
    # se.set_angles(idlist, s_degree, step, 1)
arm_pose(210, 210, 100, 0, 100)