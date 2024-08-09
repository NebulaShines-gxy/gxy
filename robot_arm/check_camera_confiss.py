import cv2
import numpy as np

# 相机内参矩阵（替换为你的实际参数）
camera_matrix = np.array([[131.2663, 0,  60.6533],
                          [0, 131.2183, 57.9450],
                          [0,  0,  1]], dtype=np.float32)

# 畸变系数（替换为你的实际参数）
dist_coeffs = np.array([-0.4233, 0.2229,  -0.00048375, -0.00044478, -0.0640,], dtype=np.float32)
#dist_coeffs = np.array([-0.4531, 0.3776, -0.3124, 0.0022, -0.00037268, ], dtype=np.float32)

#dist_coeffs = np.array([-0.4321, 0.2589,  0.0010, -0.00029798, -0.1262,], dtype=np.float32)
#dist_coeffs = np.array([k1, k2, p1, p2, k3])
image = cv2.imread('F:\\My_Work\\camera_calibration\\25.jpg')
# 矫正图像
undistorted_image = cv2.undistort(image, cameraMatrix=camera_matrix, distCoeffs=dist_coeffs)

# 保存或显示矫正后的图像
cv2.imwrite('undistorted_image.jpg', undistorted_image)
cv2.imshow('Undistorted Image', undistorted_image)
cv2.waitKey(0)
cv2.destroyAllWindows()