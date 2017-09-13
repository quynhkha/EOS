import cv2
import numpy as np

is_drawing = False
is_add = True
brush_size = 5
ix, iy = -1, -1
img = cv2.imread('/home/long/PycharmProjects/EOS/ImageProcessing/data/1947-1_plg6.small.png')
img = np.uint8(img)
mask = np.zeros(img[:, :, 0].shape, np.uint8)
mask_red = np.zeros(img.shape, np.uint8)
result_img = np.zeros(img.shape, np.uint8)

# mouse callback
def mouse_tracking(event, x, y, flags, param):
    global ix, iy, is_drawing, is_add, mask, mask_red, result_img

    if event == cv2.EVENT_LBUTTONDOWN:
        is_drawing = True
        ix, iy = x, y

    elif event == cv2.EVENT_MOUSEMOVE:
        if is_drawing == True:
            if is_add == True:
                cv2.circle (mask, (x,y), brush_size, 255, -1)
            elif is_add == False:
                cv2.circle(mask, (x, y), brush_size, 0, -1)
            mask_red[mask == 255] = (0, 0, 255)
            mask_red[mask == 0] = (0, 0, 0)

    elif event == cv2.EVENT_LBUTTONUP:
        is_drawing = False
        if is_add == True:
            cv2.circle(mask, (x, y), brush_size, 255, -1)
        elif is_add == False:
            cv2.circle(mask, (x, y), brush_size, 0, -1)
        mask_red[mask == 255] = (0, 0, 255)
        mask_red[mask == 0] = (0, 0, 0)

    result_img = cv2.addWeighted(img,0.7,mask_red,0.3,0)
cv2.namedWindow('image')
cv2.setMouseCallback('image', mouse_tracking)

while(1):
    cv2.imshow('image', result_img)
    k = cv2.waitKey(1) & 0xFF
    # if k == ord('m'):
    #     mode = not mode

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
    elif k == 27:
        break

cv2.destroyAllWindows()
