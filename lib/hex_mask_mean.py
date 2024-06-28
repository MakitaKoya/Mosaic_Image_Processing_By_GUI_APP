import cv2
import numpy as np

def hex_points(side,center_x,center_y):
    right_side = int(center_x + (np.sqrt(3)/2)*side)
    left_side = int(center_x - (np.sqrt(3)/2)*side)
    up_side = int(center_y - side)
    down_side = int(center_y + side)
    up_mid = int(center_y - (side/2))
    down_mid = int(center_y + (side/2))
    return np.array([
        [center_x,up_side],
        [right_side,up_mid],
        [right_side,down_mid],
        [center_x,down_side],
        [left_side,down_mid],
        [left_side,up_mid]
    ])

def hex_mean(height,width,side_len,mask_color,img,mask,hex_mean_img):
    x_interval = int(side_len*(np.sqrt(3)/2)*2)
    y_interval = int(side_len*3/2)
    count = 0
    for j in range(0,height+side_len,y_interval):
        start = 0
        if count%2 == 1:
            start = int(x_interval/2)
        count += 1
        for i in range(start,width+side_len,x_interval):
            mask.fill(0)            
            cv2.fillPoly(mask, [hex_points(side_len,i,j)], mask_color)

            bgrm = cv2.mean(img, mask)
            bgr = [int(bgrm[0]), int(bgrm[1]), int(bgrm[2])]
            hex_mean_img[mask == 255] = bgr
            
    return hex_mean_img

def main(img,side_len):
    
    mask_color = (255,255,255)        

    height, width, channel = img.shape[:3]

    mask = np.zeros((height,width),dtype=np.uint8)
    mean_img = np.zeros((height, width, channel), dtype=np.uint8)
    
    hex_mean_img = hex_mean(height,width,side_len,mask_color,img,mask,mean_img)
    return hex_mean_img

if __name__ == "__main__":
    path = '../input/cap-2923682_640.jpg'
    img = cv2.imread(path)
    side_len = 10
    hex_mean_img = main(img,side_len)

    cv2.imshow('mean',hex_mean_img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()