from matplotlib import pyplot as plt
import numpy as np
from pyparsing import col


ypoints = [17, 10, 11 , 15] # Price
xpoints = [116, 126, 133, 152] # Areage
#cpoints = ['blue', 'blue' ,'blue', 'blue']
cpoints = ['black', 'red', 'red', 'blue']

for index, it in enumerate(xpoints):
    plt.plot(xpoints[index], ypoints[index], 'o', color = cpoints[index])

plt.xlabel("Areage")
plt.ylabel("Price")
plt.axvline(x=142.5, color = 'red')
plt.axvline(x=124, color = 'black')

# point1 = [12.67, 12.67]
# point2 = [113, 142.5]
# plt.plot(point2, point1, 'green')
# point1 = [15, 15]
# point2 = [142.5, 160]
# plt.plot(point2, point1, 'green')


# point1 = [12.67, 17]
# point2 = [116, 116]
# plt.plot(point2, point1, 'black')

# point1 = [10, 12.67]
# point2 = [126, 126]
# plt.plot(point2, point1, 'black')

# point1 = [11, 12.67]
# point2 = [133, 133]
# plt.plot(point2, point1, 'black')

# point1 = [15, 15]
# point2 = [152, 152]
# plt.plot(point2, point1, 'black')
# plt.figure()

# #residual 
# rypoint = [28.67, 32.5, 14]
# rxpoint = [142.5, 129.5, 121]

# plt.ylabel("Tổng Residual")
# plt.xlabel("Trung bình diện tích")
# plt.plot(rxpoint, rypoint, 'o', color = 'red')
# plt.axhline(y = 14, color = 'green')

plt.show()