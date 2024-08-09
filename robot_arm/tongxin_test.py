import serial
import serial.tools.list_ports
import json
import time
import re
import picture2world
import world2arm_
import math

ser = serial.Serial('COM9', 115200)
# 替换为你的Arduino串行端口
ser1 = serial.Serial('COM10', 115200)  # Windows 示例端口，Linux/macOS 请使用 /dev/ttyACMx 或 /dev/ttyUSBx
start = 1

def find_value(buffer, start_index, key):
    # 从指定的起始位置截取 buffer
    buffer = buffer[start_index:]
    # 使用正则表达式查找 "cx": n, 的模式
    matches = list(re.finditer(rf'"{key}"\s*:\s*(\d+)\s*,', buffer))
    #print(matches)
    if matches:
        closest_match = matches[0]
        n = int(closest_match.group(1))
        return n
    else:
        return None

def format_numbers(x_, x1, x2, number):
    numbers = []
    numbers.append(x_)
    numbers.append(x1)
    numbers.append(x2)
    numbers.append(number)
    formatted_numbers = [f"{num:03}" for num in numbers]
    result = ''.join(formatted_numbers)
    result = result + '\n'
    return result
   
def get_number(code, pixels):
    number = 9
    if code == 1 and pixels >=180:
        number = 3
    if code == 1 and pixels < 180:
        number = 1
    if code == 2:
        number = 2
    #print('number:', number)
    return number

count = 0
buffer = ""
def get_data():
    global ser
    count = 0 
    buffer = ""
    cx = 0
    cy = 0
    ser.reset_input_buffer()
    ser.reset_output_buffer()
    while count < 300:
        com_input = ser.read(10)
        #print(com_input)
        if com_input:   # 如果读取结果非空，则输出
     # 将字节数据转换为字符串并追加到缓冲区
            #print(buffer)
            count += 1
            buffer += com_input.decode('utf-8')
    start_index = len(buffer) // 2 
    #print("当前缓冲区内容:", buffer)
    cx = find_value(buffer, start_index, 'cx')
    cy = find_value(buffer, start_index, 'cy')
    pixels = int(find_value(buffer, start_index, 'pixels'))
    code = int(find_value(buffer, start_index, 'code'))
    #print("cx:", cx, "cy:", cy)
    buffer = " "
    return cx, cy, pixels, code
'''
# 获取所有串口设备实例。
# 如果没找到串口设备，则输出：“无串口设备。”
# 如果找到串口设备，则依次输出每个设备对应的串口号和描述信息。
ports_list = list(serial.tools.list_ports.comports())
if len(ports_list) <= 0:
    print("无串口设备。")
else:
    print("可用的串口设备如下：")
    for comport in ports_list:
        print(list(comport)[0], list(comport)[1])
'''
while True:
    print(start)
    while start > 0:
        x, y, pixels, code = get_data()
        print(x, y, pixels, code)
        time.sleep(12)
        x, y, pixels, code = get_data()
        print(x, y, pixels, code)
        x, y = picture2world.image_to_world(x,y)
        x = int(x)
        y = int(y)  
        print(x, y)
        number = get_number(code, pixels)    
        x1, x2, x3 = world2arm_.arm_pose(x, y, 100, 0, 100)
        x1 = int(x1)
        x2 = int(x2)    
        x3 = int(x3)
        number = get_number(code, pixels)
        message = format_numbers( x1, x2, x3, number)
        #message = '120120001\n'
        #time.sleep(3)
        print(message)
        ser1.write(message.encode())
        time.sleep(15)  # 等待一段时间再次发送
        
'''

start = 0
a = 0
while True:
    if start == 0:
        x, y, w, code = get_data()
        x, y = picture2world.image_to_world(x, y)
        
        ref, x1, x2, x3, x4 = world2arm.backward_kinematics(x, y, 20)
        if not ref:
            x1, x2, x3, x4 = 100, 100, 100, 100
        
        number = get_number(code, w)
        message = format_numbers(x1, x2, x3, x4, number)
        ser1.write(message.encode())
        print(f"Sending to Arduino: {message}")
        
        #time.sleep(30)
        
    if start == 1 and ser1.in_waiting > 0:
        #print(1)  # 检查是否有数据可读
        print('you shu ju')
        #a += 1
        print(ser1.in_waiting)
        response = ''
        while ser1.in_waiting > 0:
            response += ser1.read(1).decode('utf-8')
        response = response.strip()
        print(response)
        print('you response')
        #print(response)
        char = "12345"
        index = find_char_in_string(response, char)
        print('index', index)
        if index != -1:
            start = 0  # 重置 start 以便发送下一条消息
        print(start)
    time.sleep(1)
'''
ser.close()
ser1.close()

