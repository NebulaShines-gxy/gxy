
import math

P = 0
A1 = 86
A2 = 138
A3 = 75
A4 = 160
MAX_LEN = A2 + A3 + A4
MAX_HIGH = A1 + A2 + A3 + A4
alpha = 180


def cos(degree):
    return math.cos(math.radians(degree))


def sin(degree):
    return math.sin(math.radians(degree))


def atan2(v1, v2):
    rad = math.atan2(v1, v2)
    return math.degrees(rad)


def _j_degree_convert(joint, j_or_deg):
    # ��j1-j4�ͻ�е�۵ĽǶȱ��ﻥ��
    if joint == 1:
        res = j_or_deg
    elif joint == 2 or joint == 3 or joint == 4:
        res = 90 - j_or_deg
    else:
        # ֻ������1-4�ؽ�
        raise ValueError
    return res


def _valid_degree(joint, degree):
    if 0 <= degree <= 180:
        return True

    else:
        #print('joint {} is invalid degree {}'.format(joint, degree))
        return False


def _valid_j(joint, j):
    if j is None:
        return False
    degree = _j_degree_convert(joint, j)
    if 0 <= degree <= 180:
        return True
    else:
        #print('joint {} is invalid j:{} degree {}'.format(joint, j, degree))
        return False


def _out_of_range(lengh, height):
    if height > MAX_HIGH:
        #print('over{}{}'.format(height, MAX_HIGH))
        return True
    if lengh > MAX_LEN:
        #print('over{}  {}'.format(lengh, MAX_LEN))
        return True
    return False


def _calculate_j1(x, y, z):
    length = round(math.sqrt(pow((y + P), 2) + pow(x, 2)), 2)

    if length == 0:
        j1 = 0  # ������������
    else:
        j1 = atan2((y + P), x)
    hight = z
    return j1, length, hight


def _calculate_j3(L, H):
    cos3 = (L ** 2 + H ** 2 - A2 ** 2 - A3 ** 2) / (2 * A2 * A3)
    # cos3=(pow(L,2)+pow(H,2))-(pow(A2,2)+pow(A3,2)/2*A2*A3)
    if (cos3 ** 2 > 1):
        return None
    sin3 = math.sqrt(1 - cos3 ** 2)
    j3 = atan2(sin3, cos3)
    return j3


def _calculate_j2(L, H, j3):
    K1 = A2 + A3 * cos(j3)
    K2 = A3 * sin(j3)
    w = atan2(K2, K1)
    j2 = atan2(L, H) - w
    return j2


def _calculate_j4(j2, j3, alpha ):
    j4 = alpha - j2 - j3
    return j4


def _xyz_alpha_to_j123(x, y, z, alpha):
    valid = False
    j1, j2, j3, j4 = None, None, None, None
    j1, length, height = _calculate_j1(x, y, z)
    if _valid_j(1, j1) and not _out_of_range(length, height):
        L = length - A4 * sin(alpha)
        H = height - A4 * cos(alpha) - A1
        j3 = _calculate_j3(L, H)
        if _valid_j(3, j3):
            j2 = _calculate_j2(L, H, j3)
            if _valid_j(2, j2):
                j4 = _calculate_j4(j2, j3, alpha)
                if _valid_j(4, j4):
                    valid = True
    return valid, j1, j2, j3, j4


def _xyz_to_j123(x,y, z, alpha=alpha):
    MIN_ALPHA = 90  # j2+j3+j4 min value, ���һ��joint�������
    valid = False
    j1, j2, j3, j4 = None, None, None, None
    while alpha >= MIN_ALPHA and not valid:
        valid, j1, j2, j3, j4 = _xyz_alpha_to_j123(x, y, z, alpha)
        if not valid:
            alpha -= 1
    return valid, j1, j2, j3, j4


def backward_kinematics(x, y, z, alpha=alpha):
    x = int(x)
    y = int(y)
    z = int(z)
    #print('x:{} y:{} z:{} alpha:{}'.format(x, y, z, alpha))

    if z < 0:
        print('z >=0')
        raise ValueError
    if y < 0:
        print('y >=0')
        raise ValueError

    valid, j1, j2, j3, j4 = _xyz_to_j123(x, y, z, alpha)
    deg1, deg2, deg3, deg4 = None, None, None, None
    if valid:
        deg1 = round(_j_degree_convert(1, j1), 2)
        deg2 = round(_j_degree_convert(2, j2), 2)
        deg3 = round(_j_degree_convert(3, j3), 2)
        deg4 = round(_j_degree_convert(4, j4), 2)
        deg1 = int(deg1)
        deg2 = int(deg2)
        deg3 = int(deg3)
        deg4 = int(deg4)

    #print('valid:{},deg1:{},deg2:{},deg3:{},deg4:{}'.format(valid, deg1, deg2, deg3, deg4))
    #print('{} [{},{},{},{}]'.format(valid, deg1, deg2, deg3, deg4))

    return valid, deg1, deg2, deg3, deg4


def forward_kinematics(deg1, deg2, deg3, deg4):
    valid = False
    if not _valid_degree(1, deg1) or not _valid_degree(2, deg2) or not _valid_degree(3, deg3) or not _valid_degree(4,
                                                                                                                   deg4):
        return valid, None, None, None
    j1 = _j_degree_convert(1, deg1)
    j2 = _j_degree_convert(2, deg2)
    j3 = _j_degree_convert(3, deg3)
    j4 = _j_degree_convert(4, deg4)
    length = A2 * sin(j2) + A3 * sin(j2 + j3) + A4 * sin(j2 + j3 + j4)
    height = A1 + A2 * cos(j2) + A3 * cos(j2 + j3) + A4 * cos(j2 + j3 + j4)
    alpha = j2 + j3 + j4

    z = round(height, 2)
    x = round(length * cos(j1))
    y = round(length * sin(j1) - P)

    # ��������ı߽�
    if 0 <= y and z >= 0:
        valid = True

    #print('valid:{},x:{},y:{},z:{},lenghth:{},height:{},alpha:{}'.format(valid, x, y, z, round(length, 2),
     #                                                                    round(height, 2), alpha))

    return valid, x, y, z


def test_ok(x, y, z):
    valid, deg1, deg2, deg3, deg4 = backward_kinematics(x, y, z, alpha=alpha)
    if valid:
        valid, x1, y1, z1 = forward_kinematics(deg1, deg2, deg3, deg4)
        if abs(x1 - x) > 0.5 or abs(y1 - y) > 0.5 or abs(z1 - z) > 0.5:
            print('err')
        else:
            print('ok')


if __name__ == '__main__':
   
    a, b, c, d, e=backward_kinematics(84, 98, 20)
    print(a, b, c, d, e)

