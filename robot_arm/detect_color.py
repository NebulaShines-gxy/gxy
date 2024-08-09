import sensor, image, time
from pyb import UART
import network
import socket
import json


# 颜色追踪的例子，一定要控制环境的光，保持光线是稳定的。
#green_threshold   = (21, 56, -46, -18, -16, 33)
green_threshold   = (0, 100, -128, -18, -128, 127)
#red_threshold     = (28, 80, -53, 97, 36, 110)
red_threshold     = (0, 100, 22, 127, -128, 127)
sensor.reset() # 初始化摄像头
sensor.set_pixformat(sensor.RGB565) # 格式为 RGB565.
sensor.set_framesize(sensor.QQVGA) # 使用 QQVGA 速度快一些
sensor.skip_frames(time = 2000) # 跳过2000s，使新设置生效,并自动调节白平衡
sensor.set_auto_gain(False) # 关闭自动自动增益。默认开启的，在颜色识别中，一定要关闭白平衡。
sensor.set_auto_whitebal(False)#关闭白平衡。白平衡是默认开启的，在颜色识别中，一定要关闭白平衡。
sensor.set_framerate(20)
clock = time.clock() # 追踪帧率
K = 6000
uart = UART(3,115200)
while(True):
    clock.tick() # Track elapsed milliseconds between snapshots().
    img = sensor.snapshot(1.8) # 从感光芯片获得一张图像

    blobs = img.find_blobs([green_threshold,red_threshold],pixels_threshold = 24,area_threshold = 5,merge = True)
    #blobr = img.find_blobs([red_threshold],pixels_threshold = 24,area_threshold = 5,merge = True)
    #bloba = blobr.add(blobg)
    if blobs:
    #如果找到了目标颜色
        output_str = json.dumps(blobs)
        for b in blobs: #循环效果不好，会有很多误识别，采用单个矩形采样方便返回坐标
        #迭代找到的目标颜色区域
            x = b[0]
            y = b[1]
            width = b[2]
            height = b[3]
                # Draw a rect around the blob.
            img.draw_rectangle([x,y,width,height]) # rect
                #用矩形标记出目标颜色区域
            img.draw_cross(b[5], b[6]) # cx, cy
            print(output_str)
                #在目标颜色区域的中心画十字形标记
            uart.write(output_str)


    #print(clock.fps()) # 注意: 你的OpenMV连到电脑后帧率大概为原来的一半 #如果断开电脑，帧率会增加



