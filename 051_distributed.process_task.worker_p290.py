## !usr/bin/env python3
# -*- coding:utf-8 -*-

import time
import sys
import queue
from multiprocessing.managers import BaseManager

# 分布式进程

# 1.1 服务进程：负责启动Queue，把Queue注册到网络上，然后往Queue里写入任务
print('========1.1========')


#  task worker代码：

# 创建类似的QueueManager
class QueueManager(BaseManager):
    pass


# 由于这个QueueManager只从网络上获取Queue，所以注册时只提供名字
QueueManager.register('get_task_queue')
QueueManager.register('get_result_queue')

# 连接到服务器
server_addr = '155.69.191.250'
print('Connect to server %s...' % server_addr)

# 端口和验证密码保持与task master 的设置完全一致
m = QueueManager(address=(server_addr, 5000), authkey=b'abc')

# 从网络链接
m.connect()

# 获取Queue对象
task = m.get_task_queue()
result = m.get_result_queue()

# 从task队列取任务，并把结果写入result队列中
for i in range(10):
    try:
        n = task.get(timeout=1)
        print('run task %d * %d...' % (n, n))
        r ='%d * %d = %d' % (n, n, n*n)
        time.sleep(1)
        result.put(r)
    except Queue.Empty:
        print('task queue is empty')

print('worker exit.')

# undone
