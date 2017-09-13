import cv2
import numpy as np

import copy

is_drawing = False
is_add = True
show_brush_region = True
brush_size = 5
ix, iy = -1, -1
img = cv2.imread('/home/long/PycharmProjects/EOS/ImageProcessing/data/1947-1_plg6.small.png')
############### Note ##############
# need to convert img to uint8 to have same type with final mask apply on image (so that cv2.addWeighted can run)
# need to use np.int8 mask instead of np.uint8 mask for calculation to avoid overflow when value becomes negative
img = np.uint8(img)
mask_add = np.zeros(img[:, :, 0].shape, np.int8) #int8: -128 ->127
mask_subtract = np.zeros(img[:, :, 0].shape, np.int8)
mask_int8 = np.zeros(img[:, :, 0].shape, np.int8)
mask = np.zeros(img[:, :, 0].shape, np.uint8)

mask_color = np.zeros(img.shape, np.uint8)
result_img = np.zeros(img.shape, np.uint8)

img_copy = copy.copy(img)
simulated_mask = np.zeros(img[:, :, 0].shape, np.uint8)
cv2.rectangle(simulated_mask,(200,0),(400,128),255,-1)
print("here once")

# io.imshow(simulated_mask)
# io.show()

# mouse callback
def mouse_tracking(event, x, y, flags, param):
    global ix, iy, is_drawing, is_add, mask, mask_color, mask_int8, result_img, img_copy

    if event == cv2.EVENT_LBUTTONDOWN:
        is_drawing = True
        ix, iy = x, y
        mask_add[mask_int8 == 0] = 0
        mask_subtract[mask_int8 == 0] = 0

    elif event == cv2.EVENT_MOUSEMOVE:
        if is_drawing == True:
            if is_add == True:
                # mask_add[mask_int8 == 0] = 0
                # mask_subtract[mask_int8 == 0] = 0
                cv2.circle (mask_add, (x,y), brush_size, 64, -1)
                mask_int8 = mask_add - mask_subtract  # value -64, 0, 64: subtract, no op, add

            elif is_add == False:
                # mask_add[mask_int8 == 0] = 0
                # mask_subtract[mask_int8 == 0] = 0
                cv2.circle(mask_subtract, (x, y), brush_size, 64, -1)
                mask_int8 = mask_add - mask_subtract  # value -64, 0, 64: subtract, no op, add

    elif event == cv2.EVENT_LBUTTONUP:
        is_drawing = False
        if is_add == True:
            # mask_add[mask_int8 == 0] = 0
            # mask_subtract[mask_int8 == 0] = 0
            cv2.circle(mask_add, (x, y), brush_size, 64, -1)
            mask_int8 = mask_add - mask_subtract  # value -64, 0, 64: subtract, no op, add

        elif is_add == False:
            # mask_add[mask_int8 == 0] = 0
            # mask_subtract[mask_int8 == 0] = 0
            cv2.circle(mask_subtract, (x, y), brush_size, 64, -1)
            mask_int8 = mask_add - mask_subtract  # value -64, 0, 64: subtract, no op, add


    #mask_int8 = np.int8(np.int16(mask_add) - np.int16(mask_subtract))
    #mask_int8 = mask_add - mask_subtract  # value -64, 0, 64: subtract, no op, add
    mask_color[mask_int8 == 64] = (0, 255, 0)
    mask_color[mask_int8 == 0] = (0, 0, 0)
    mask_color[mask_int8 == -64] = (0, 0, 255)

    simulated_mask[mask_int8==64] = 255
    simulated_mask[mask_int8==-64] = 0

    img_copy = copy.copy(img)
    img_copy[simulated_mask==0] = 0

    #result_img = cv2.addWeighted(img,0.7,mask_color,0.3,0)
    result_img = cv2.addWeighted(img_copy, 0.7, mask_color, 0.3, 0)
cv2.namedWindow('image')
cv2.setMouseCallback('image', mouse_tracking)


while(1):
    if show_brush_region:
        cv2.imshow('image', result_img)
    else:
        cv2.imshow('image', img_copy)
    k = cv2.waitKey(1) & 0xFF
    if k == ord('m'):
        show_brush_region = not show_brush_region

    if k == ord('['):
        if brush_size >1:
            brush_size += -1
            print('brush size', brush_size)
        else:
            print ('brush size cannot be smaller')
    elif k == ord(']'):
        brush_size += 1
        print('brush size', brush_size)
    elif k == ord ('t'):
        is_add = not is_add
        print('is_add', is_add)
    elif k == 27: # ESC key pressed
        break

cv2.destroyAllWindows()
