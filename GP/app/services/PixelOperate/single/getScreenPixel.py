import pyautogui
from PIL import ImageGrab
import signal
import AppKit
from pynput import mouse
import sys
from utils import printUtils
import pyperclip


def get_mouse_pixel_color():
    x, y = pyautogui.position()  # 获取鼠标当前位置
    # 从固定的位置取颜色
    x = 950
    y = 850
    screenshot = ImageGrab.grab()  # 获取屏幕截图
    # screenshot_LAB = screenshot.convert('P')
    pixel_color = screenshot.getpixel((x, y))  # 获取鼠标位置的像素颜色
    return pixel_color


def get_front_application_ID():
    # 获取最前面的应用程序
    front_app = AppKit.NSWorkspace.sharedWorkspace().frontmostApplication()
    # 获取应用程序的bundle identifier
    return front_app.bundleIdentifier()


def bring_app_to_front(app_ID_):
    # 获取正在运行的所有应用程序
    _runningApps = AppKit.NSRunningApplication.runningApplicationsWithBundleIdentifier_(app_ID_)
    for app in _runningApps:
        _runningAppID = app.bundleIdentifier()
        if _runningAppID == app_ID_:  # 激活应用
            app.activateWithOptions_(AppKit.NSApplicationActivateIgnoringOtherApps)
            # print(f"    {app_ID_} 匹配，打开")
            return
        else:
            print(f"    当前 {_runningAppID} 和 {app_ID_} 不匹配")
    print(f"ERROR :  {app_ID_} 不在运行中")
    sys.exit(1)


def on_click(x, y, button, pressed):
    if pressed:
        # print(f"Mouse clicked at ({x}, {y}) with {button}")
        return False  # 返回False将停止监听


# 定义一个要执行的清理函数
def cleanup(signum, frame):
    unqColorList = list(set(colorList))
    _colorListStr = ""
    for _i in range(len(unqColorList)):
        _color = unqColorList[_i]
        _colorListStr = f"{_colorListStr}{_color},"
    pyperclip.copy(_colorListStr)  # 拷贝到剪切板
    print(f"拷贝到 {len(unqColorList)} 个颜色")
    sys.exit(0)


colorList = []

if __name__ == "__main__":

    # _frontAppID = get_front_application_ID()
    # print('_frontAppID = ' + str(_frontAppID))
    # sys.exit(1)

    _appBundleID = "com.apple.Preview"
    bring_app_to_front("com.apple.DigitalColorMeter")  # 取色器
    bring_app_to_front(_appBundleID)  # 预览

    # 注册信号处理器
    signal.signal(signal.SIGINT, cleanup)  # 捕捉 CTRL+C
    signal.signal(signal.SIGTERM, cleanup)  # 捕捉终止信号
    while True:
        with mouse.Listener(on_click=on_click) as listener:  # 监听鼠标点击事件
            listener.join()  # 等待点击
        color = get_mouse_pixel_color()  # 测试获取鼠标像素颜色
        colorList.append(color[:3])
        print(f"鼠标当前位置的像素颜色为: {color}")
        _front_app_ID = get_front_application_ID()  # 最前方的应用
        if _appBundleID != _front_app_ID:
            print(f"ERROR : {_appBundleID} 不在最前方，停止小本运行。{_front_app_ID} 弹出")
            sys.exit(1)
        else:
            # print(f"当前最前方的窗口为 : {_front_app_ID}")
            continue
