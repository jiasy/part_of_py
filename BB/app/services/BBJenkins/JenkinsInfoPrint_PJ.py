#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import jenkins
from utils import printUtils
from utils import jenkinsUtils

CUR_DIR = os.path.abspath('.')



if __name__ == '__main__':
    server = jenkins.Jenkins('http://网址:端口/', username='root', password='boqugame')
    user = server.get_whoami()
    version = server.get_version()
    print('Hello %s from Jenkins %s' % (user['fullName'], version))
    # 打印 server 的 job 信息
    jobs = server.get_jobs()
    printUtils.printPyObjAsKV("jobs", jobs)
    nodes = server.get_nodes()
    printUtils.printPyObjAsKV("nodes", nodes)
    queues = server.get_queue_info()
    printUtils.printPyObjAsKV("queues", queues)
    running_builds = server.get_running_builds()
    printUtils.printPyObjAsKV("running_builds", running_builds)

    jenkinsUtils.printJobStatus(server, "FunSpadesDebugBranch")
