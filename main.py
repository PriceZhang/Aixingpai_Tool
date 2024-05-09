import time
import os
from paddleocr import PaddleOCR
import pyautogui
import numpy as np
from datetime import datetime

from aixing_tools import set_coordinate, InferOcrApp, calculate_text_difference, calculate_center, height, width
from aixing_tools import Check_g_com, buy_function, sell_function

os.environ["KMP_DUPLICATE_LIB_OK"]="TRUE"

shop_list = []
coordinate_dict = {}
last_com_time = {}
app_center_x = 0
app_center_y = height//2
def BuySellFunction(g_com, g_time, g_point):
    # 0. 进我的委拍，记录数量
    pyautogui.moveTo(coordinate_dict["我的point"][0], coordinate_dict["我的point"][1])
    pyautogui.click()
    time.sleep(2)
    # 截取委拍位置的图像
    result = InferOcrApp(coordinate_dict["委拍数量box"][0], coordinate_dict["委拍数量box"][1], coordinate_dict["委拍数量box"][2], coordinate_dict["委拍数量box"][3])
    wei_pai_num_1 = int(result[0][-1][1][0])

    # 回首页并进入产品界面
    pyautogui.moveTo(coordinate_dict["首页point"][0], coordinate_dict["首页point"][1])
    pyautogui.click()
    time.sleep(2)
    pyautogui.moveTo(g_point[0], g_point[1])
    pyautogui.click()
    time.sleep(2)
    # 先进委拍，点上全部看数量，数量不为0，则继续点委拍，数字为0，则去参拍
    sell_flag = sell_function(coordinate_dict, g_time)
    buy_flag = 0
    time.sleep(2)
    pyautogui.moveTo(coordinate_dict["返回point"][0], coordinate_dict["返回point"][1])
    pyautogui.click()
    time.sleep(2)
    if sell_flag == 0:
        # 非委拍，进参拍
        pyautogui.moveTo(coordinate_dict["首页point"][0], coordinate_dict["首页point"][1])
        pyautogui.click()
        time.sleep(2)
        pyautogui.moveTo(g_point[0], g_point[1])
        pyautogui.click()
        time.sleep(2)
        buy_flag = buy_function(coordinate_dict, g_time)
        time.sleep(2)
        pyautogui.moveTo(coordinate_dict["返回point"][0], coordinate_dict["返回point"][1])
        pyautogui.click()
        time.sleep(2)

        if buy_flag == 0:
            print("委拍和购买均失败")
            return
    else:
        # 2. 如果刚才是委拍，返回我的，查看当前委拍数量，如果委拍数量与之前记录不一样，证明委拍成功
        pyautogui.moveTo(coordinate_dict["首页point"][0], coordinate_dict["首页point"][1])
        pyautogui.click()
        time.sleep(5)
        pyautogui.moveTo(coordinate_dict["我的point"][0], coordinate_dict["我的point"][1])
        pyautogui.click()
        # 截取委拍位置的图像
        result = InferOcrApp(coordinate_dict["委拍数量box"][0], coordinate_dict["委拍数量box"][1], coordinate_dict["委拍数量box"][2], coordinate_dict["委拍数量box"][3])
        wei_pai_num_2 = int(result[0][-1][1][0])
        if wei_pai_num_2 != wei_pai_num_1:
            print("委拍成功，当前委拍数为 " + str(wei_pai_num_2))
            while True:
                # 2.1 如果委拍成功，不停的点返回，再点我的，直到委拍数量变化
                pyautogui.moveTo(coordinate_dict["首页point"][0], coordinate_dict["首页point"][1])
                pyautogui.click()
                time.sleep(2)
                pyautogui.moveTo(coordinate_dict["我的point"][0], coordinate_dict["我的point"][1])
                pyautogui.click()
                wei_pai_num_3 = InferOcrApp(coordinate_dict["委拍数量box"][0], coordinate_dict["委拍数量box"][1], coordinate_dict["委拍数量box"][2], coordinate_dict["委拍数量box"][3])
                if wei_pai_num_3 != wei_pai_num_2:
                    print("委拍的物品已拍卖！")
                    break
        else:
            print("之前委拍数为 " + str(wei_pai_num_1) + "现在委拍数为 " + str(wei_pai_num_2))
            print("直接进入参拍")
        # 2.2 委拍完成，进参拍，拍完return
        pyautogui.moveTo(coordinate_dict["首页point"][0], coordinate_dict["首页point"][1])
        pyautogui.click()
        time.sleep(2)
        pyautogui.moveTo(g_point[0], g_point[1])
        pyautogui.click()
        time.sleep(2)
        buy_function(coordinate_dict, g_time)
        pyautogui.moveTo(coordinate_dict["返回point"][0], coordinate_dict["返回point"][1])
        pyautogui.click()
        time.sleep(2)
        return

def Shopping_time(g_com, g_time):
    pyautogui.click(coordinate_dict["首页point"][0], coordinate_dict["首页point"][1])
    time.sleep(2)
    # 2. 获取屏幕中模拟器截图
    scoll_time = 0
    while True: # 添加循环，每次一循环滚轮滚一次
        result = InferOcrApp()
        for idx in range(len(result)):
            res = result[idx]
            for line in res:
                if calculate_text_difference(g_com, line[-1][0]) >= 0.9:
                    # 找到了，返回边框中心点
                    g_com_p = calculate_center(line[0])
                    BuySellFunction(g_com, g_time, g_com_p)
                    pyautogui.moveTo(coordinate_dict["首页point"][0], coordinate_dict["首页point"][1])
                    pyautogui.click()
                    time.sleep(1)
                    pyautogui.moveTo(app_center_x, app_center_y)
                    time.sleep(1)
                    pyautogui.scroll(500)
                    time.sleep(1)
                    return
        if scoll_time > 3:
            print(f"没有【{g_com}】这个商品！！")
            pyautogui.moveTo(app_center_x, app_center_y)
            pyautogui.scroll(500)
            time.sleep(1)
            return
        scoll_time += 1
        pyautogui.moveTo(app_center_x, app_center_y)
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
    # 写入当前版本的各关键坐标文件
    app_center_x = set_coordinate()
    # print(app_center_x)
    # app_center_x = 1440
    pyautogui.moveTo(app_center_x, app_center_y)
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
            if abs(G_time-trans_time) <= 30 and abs(trans_time-last_com_time[Com]) > 36000:
            # print(G_time)
            # print(trans_time)
            # print(last_com_time[Com])
                Shopping_time(Com, G_time)
                last_com_time[Com] = trans_time
        time.sleep(10)


