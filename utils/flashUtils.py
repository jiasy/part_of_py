import subprocess
import os

_flashAppPath = "/Applications/Adobe Animate 2021/Adobe Animate 2021.app/Contents/MacOS/Adobe Animate 2021"

def runJsfl(flaPath_: str, jsflPath_: str):
    if flaPath_ is None or jsflPath_ is None:
        return
    if not os.path.exists(flaPath_) or not os.path.exists(jsflPath_):
        print("文件不存在")
        return
    # 定义命令列表
    command_list = [_flashAppPath, flaPath_, '-commands', jsflPath_]
    # 执行命令
    proc = subprocess.Popen(command_list, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # 输出命令结果
    stdout, stderr = proc.communicate()
    print(stdout.decode())
    print(stderr.decode())


if __name__ == "__main__":
    runJsfl()
