from pynput.keyboard import Controller, Key
import time
# 创建一个键盘控制器实例
keyboard_controller = Controller()


while True:
    # 模拟按下 Ctrl+Tab 组合键
    # 首先按下 Ctrl 键
    keyboard_controller.press(Key.ctrl)
    # 然后按下并释放 Tab 键
    keyboard_controller.press(Key.tab)
    keyboard_controller.release(Key.tab)
    # 最后释放 Ctrl 键
    keyboard_controller.release(Key.ctrl)
    time.sleep(1)