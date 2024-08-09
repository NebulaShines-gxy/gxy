import cv2
import numpy as np

# 示例相机内参矩阵
camera_matrix = np.array([[256.6323, 0,  123.5038],
                          [0, 256.5062, 116.4625],
                          [0,  0,  1]], dtype=np.float32)

# 示例相机畸变系数
dist_coeffs = np.array([-0.442, 0.2762, -0.1207, -0.00053171, -0.00066047], dtype=np.float32)

# 图像上的四个点坐标
image_points = np.array([
    [22, 85],
    [20, 10],
    [102, 86],
    [103, 20]
], dtype=np.float32)
image_points = image_points.reshape(-1, 1, 2)

# 对应的世界坐标
world_points = np.array([
    [-13.5, 5, 0],
    [-13.5, 17, 0],
    [13.5, 5, 0],
    [13.5, 17, 0]
], dtype=np.float32)

# 校正图像点
image_points_undistorted = cv2.undistortPoints(
    image_points, camera_matrix, dist_coeffs, P=camera_matrix).reshape(-1, 2)
print(image_points_undistorted)
# 计算相机外参
success, rotation_vector, translation_vector = cv2.solvePnP(
    world_points, image_points_undistorted, camera_matrix, dist_coeffs)
if not success:
    raise ValueError("solvePnP failed to find a valid solution")

# 将旋转向量转换为旋转矩阵
rotation_matrix, _ = cv2.Rodrigues(rotation_vector)

# 定义一个图像坐标转换为世界坐标的函数
def image_to_world(image_point):
    # 校正图像点
    image_point_undistorted = cv2.undistortPoints(
        np.expand_dims(np.array([image_point], dtype=np.float32), axis=1),
        camera_matrix, dist_coeffs)
    # 将图像点转换为相机坐标
    image_point_cam = np.array([image_point_undistorted[0][0][0],
                               image_point_undistorted[0][0][1], 1.0])
    image_point_cam = image_point_cam.reshape((3, 1))
    #print(image_point_cam)
    # 计算世界坐标
    rotation_matrix_inv = np.linalg.inv(rotation_matrix)
    translation_vector_reshaped = translation_vector.reshape((3, 1))
    #print(translation_vector_reshaped)
    world_point_cam = np.dot(rotation_matrix_inv, image_point_cam - translation_vector_reshaped)

    print("rotation_matrix_inv", rotation_matrix_inv)
    print("translation_vector_reshaped", translation_vector_reshaped)  

    # 将相机坐标转换为世界坐标
    world_point = world_point_cam.flatten()
    print(world_point.shape)
    return world_point

# 使用示例
image_point = [76, 30]
world_point = image_to_world(image_point)
print("World coordinates:", world_point)


