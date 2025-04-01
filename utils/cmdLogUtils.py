# 命令行日志工具，python 作为脚本被调用的时候，在命令行中的特殊输出
# green
def log(msg_):
    print('\033[1;32;40m%s\033[0m' % msg_)


# red
def err(msg_):
    print('\033[1;31;40m%s\033[0m' % msg_)


# yellow
def warn(msg_):
    print('\033[1;33;40m%s\033[0m' % msg_)


if __name__ == '__main__':
    log("1")
    err("1")
    warn("1")
