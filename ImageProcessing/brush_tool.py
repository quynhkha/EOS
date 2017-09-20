import cv2
import numpy as np
import copy

class Brushtool:
    def __init__(self):
        self.is_drawing = False
        self.is_add = True
        self.show_brush_region = True
        self.brush_size = 5

        self.img = cv2.imread('/home/long/PycharmProjects/EOS/ImageProcessing/data/1947-1_plg6.small.png')
        ############### Note ##############
        # need to convert img to uint8 to have same type with final mask apply on image (so that cv2.addWeighted can run)
        # need to use np.int8 mask instead of np.uint8 mask for calculation to avoid overflow when value becomes negative
        self.img = np.uint8(self.img)
        self.mask_add = np.zeros(self.img[:, :, 0].shape, np.int8) #int8: -128 ->127
        self.mask_subtract = np.zeros(self.img[:, :, 0].shape, np.int8)
        self.mask_int8 = np.zeros(self.img[:, :, 0].shape, np.int8)
        self.mask = np.zeros(self.img[:, :, 0].shape, np.uint8)

        self.mask_color = np.zeros(self.img.shape, np.uint8)
        self.result_img = np.zeros(self.img.shape, np.uint8)

        self.img_copy = copy.copy(self.img)
        self.simulated_mask = np.zeros(self.img[:, :, 0].shape, np.uint8)
        cv2.rectangle(self.simulated_mask,(200,0),(400,128),255,-1)
        print("here once")

        # io.imshow(simulated_mask)
        # io.show()

# mouse callback
    def mouse_tracking(self, event, x, y, flags, param):
        #global ix, iy, is_drawing, is_add, mask, mask_color, mask_int8, result_img, img_copy

        if event == cv2.EVENT_LBUTTONDOWN:
            self.is_drawing = True
            self.mask_add[self.mask_int8 == 0] = 0
            self.mask_subtract[self.mask_int8 == 0] = 0

        elif event == cv2.EVENT_MOUSEMOVE:
            if self.is_drawing == True:
                if self.is_add == True:
                    # mask_add[mask_int8 == 0] = 0
                    # mask_subtract[mask_int8 == 0] = 0
                    cv2.circle (self.mask_add, (x,y), self.brush_size, 64, -1)
                    self.mask_int8 = self.mask_add - self.mask_subtract  # value -64, 0, 64: subtract, no op, add

                elif self.is_add == False:
                    # mask_add[mask_int8 == 0] = 0
                    # mask_subtract[mask_int8 == 0] = 0
                    cv2.circle(self.mask_subtract, (x, y), self.brush_size, 64, -1)
                    self.mask_int8 = self.mask_add - self.mask_subtract  # value -64, 0, 64: subtract, no op, add

        elif event == cv2.EVENT_LBUTTONUP:
            self.is_drawing = False
            if self.is_add == True:
                # mask_add[mask_int8 == 0] = 0
                # mask_subtract[mask_int8 == 0] = 0
                cv2.circle(self.mask_add, (x, y), self.brush_size, 64, -1)
                self.mask_int8 = self.mask_add - self.mask_subtract  # value -64, 0, 64: subtract, no op, add

            elif self.is_add == False:
                # mask_add[mask_int8 == 0] = 0
                # mask_subtract[mask_int8 == 0] = 0
                cv2.circle(self.mask_subtract, (x, y), self.brush_size, 64, -1)
                self.mask_int8 = self.mask_add - self.mask_subtract  # value -64, 0, 64: subtract, no op, add


        #mask_int8 = np.int8(np.int16(mask_add) - np.int16(mask_subtract))
        #mask_int8 = mask_add - mask_subtract  # value -64, 0, 64: subtract, no op, add
        self.mask_color[self.mask_int8 == 64] = (0, 255, 0)
        self.mask_color[self.mask_int8 == 0] = (0, 0, 0)
        self.mask_color[self.mask_int8 == -64] = (0, 0, 255)

        self.simulated_mask[self.mask_int8==64] = 255
        self.simulated_mask[self.mask_int8==-64] = 0

        self.img_copy = copy.copy(self.img)
        self.img_copy[self.simulated_mask==0] = 0

        #result_img = cv2.addWeighted(img,0.7,mask_color,0.3,0)
        self.result_img = cv2.addWeighted(self.img_copy, 0.7, self.mask_color, 0.3, 0)

        return self.img_copy,self.result_img

    def brush(self):
        cv2.namedWindow('image')
        cv2.setMouseCallback('image', self.mouse_tracking)


        while(1):
            if self.show_brush_region:
                cv2.imshow('image', self.result_img)
            else:
                cv2.imshow('image', self.img_copy)
            k = cv2.waitKey(1) & 0xFF
            if k == ord('m'):
                self.show_brush_region = not self.show_brush_region
                if (self.show_brush_region == True):
                    print ("'m' is pressed. Show brush masked region")
                else:
                    print ("'m' is pressed. Hide brush masked region")

            if k == ord('['):
                if self.brush_size >1:
                    self.brush_size += -1
                    print("'[' is pressed. Brush size decreased to ", self.brush_size)
                else:
                    print ("'[' is pressed. Brush size cannot be smaller")
            elif k == ord(']'):
                self.brush_size += 1
                print("']' is pressed. Brush size increased to ", self.brush_size)
            elif k == ord ('t'):
                self.is_add = not self.is_add
                if self.is_add == True:
                    print("'t' is pressed. Toggle add mode")
                else:
                    print("'t' is pressed. Toggle subtract mode")

            elif k == 27: # ESC key pressed
                break

        cv2.destroyAllWindows()

if __name__ == "__main__":
    brushtool = Brushtool()
    brushtool.brush()
