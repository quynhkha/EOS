import numpy as np
import matplotlib.pyplot as plt
import os
from skimage import io
from skimage.feature import match_template
from skimage import data
import copy

data_dir = '/home/long/PycharmProjects/EOS/ImageProcessing/data/'
code_dir = '/home/long/PycharmProjects/EOS/ImageProcessing/'
filename = os.path.join(data_dir, '1947-1_plg6.small.png')

image = io.imread(filename)
coin = data.coins()
im = image[:, :, 0]
io.imshow(im)
io.show()
rock_sample = im[220:240, 310:330]

result = match_template(im, rock_sample)
print (result, result.shape)

(width, height) = result.shape
result_copy = np.zeros(result.shape)
for xi in range(width):
    for yi in range(height):
        if result[xi,yi] > 0.005:
            result_copy[xi,yi] = 255
ij = np.unravel_index(np.argmax(result), result.shape)
x, y  = ij[::-1]

fig = plt.figure(figsize=(8, 3))
ax1 = plt.subplot(1, 3, 1)
ax2 = plt.subplot(1, 3, 2, adjustable='box-forced')
ax3 = plt.subplot(1, 3, 3, sharex=ax2, sharey=ax2, adjustable='box-forced')

ax1.imshow(rock_sample, cmap=plt.cm.gray)
ax1.set_axis_off()
ax1.set_title('template')

ax2.imshow(im, cmap=plt.cm.gray)
ax2.set_axis_off()
ax2.set_title('image')
# highlight matched region
hsample, wsample = rock_sample.shape
rect = plt.Rectangle((x, y), wsample, hsample, edgecolor='r', facecolor='none')
ax2.add_patch(rect)

ax3.imshow(result_copy, cmap = plt.cm.gray)
ax3.set_axis_off()
ax3.set_title('`match_template`\nresult')
# highlight matched region
ax3.autoscale(False)
ax3.plot(x, y, 'o', markeredgecolor='r', markerfacecolor='none', markersize=10)

plt.show()