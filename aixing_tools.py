import time
from difflib import SequenceMatcher
import os
import pyautogui
import cv2
import numpy as np
from paddleocr import PaddleOCR
ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # need to run only once to download and load model into memory
width = 1920
height = 1080
def InferOcrApp(x1=0, y1=0, x2=width, y2=height):
    screenshot = pyautogui.screenshot()
    # width, height = screenshot.size
    if x1 != 0 or y1 != 0:
        app_image = screenshot.crop((x1, y1, x2, y2))
    else:
        app_image = screenshot
    img_path = np.array(app_image)
    result = ocr.ocr(img_path, cls=True)
    return result


def calculate_center(points):
    # 假设 points 是按照顺时针或逆时针顺序给出的四个点
    # 例如：points = [[20.0, 551.0], [171.0, 551.0], [171.0, 567.0], [20.0, 567.0]]

    # 计算对角线的交点
    def line_intersection(p1, q1, p2, q2):
        A1 = q1[1] - p1[1]
        B1 = p1[0] - q1[0]
        C1 = A1 * p1[0] + B1 * p1[1]
        A2 = q2[1] - p2[1]
        B2 = p2[0] - q2[0]
        C2 = A2 * p2[0] + B2 * p2[1]

        determinant = A1 * B2 - A2 * B1

        if determinant == 0:
            return None  # 线段平行或重合，没有交点
        else:
            x = (B2 * C1 - B1 * C2) / determinant
            y = (A1 * C2 - A2 * C1) / determinant
            return [x, y]

            # 对角线分组

    diagonal1 = [points[0], points[2]]  # 第一个点和第三个点
    diagonal2 = [points[1], points[3]]  # 第二个点和第四个点

    # 计算对角线的交点，即四边形的中心点
    center = line_intersection(*diagonal1, *diagonal2)
    return center

