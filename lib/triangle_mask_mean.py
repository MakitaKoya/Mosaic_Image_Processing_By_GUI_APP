import cv2
import numpy as np

def triangle_points(side,center_x,center_y,UsD):
    down_side = int(center_y + (np.sqrt(3)*side/2))
    left_side = int(center_x - (side/2))
    right_side = int(center_x + (side/2))

    if UsD:
        return np.array([
            [center_x,center_y],
            [right_side,down_side],
            [left_side,down_side]
        ])
    else:
        return np.array([
            [right_side,center_y],
            [center_x,down_side],
            [left_side,center_y]
        ])
    
def triangle_mean(height,width,side_len,mask_color,img,mask,mean_img):
    x_interval = int(side_len/2)
    y_interval = int(np.sqrt(3)*side_len/2)
    UsD = False
    for j in range(0,height+side_len,y_interval):
        UsD = not UsD
        for i in range(0,width+side_len,x_interval):
            mask.fill(0)
            cv2.fillPoly(mask,[triangle_points(side_len,i,j,UsD)],mask_color)
            bgrm = cv2.mean(img, mask)
            bgr = [int(bgrm[0]), int(bgrm[1]), int(bgrm[2])]
            mean_img[mask == 255] = bgr
            UsD = not UsD
                
    return mean_img
    
def main(img,side_len):
    
    mask_color = (255,255,255)
    
    height, width, channel = img.shape[:3]

    mask = np.zeros((height,width),dtype=np.uint8)
    mean_img = np.zeros((height, width, channel), dtype=np.uint8)

    triangle_mean_img = triangle_mean(height,width,side_len,mask_color,img,mask,mean_img)

    return triangle_mean_img
    

if __name__ == "__main__":
    path = '../input/cap-2923682_640.jpg'
    img = cv2.imread(path)
    side_len = 20
    triangle_mean_img = main(img,side_len)
    cv2.imshow('mean',triangle_mean_img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()