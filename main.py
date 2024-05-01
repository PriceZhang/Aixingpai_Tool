import time

import cv2
from paddleocr import PaddleOCR, draw_ocr
import pyautogui
from io import BytesIO
import numpy as np
from PIL import Image
from datetime import datetime
from difflib import SequenceMatcher
# 加载paddleOcr模型
ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # need to run only once to download and load model into memory

width_app = 560  # app的分辨率宽度
width = 1920
height = 1080
left = (width - width_app) // 2
top = 0
right = left + width_app
bottom = height

shop_list = []
coordinate_dict = {}
last_com_time = {}
def InferOcrApp(x1=left, y1=0, x2=right, y2=bottom):
    screenshot = pyautogui.screenshot()
    # width, height = screenshot.size
    app_image = screenshot.crop((x1, y1, x2, y2))
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
    center[0] = center[0]+left
    center[1] = center[1]+top
    return center
# 计算文本距离
def calculate_text_difference(text1, text2):
    matcher = SequenceMatcher(None, text1, text2)
    return matcher.ratio()
def BuySellFunction(g_com, g_time, g_point, scroll_time):
    # 0. 进我的委拍，记录数量
    print(coordinate_dict["我的point"])
    pyautogui.moveTo(coordinate_dict["我的point"][0], coordinate_dict["我的point"][1])
    pyautogui.click()
    time.sleep(2)
    # 截取委拍位置的图像
    result = InferOcrApp(coordinate_dict["委拍数量box"][0], coordinate_dict["委拍数量box"][1], coordinate_dict["委拍数量box"][2], coordinate_dict["委拍数量box"][3])
    wei_pai_num = int(result[0][-1][1][0])
    # 1. 先进委拍，看看数量是否为0
    # 1.1 如果不为0， 进委拍， 点最大数量，一直点委派，每次点完看看有没有【取消】的字段，有就继续，没有就下一环节
    # 1.2 如果为0，进参拍，点最大数量，一直参拍，每次点完看有没有取消字段，有就继续，没有就参拍完成，直接return
    if wei_pai_num == 0:
        print("当前委拍为0")
        # 进首页
        pyautogui.moveTo(coordinate_dict["首页point"][0], coordinate_dict["首页point"][1])
        pyautogui.click()
        time.sleep(1)
        for i in range(0, scroll_time):
            pyautogui.moveTo(width/2, height/2)
            pyautogui.scroll(-100)
        print(g_point)
        pyautogui.moveTo(g_point[0], g_point[1])
        pyautogui.click()
        time.sleep(1)
        pyautogui.moveTo(coordinate_dict["参拍1point"][0], coordinate_dict["参拍1point"][1])
        pyautogui.click()
        time.sleep(1)
        pyautogui.moveTo(coordinate_dict["全部point"][0], coordinate_dict["全部point"][1])
        pyautogui.click()
        time.sleep(1)
        pyautogui.moveTo(coordinate_dict["参拍2point"][0], coordinate_dict["参拍2point"][1])
        pyautogui.click()
        time.sleep(2)
        while True:
            result = InferOcrApp(coordinate_dict["取消box"][0], coordinate_dict["取消box"][1], coordinate_dict["取消box"][2], coordinate_dict["取消box"][3])
            try:
                if result and result[0][0][1][0] == "取消":
                    pyautogui.moveTo(coordinate_dict["全部point"][0], coordinate_dict["全部point"][1])
                    pyautogui.click()
                    time.sleep(0.25)
                    pyautogui.moveTo(coordinate_dict["参拍2point"][0], coordinate_dict["参拍2point"][1])
                    pyautogui.click()
                    time.sleep(1)
                else:
                    print("抢完了！！！")
                    return
            except:
                print("抢完了！")
                return
    else:
        print("当前委拍为 "+str(wei_pai_num))
        # 进首页
        pyautogui.moveTo(coordinate_dict["首页point"][0], coordinate_dict["首页point"][1])
        pyautogui.click()
        time.sleep(1)
        for i in range(0, scroll_time):
            pyautogui.moveTo(width/2, height/2)
            pyautogui.scroll(-100)
        print(g_point)
        pyautogui.moveTo(g_point[0], g_point[1])
        pyautogui.click()
        time.sleep(1)
        pyautogui.moveTo(coordinate_dict["委拍1point"][0], coordinate_dict["委拍1point"][1])
        pyautogui.click()
        time.sleep(1)
        pyautogui.moveTo(coordinate_dict["全部point"][0], coordinate_dict["全部point"][1])
        pyautogui.click()
        time.sleep(1)
        pyautogui.moveTo(coordinate_dict["委拍2point"][0], coordinate_dict["委拍2point"][1])
        pyautogui.click()
        time.sleep(2)
        while True:
            result = InferOcrApp(coordinate_dict["取消box"][0], coordinate_dict["取消box"][1], coordinate_dict["取消box"][2], coordinate_dict["取消box"][3])
            try:
                if result and result[0][0][1][0] == "取消":
                    pyautogui.moveTo(coordinate_dict["全部point"][0], coordinate_dict["全部point"][1])
                    pyautogui.click()
                    time.sleep(0.25)
                    pyautogui.moveTo(coordinate_dict["委拍2point"][0], coordinate_dict["委拍2point"][1])
                    pyautogui.click()
                    time.sleep(1)
                else:
                    print("委拍完了！！！")
                    break
            except:
                print("委拍完了！")
                break
    pyautogui.moveTo(coordinate_dict["返回point"][0], coordinate_dict["返回point"][1])
    pyautogui.click()
    # 2. 如果刚才是委拍，返回我的，查看当前委拍数量，如果委拍数量与之前记录不一样，证明委拍成功
    if wei_pai_num != 0:
        while True:
            pyautogui.moveTo(coordinate_dict["首页point"][0], coordinate_dict["首页point"][1])
            pyautogui.click()
            time.sleep(1)
            pyautogui.moveTo(coordinate_dict["我的point"][0], coordinate_dict["我的point"][1])
            pyautogui.click()
            # 截取委拍位置的图像
            result = InferOcrApp(coordinate_dict["委拍数量box"][0], coordinate_dict["委拍数量box"][1], coordinate_dict["委拍数量box"][2], coordinate_dict["委拍数量box"][3])
            now_wei_pai_num = int(result[0][-1][1][0])
            if now_wei_pai_num != wei_pai_num:
                break

        while True:
            # 2.1 如果委拍成功，不停的点返回，再点我的，直到委拍数量减少
            pyautogui.moveTo(coordinate_dict["首页point"][0], coordinate_dict["首页point"][1])
            pyautogui.click()
            time.sleep(1)
            pyautogui.moveTo(coordinate_dict["我的point"][0], coordinate_dict["我的point"][1])
            pyautogui.click()
            result = InferOcrApp(coordinate_dict["委拍数量box"][0], coordinate_dict["委拍数量box"][1], coordinate_dict["委拍数量box"][2], coordinate_dict["委拍数量box"][3])
            if now_wei_pai_num != int(result[0][-1][1][0]):
                print("委拍的物品已拍卖！")
                break
        # 2.2 委拍完成，进参拍，拍完return
        pyautogui.moveTo(coordinate_dict["首页point"][0], coordinate_dict["首页point"][1])
        pyautogui.click()
        time.sleep(1)
        for i in range(0, scroll_time):
            pyautogui.moveTo(width / 2, height / 2)
            pyautogui.scroll(-100)
        print(g_point)
        pyautogui.moveTo(g_point[0], g_point[1])
        pyautogui.click()
        time.sleep(1)
        pyautogui.moveTo(coordinate_dict["参拍1point"][0], coordinate_dict["参拍1point"][1])
        pyautogui.click()
        time.sleep(1)
        pyautogui.moveTo(coordinate_dict["全部point"][0], coordinate_dict["全部point"][1])
        pyautogui.click()
        time.sleep(1)
        pyautogui.moveTo(coordinate_dict["参拍2point"][0], coordinate_dict["参拍2point"][1])
        pyautogui.click()
        time.sleep(2)
        while True:
            result = InferOcrApp(coordinate_dict["取消box"][0], coordinate_dict["取消box"][1], coordinate_dict["取消box"][2], coordinate_dict["取消box"][3])
            try:
                if result and result[0][0][1][0] == "取消":
                    pyautogui.moveTo(coordinate_dict["全部point"][0], coordinate_dict["全部point"][1])
                    pyautogui.click()
                    time.sleep(0.25)
                    pyautogui.moveTo(coordinate_dict["参拍2point"][0], coordinate_dict["参拍2point"][1])
                    pyautogui.click()
                    time.sleep(1)
                else:
                    print("抢完了！！！")
                    return
            except:
                print("抢完了！")
                return