def find_image_in_large(large_image, small_image_name, threshold=0.85, type="point"):
    small_image_path = os.path.join("./image", small_image_name+".png")
    # 读取大图和小图
    large_image = cv2.cvtColor(large_image, cv2.COLOR_BGR2GRAY)
    small_image = cv2.imread(small_image_path, 0)
    cv2.imwrite("large.png", large_image)
    cv2.imwrite("small.png", small_image)
    if large_image is None or small_image is None:
        print("Error loading images!")
        return None

        # 进行模板匹配
    result = cv2.matchTemplate(large_image, small_image, cv2.TM_CCOEFF_NORMED)

    # 找到匹配度的最大值及其位置
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # 检查最大匹配值是否超过设定的阈值
    print(max_val)
    print(small_image.shape)
    if max_val >= threshold:
        if type == "point":
            return max_loc[0]+(small_image.shape[1]//2), max_loc[1]+(small_image.shape[0]//2)
        else:
            return max_loc[0], max_loc[1], small_image.shape[1], small_image.shape[0]
    else:
        return None
# 计算文本距离
def calculate_text_difference(text1, text2):
    matcher = SequenceMatcher(None, text1, text2)
    return matcher.ratio()
def set_coordinate():
    app_center_x = 0
    tmp_list = []
    with open("shop_list.txt", "r", encoding="utf8") as f:
        for item in f.readlines():
            item = item.strip()
            commodity, deadtime = item.split()
            tmp_list.append(commodity)
    # 根据图片获取各个坐标
    f = open("coordinate_dict.txt", "w", encoding="utf8")

    # 初始页，确认首页、我的、我的委拍
    screenshot = np.array(pyautogui.screenshot())
    point = find_image_in_large(screenshot, "my")
    if point is None:
        print("[我的] 没找到")
        return None
    else:
        pyautogui.moveTo(point[0], point[1])
        time.sleep(2)
        app_center_x += point[0]//2
        f.write("我的point "+str(point[0])+","+str(point[1])+"\n")
        pyautogui.click()
        time.sleep(2)

    screenshot = np.array(pyautogui.screenshot())
    box = find_image_in_large(screenshot, "mysell", type="box")
    print(box)
    if box is None:
        print("[我的委拍] 没找到")
        return None
    else:
        pyautogui.moveTo(box[0]+box[2]//2, box[1]+box[3])
        time.sleep(2)
        f.write("委拍数量box "+str(box[0])+","+str(box[1])+","+str(box[0]+box[2])+","+str(box[1]+box[3]*2)+"\n")
        cv2.imwrite("test_weipai.png", screenshot[box[1]:box[1]+box[3]*2, box[0]:box[0]+box[2]])

    point = find_image_in_large(screenshot, "first")
    if point is None:
        print("[首页] 没找到")
        return None
    else:
        pyautogui.moveTo(point[0], point[1])
        time.sleep(2)
        f.write("首页point "+str(point[0])+","+str(point[1])+"\n")
        app_center_x += point[0] // 2
        pyautogui.click()
        time.sleep(2)

    # 进商品拍卖界面，确认其他点位
    for item in tmp_list:
        result = InferOcrApp()
        for idx in range(len(result)):
            res = result[idx]
            for line in res:
                if calculate_text_difference(item, line[-1][0]) >= 0.85:
                    # 找到了，返回边框中心点
                    find_flag = True
                    g_com_p = calculate_center(line[0])
                    break
            if find_flag == True:
                break
        if find_flag == True:
            break
    pyautogui.moveTo(g_com_p[0], g_com_p[1])
    time.sleep(1)
    pyautogui.click()
    time.sleep(2)
    screenshot = np.array(pyautogui.screenshot())
    point = find_image_in_large(screenshot, "buy1")
    if point is None:
        print("[参拍1] 没找到")
        return None
    else:
        pyautogui.moveTo(point[0], point[1])
        time.sleep(2)
        f.write("参拍1point "+str(point[0])+","+str(point[1])+"\n")
    point = find_image_in_large(screenshot, "sell1")
    if point is None:
        print("[委拍1] 没找到")
        return None
    else:
        pyautogui.moveTo(point[0], point[1])
        time.sleep(2)
        f.write("委拍1point "+str(point[0])+","+str(point[1])+"\n")
        pyautogui.click()
        time.sleep(2)
    screenshot = np.array(pyautogui.screenshot())
    point = find_image_in_large(screenshot, "sell2")
    if point is None:
        print("[委拍2] 没找到")
        return None
    else:
        pyautogui.moveTo(point[0], point[1])
        time.sleep(2)
        f.write("委拍2point "+str(point[0])+","+str(point[1])+"\n")
        f.write("参拍2point " + str(point[0]) + "," + str(point[1]) + "\n")
    point = find_image_in_large(screenshot, "all")
    if point is None:
        print("[全部] 没找到")
        return None
    else:
        pyautogui.moveTo(point[0], point[1])
        time.sleep(2)
        f.write("全部point "+str(point[0])+","+str(point[1])+"\n")
    point = find_image_in_large(screenshot, "cancel")
    box = find_image_in_large(screenshot, "cancel", type="box")
    if point is None:
        print("[取消] 没找到")
        return None
    else:
        pyautogui.moveTo(point[0], point[1])
        time.sleep(2)
        f.write("取消point "+str(point[0])+","+str(point[1])+"\n")
        f.write("取消box "+str(box[0])+","+str(box[1])+","+str(box[0]+box[2])+","+str(box[1]+box[3])+"\n")
        cv2.imwrite("test_weipai.png", screenshot[box[1]:box[1]+box[3], box[0]:box[0]+box[2]])
    point = find_image_in_large(screenshot, "back")
    if point is None:
        print("[返回] 没找到")
        return None
    else:
        pyautogui.moveTo(point[0], point[1])
        time.sleep(2)
        f.write("返回point "+str(point[0])+","+str(point[1])+"\n")
        pyautogui.click()
        time.sleep(2)
    print("所有的点位都已找到")
    return app_center_x
