###########################################
# 图像预处理示例
# 
#
#
###########################################

import os
import cv2
import numpy as np

import pdb


def img2grey(img:str, output:str="output")->str:
    # 彩色图像 转换为灰度图像
    img_cv = cv2.imread(img)
    gray_img = cv2.cvtColor(img_cv, cv2.COLOR_BGR2GRAY)
    cv2.imwrite( os.path.join(output,'img2gray.png'), gray_img)

def img_inverse(img:str, output:str="output")->list:
    # 图像反转
    img = cv2.imread(img)
    if len(img.shape) == 2:
        img = cv2.bitwise_not(img)
    elif len(img.shape) == 3:
        img[:, :, 0] = cv2.bitwise_not(img[:, :, 0])
        img[:, :, 1] = cv2.bitwise_not(img[:, :, 1])
        img[:, :, 2] = cv2.bitwise_not(img[:, :, 2])
    cv2.imwrite( os.path.join(output,'img2inverse.png'), img)
    return img

def img_anno_cox(img_cv:list, HSV_Scope:list=[])->list:
    # 按颜色提取边框
    img_hsv = cv2.cvtColor(img_cv, cv2.COLOR_BGR2HSV)
    # 设定色彩的HSV范围
    lower_hsv = np.array(HSV_Scope[0])
    upper_hsv = np.array(HSV_Scope[1])
    # 创建彩色区域的二值掩码
    mask = cv2.inRange(img_hsv, lower_hsv, upper_hsv)
    bbox = cv2.boundingRect(mask)

    if bbox is not None:
        print(f"Object detected: {bbox}")
        x, y, w, h = bbox
        return bbox
    else:
        print("Object not detected")
        return None
    # # 找到图像中的直线条
    # contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)    

    # for contour in contours:
    #     x, y, w, h = cv2.boundingRect(contour)
    #     # 提取当前颜色区域的边界框
    #     bbox = (x, y, x+w, y+h)
    #     print(f"Rectangle detected with coordinates: Top-left: ({x}, {y}), 高，宽: ({w}, {h})")
    
def img_bbox(img:str, bbox:list=(59, 41, 507, 45), output:str="output")->None:
    x, y, w, h = bbox
    # top_left = (top_left_y, top_left_x)
    # bottom_right = (bottom_right_y, bottom_right_x)
    # label_img = img[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]
    label_bbox = img[x:x+w, y:y-h]
    cv2.imwrite(os.path.join(output,f'output_{x}_{y}.png'), label_bbox)

def img_blocks(img:str, block_size:list=(632.5,474), output:str="output")->list:
    ## 按尺寸分割图像
    img_cv = cv2.imread(img)
    height, width = img_cv.shape[:2]
    if width <= block_size[0]:
        return img_cv
    blocks_horiz = width // block_size[0]
    # blocks_vert = int(height // block_size[1])
    # 遍历并切分图像
    blocks = []
    for w in range(int(blocks_horiz)):
        left_x = w * block_size[0]
        left_y = 0 * block_size[1]
        # 获取小块图像
        breakpoint()
        block = img_cv[0:left_y+block_size[1],left_x:left_x+block_size[0]]
        # block = img_cv[start_y:start_y + block_size[1], start_x:start_x + block_size[0]]
        cv2.imwrite(os.path.join(output,f'output_{w}.png'), block)
        blocks.append(block)

def rgb2hsv(r, g, b):
    # R, G, B values are divided by 255 
    # to change the range from 0..255 to 0..1: 
    r, g, b = r / 255.0, g / 255.0, b / 255.0
    # h, s, v = hue, saturation, value 
    cmax = max(r, g, b)    # maximum of r, g, b 
    cmin = min(r, g, b)    # minimum of r, g, b 
    diff = cmax-cmin       # diff of cmax and cmin. 
    # if cmax and cmax are equal then h = 0 
    if cmax == cmin:  
        h = 0
    # if cmax equal r then compute h 
    elif cmax == r:  
        h = (60 * ((g - b) / diff) + 360) % 360
    # if cmax equal g then compute h 
    elif cmax == g: 
        h = (60 * ((b - r) / diff) + 120) % 360
    # if cmax equal b then compute h 
    elif cmax == b: 
        h = (60 * ((r - g) / diff) + 240) % 360
  
    # if cmax equal zero 
    if cmax == 0: 
        s = 0
    else: 
        s = (diff / cmax) * 100
  
    # compute v 
    v = cmax * 100
    return h, s, v 

if __name__ == "__main__":
    img = os.path.abspath(r'_static/img/_______17003598097052_20231119101223.png')
    output = os.path.abspath(r"output")
    r,g,b = 255,190,0
    yellow_lower = (20, 100, 100)
    yellow_upper = (30, 255, 255)
    hsv = rgb2hsv(r,g,b)
    # breakpoint()
    HSV_Scope = [(hsv[0]-10,hsv[1]-10,hsv[2]-10),(hsv[0]+10,hsv[1]+10,hsv[2]+10)]
    HSV_Scope = [(20, 100, 100), (30, 255, 255)]
    # img2grey(img)     ## 灰度
    # img_inverse(img)  ## 反向
    # img_anno_cox(img)
    blocks = img_blocks(img)
    anno_block = []

    for block in blocks:
        bbox = img_anno_cox(block, HSV_Scope)
        img_bbox(block, bbox)
