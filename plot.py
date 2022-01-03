import matplotlib.pyplot as plt
import numpy as np


with open('data2.txt', 'r') as files:
    data = files.readlines()
l = len(data)
dat = np.zeros(l)

MAX = []
MIN = []
for i in range(l):
    data[i] = data[i].replace('\n', '')
    item = int(data[i])
    dat[i] = item - 8888



datt = dat
d = len(datt)
y = np.zeros(d)
for i in range(d):
    if datt[i] == 1599:
        MAX.append(i)
    if datt[i] < -1610:
        MIN.append(i)
print(MAX)
print(MIN)

begin = []
begin.append(MAX[0])

for i in range(len(MAX)-1):
    if MAX[i+1] - MAX[i] > 1000:
        begin.append(MAX[i+1])

for i in range(len(begin)):
    if begin[i]+2000 < len(datt):
        y[begin[i]: begin[i]+2000] = np.ones(2000)
        print(y)
    else:
        y[begin[i]:] = np.ones(len(datt) - begin[i])

a = len(begin)

with open('./y.txt', 'w') as files:
    for item in y:
        files.write(str(item))
        files.write('\n')

plt.subplot(3, 1, 1)
plt.plot(datt)
plt.title('datas of TENG')
plt.xlabel('dot')
plt.ylabel('V/mv')
plt.subplot(3, 1, 3)
plt.plot(y)
plt.title('arduino')
plt.xlabel('dot')
plt.ylabel('V/mv')
plt.show()