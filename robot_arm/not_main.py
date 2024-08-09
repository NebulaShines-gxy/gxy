import serial
import serial.tools.list_ports
import picture2world
import world2arm
import detect_color_usb_cam

ser1 = serial.Serial('COM6', 9600)

start = 1
while True:
    if ser1.in_waiting > 0:  # 检查是否有数据可读
        response = ser1.readline().decode().strip()  # 读取一行并解码，strip() 去除行尾的换行符和空格
        print(f"Received from Arduino: {response}")
        start = 1
    result = color_detect()
    while start > 0:
        x, y, w, code = detect_color_usb_cam.color_detect()
        print(x, y, w, code)
        word_point = picture2world.image_to_world(x,y)
        #print(word_point[1])
        #word_point = [[int(element) for element in row] for row in word_point]
        ref, x1, x2, x3, x4 = world2arm.backward_kinematics(word_point[0], abs(word_point[1]), 20)
        print(ref, x1, x2, x3, x4)
        if ref == False:
            x1, x2, x3, x4 = 100, 100, 100, 100
        print("word_point", word_point)
        #time.sleep(1)
        message = format_numbers(x1, x2, x3, x4)
        print(message)
        ser1.write(message.encode())
        start = -1
        print(start)

# 释放摄像头
cap.release()        