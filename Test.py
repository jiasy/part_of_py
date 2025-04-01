import Main

if __name__ == "__main__":
    _main = Main.Main()
    # # 框架的测试，以及引用类的测试
    _testApp = _main.getAppByName("Test")
    _testApp.testStart()
