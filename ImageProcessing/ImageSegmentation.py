import numpy as np
from skimage import data

import matplotlib.pyplot as plt

coins = data.coins()
print ("image size: ",coins.shape, " max: ", coins.max()," min: ",coins.min() \
       , "image type", np.array(coins).dtype)

(img_height, img_width) = coins.shape
print (coins[10,100])
# coins_arr = np.asarray(coins)
#
# for i in range (img_height):
#     for j in range (img_width):
#         coins_arr[i,j] = 255
mask = coins>0
print (mask)
coins[mask]=254
histo = np.histogram(coins, bins = np.arange(0, 256))
# plt.hist(histo, bins = 256, histtype= 'step', color= 'black')
plt.imshow(coins, cmap = 'gray')
plt.show()
