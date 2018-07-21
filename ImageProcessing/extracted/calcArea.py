import os
import cv2
import numpy as np 
import matplotlib.pyplot as plt 

# scale is (true distance / pixel)
scale = 1e-3
threshold = 200
areas = np.zeros(21)

for i in range(1, 22):
	img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "{}.tif".format(i))
	gray = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
	areas[i-1] = scale * len(np.where(gray < threshold)[0])
	
print(areas)
plt.hist(areas, bins=np.arange(min(areas), max(areas) + 1, 1), histtype='bar', rwidth=0.5)
plt.ylabel('No of crystal')
plt.xlabel('Area')
plt.xticks(np.arange(int(min(areas)), int(max(areas)) + 2, 1)) 
plt.show()

