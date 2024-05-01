from paddleocr import PaddleOCR, draw_ocr
import pyautogui
from io import BytesIO
import numpy as np
from PIL import Image
pyautogui.moveTo(100, 150)
pyautogui.rightClick()
# Paddleocr目前支持的多语言语种可以通过修改lang参数进行切换
# 例如`ch`, `en`, `fr`, `german`, `korean`, `japan`
# ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # need to run only once to download and load model into memory
# img_path = './11.jpg'
# 截取屏幕
# screenshot = pyautogui.screenshot()
# screenshot.save('result.jpg')
# img_path = np.array(screenshot)
# print(type(img_path))
# result = ocr.ocr(img_path, cls=True)
# for idx in range(len(result)):
#     res = result[idx]
#     for line in res:
#         print(line)
#
# # 显示结果
# result = result[0]
# # image = Image.open(img_path).convert('RGB')
# image = screenshot
# boxes = [line[0] for line in result]
# txts = [line[1][0] for line in result]
# scores = [line[1][1] for line in result]
# im_show = draw_ocr(image, boxes, txts, scores, font_path='./simfang.ttf')
# im_show = Image.fromarray(im_show)
# im_show.save('result.jpg')