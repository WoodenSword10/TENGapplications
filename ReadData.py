# import serial
#
# data = []
# my_port = serial.Serial('COM9', 9600)
# for i in range(1000):
#     dat = str(my_port.readline())
#     dat = dat[2:-5]
#     print(dat)
#     data.append(dat)
#
# with open('data2.txt', 'wb') as f:
#     for item in data:
#         datt = item
#         f.write(datt.encode())
#         f.write(b'\n')

# import numpy as np
# import matplotlib.pyplot as plt
# with open('data2.txt', 'r') as f:
#     data = f.readlines()
#
# for i in range(len(data)):
#     data[i] = int(str(data[i])[:-1])-8889
#
# data = data[110:303]
#
# MAX = []
# MIN = []
# i = 0
# for item in data:
#     if item > 8590:
#         MAX.append(i)
#     elif item < -8600:
#         MIN.append(i)
#     i += 1
#
# print('MAX=', MAX)
# print('MIN=', MIN)
#
# begin = []
# begin.append(MAX[0])
# end = []
# end.append(MIN[0])
#
# for i in range(len(MAX)-1):
#     if MAX[i+1] - MAX[i] > 20:
#         begin.append(MAX[i+1])
#
# for i in range(len(MIN)-1):
#     if MIN[i+1] - MIN[i] > 20:
#         end.append(MIN[i+1])
#
# print('begin=', begin)
# print('end=', end)
# a = len(begin)
# final = np.zeros(len(data))
# for i in range(a):
#     final[end[i]: begin[i]] = 1
#
# plt.subplot(3, 1, 1)
# plt.plot(data)
# plt.title('datas of TENG')
# plt.xlabel('dot')
# plt.ylabel('V/mv')
# plt.subplot(3, 1, 3)
# plt.plot(final)
# plt.title('arduino')
# plt.xlabel('dot')
# plt.ylabel('isHigh')
# plt.show()
import time

old_time = time.time()
time.sleep(2)
now_time = time.time()
print(now_time-old_time)