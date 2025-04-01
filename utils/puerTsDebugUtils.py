import sys

import websocket
import json
import threading
from threading import Condition
from queue import Queue

currentID = 0


# enable 默认创建环境 1
def getEnableObj():
    global currentID
    currentID = currentID + 1
    return {"id": currentID, "method": "Runtime.enable"}


# 清理 1 ，就是清理默认
def getDisposeContext():
    global currentID
    currentID = currentID + 1
    return {"id": currentID, "method": "Runtime.disposeContext", "params": {"executionContextId": 1}}


def getCodeObj(code_: str):
    global currentID
    currentID = currentID + 1
    return {"id": currentID, "method": "Runtime.evaluate", "params": {"expression": code_, "contextId": 1}}


def getDisableObj():
    global currentID
    currentID = currentID + 1
    return {"id": currentID, "method": "Runtime.disable"}


class V8RuntimeExecutor:
    def __init__(self, url_, jsCodeList: list[str]):
        # 删

    def execute_commands(self):
        if self.commands_queue.empty():
            print("All Done")
            sys.exit(0)

        with self.condition:
            command = self.commands_queue.get()
            self.current_id = command['id']
            self.response_received = False

            print(f"Executing command: {command}")
            self.ws.send(json.dumps(command))

    def on_open(self, ws):
        print("Connection opened")
        self.execute_commands()

    def on_message(self, ws, message_):
        #删

    def on_error(self, ws, error):
        print(f"Error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        print("Connection closed")

    def run(self):
        ws_thread = threading.Thread(target=self.ws.run_forever)
        ws_thread.start()
        ws_thread.join()


if __name__ == "__main__":
    url = "ws://localhost:8080"
    jsCode = "console.log(\"Hello\")"
    executor = V8RuntimeExecutor(url, [jsCode])
    executor.run()
