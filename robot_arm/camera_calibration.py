###相机标定与校正结果展示###

import os
import numpy as np
import cv2
import glob
import time

def find_chessboard_corners_custom(gray_img, pattern_size, criteria=None):
    corners = []
    w, h = pattern_size
    k = 0.4
    window_size = 5

    # Compute gradients
    dx = cv2.Sobel(gray_img, cv2.CV_64F, 1, 0, ksize=3)
    dy = cv2.Sobel(gray_img, cv2.CV_64F, 0, 1, ksize=3)

    # Compute M matrix for each pixel
    M = np.zeros_like(gray_img, dtype=np.float32)
    for y in range(gray_img.shape[0]):
        for x in range(gray_img.shape[1]):
            M[y, x] = dx[y, x]**2 * dy[y, x]**2 - k * (dx[y, x]**2 + dy[y, x]**2)**2

    # Find local maxima as corners
    for y in range(window_size, gray_img.shape[0] - window_size):
        for x in range(window_size, gray_img.shape[1] - window_size):
            if M[y, x] > np.max(M[y - window_size:y + window_size, x - window_size:x + window_size]) and M[y, x] > 0:
                corners.append((x, y))

    return True, np.array(corners, dtype=np.float32)


#相机参数标定得到相机的内参矩阵，畸变矩阵
def calib(inter_corner_shape, size_per_grid, img_dir,img_type):
    # 标准：仅用于subpix校准，此处不使用。
    # criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    w,h = inter_corner_shape
    # cpp_int：int形式的角点，以“ int”形式保存世界空间中角点的坐标
    # like (0,0,0), (1,0,0), (2,0,0) ....,(10,7,0).
    cp_int = np.zeros((w*h, 3), np.float32)
    cp_int[:, :2] = np.mgrid[0:w, 0:h].T.reshape(-1, 2)
    # cp_world：世界空间中的角点，保存世界空间中角点的坐标。
    cp_world = cp_int*size_per_grid
    
    obj_points = [] # 世界空间中的点
    img_points = [] # 图像空间中的点（与obj_points相关）
    images = glob.glob(img_dir + os.sep + '**.' + img_type)
    for frame in images:
        img_name = frame.split(os.sep)[-1]
        img = cv2.imread(frame)

        height, width, channels = img.shape
        # 打印图片大小
        #print(f"Image size: {width}x{height}")
        gray_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        # 找到角点cp_img：像素空间中的角点。
        #ret, cp_img = cv2.findChessboardCorners(gray_img, (w, h), None)
        ret, cp_img = cv2.findChessboardCorners(gray_img, (w, h), None)
        # if ret is True, save.
        if ret == True:
            # cv2.cornerSubPix(gray_img,cp_img,(11,11),(-1,-1),criteria)
            obj_points.append(cp_world)
            img_points.append(cp_img)
            #print('cp_img:', cp_img)
            # 显示角点-
            cv2.drawChessboardCorners(img, (w,h), cp_img, ret)
            #cv2.namedWindow('FoundCorners', cv2.WINDOW_NORMAL)
            #cv2.imshow('FoundCorners', img)
            cv2.imwrite(save_dir1 + os.sep + img_name, img)
            cv2.waitKey(1)
            
    cv2.destroyAllWindows()
    # 校准相机
    ret, mat_inter, coff_dis, v_rot, v_trans = cv2.calibrateCamera(obj_points, img_points, gray_img.shape[::-1], None, None)
    #标定的误差
    print (("ret:"),ret)
    print (("internal matrix:\n"),mat_inter)
    # in the form of (k_1,k_2,p_1,p_2,k_3))
    print (("distortion cofficients:\n"),coff_dis)
    # 看旋转向量和平移向量的格式
    '''
    v_rot_shape = np.array(v_rot).shape
    v_trans_shape = np.array(v_trans).shape
    print("Rotation vector shape:", v_rot_shape)
    print("Translation vector shape:", v_trans_shape)
    '''
    print (("rotation vectors:\n"),v_rot[0])
    print (("translation vectors:\n"),v_trans[0])
    # 计算重新投影的误差
    total_error = 0
    for i in range(len(obj_points)):
        img_points_repro, _ = cv2.projectPoints(obj_points[i], v_rot[i], v_trans[i], mat_inter, coff_dis)
        error = cv2.norm(img_points[i], img_points_repro, cv2.NORM_L2)/len(img_points_repro)
        total_error += error
    print(("Average Error of Reproject: "), total_error/len(obj_points))
    
    return mat_inter, coff_dis

#根据得到的内参矩阵，畸变矩阵来进行图像纠偏	
#若矫正后的图像只有原图像的一部分
##注意使用的图像要把棋盘格拍全了，这样矫正后的图像就不会只有一部分了
def dedistortion(inter_corner_shape, img_dir,img_type, save_dir, mat_inter, coff_dis):
##   w,h = inter_corner_shape
      
##   img2 = cv2.imread(img_dir_sin)
    #(w, h) = (640, 480)
##   newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mat_inter,coff_dis,(w,h),0,(w,h))
##   dst = cv2.undistort(img2, mat_inter, coff_dis, None, newcameramtx)
##   cv2.imshow('dst',dst)
    
    images = glob.glob(img_dir + os.sep + '**.' + img_type)
    for fname in images:

        img_name = fname.split(os.sep)[-1]
        img = cv2.imread(fname)
        w, h = img.shape[:2][::-1]
        newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mat_inter, coff_dis, (w,h) , 0, (w,h)) # 自由比例参数
        dst = cv2.undistort(img, mat_inter, coff_dis, None, newcameramtx)
        #clip the image
        #x,y,w,h = roi
        #dst = dst[y:y+h, x:x+w]
        #cv2.imshow('dst',dst)
        #cv2.waitKey()
        cv2.imwrite(save_dir + os.sep + img_name, dst)

    print('Dedistorted images have been saved to: %s successfully.' %save_dir)
    
if __name__ == '__main__':
	# 棋盘格格点
    inter_corner_shape = (8, 5)
	# 格点尺寸
    size_per_grid = 0.029
	# 标定照片文件夹
    img_dir = "F:\My_Work\camera_calibration\openmv_pictures"
    img_type = "jpg"
	# 保存识别角点文件夹
    save_dir1 = "F:\My_Work\camera_calibration\openmv_concers"
    # 相机标定
    mat_inter, coff_dis = calib(inter_corner_shape, size_per_grid, img_dir, img_type)
    # 保存矫正后图像文件夹 
    save_dir = "F:\My_Work\camera_calibration\openmv_save"
    # img_dir_sin='.\\pic\\IR_camera_calib_img\\image20200702084131.jpg'
    
    if(not os.path.exists(save_dir)):
        os.makedirs(save_dir)
    if(not os.path.exists(save_dir1)):
        os.makedirs(save_dir1)
    dedistortion(inter_corner_shape, img_dir, img_type, save_dir, mat_inter, coff_dis)
    
    
    
