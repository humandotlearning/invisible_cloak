
import cv2
import numpy as np
import time


# provide name of the output file you want to save
out_name = "output_nimmi.avi"

# creates a videocapture object
cam = cv2.VideoCapture(0)

# create a video write object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(out_name, fourcc, 20.0, (640,480))

# main functionality is given below
bkg = 0
while True:
    ret, im = cam.read()
    
    # checks if frames are being received or not 
    if ret == False:
        continue
        
    # saves a reference background frame
    while bkg <= 3:
        bkg += 1
        bkg_im = im
        continue
        
    # converts to hsv channel as it is easier to threshol color
    im_hsv = cv2.cvtColor(im , cv2.COLOR_BGR2HSV)
    
    # red has 2 values because in the hsv scale it lies in the begining and end of the scale
    # lower red
    lower_color =  np.array([0,120,70])
    upper_color =  np.array([10,255,255])
    mask1 = cv2.inRange(im_hsv, lower_color, upper_color)

    # upper red
    # the H values lies between 0-180 only in hsv
    lower_color =  np.array([170,120,70])
    upper_color =  np.array([180,255,255])
    mask2 = cv2.inRange(im_hsv, lower_color, upper_color)
    mask = mask1+mask2
    
    # fill noise in the mask
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((3,3),np.uint8)) 
    mask_not = cv2.bitwise_not(mask)
    
    # get the intermediate images
    im_hole = cv2.bitwise_and(im, im, mask=mask_not)
    bkg_mask = cv2.bitwise_and(bkg_im, bkg_im ,mask=mask)
    
    # final image
    final_im = cv2.bitwise_or(im_hole, bkg_mask)
    out.write(final_im)


#     cv2.imshow('image', im)
#     cv2.imshow('mask', mask)
#     cv2.imshow('im_hole', im_hole)
#     cv2.imshow('bkg_mask', bkg_mask)
    
    cv2.imshow('final_im', final_im)
    
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

out.release()
cam.release()
cv2.destroyAllWindows()