def Shopping_time(g_com, g_time):
    # 2. 获取屏幕中模拟器截图
    scoll_time = 0
    find_flag = False
    g_com_p = (0,0)
    while True: # 添加循环，每次一循环滚轮滚一次
        result = InferOcrApp()
        for idx in range(len(result)):
            res = result[idx]
            for line in res:
                if calculate_text_difference(g_com, line[-1][0]) >= 0.85:
                    # 找到了，返回边框中心点
                    find_flag = True
                    g_com_p = calculate_center(line[0])
        if find_flag:
            # 进入抢货函数
            BuySellFunction(g_com, g_time, g_com_p, scoll_time)
            break
        else:
            if scoll_time > 3:
                print(f"没有【{g_com}】这个商品！！")
                pyautogui.moveTo(width / 2, height / 2)
                pyautogui.scroll(500)
                return
            scoll_time += 1
            pyautogui.moveTo(width/2, height/2)
            pyautogui.scroll(-100)
            time.sleep(2)


if __name__ == "__main__":
    # 0. 加载抢货、卖货名单、时间
    with open("shop_list.txt", "r", encoding="utf8") as f:
        for item in f.readlines():
            item = item.strip()
            commodity, deadtime = item.split()
            shop_list.append((commodity, deadtime))
            last_com_time[commodity] = 0
    # 加载坐标字典
    with open("coordinate_dict.txt", "r", encoding="utf8") as f:
        for item in f.readlines():
            item = item.strip()
            c_name, coordinate = item.split()
            numbers_str_list = coordinate.split(",")
            coordinate_dict[c_name] = list(map(int, numbers_str_list))
    print(coordinate_dict)



    while True:
    # 提取时、分、秒
        now = datetime.now()
        hour = now.hour
        minute = now.minute
        second = now.second
        trans_time = hour*60*60 + minute*60 + second
        for Com, GotTime in shop_list:
            G_H, G_M, G_S = GotTime.split(".")
            G_time = int(G_H)*60*60 + int(G_M)*60 + int(G_S)
            # if abs(G_time-trans_time) <= 30 and abs(trans_time-last_com_time[Com])>36000:
            print(G_time)
            print(trans_time)
            print(last_com_time[Com])
            Shopping_time(Com, GotTime)
            last_com_time[Com] = trans_time
        time.sleep(10)


