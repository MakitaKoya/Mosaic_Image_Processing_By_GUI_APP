import cv2
import numpy as np

def main(img,param):
    height, width = img.shape[:2]

    b, g, r = cv2.split(img)
    channels = [b, g, r]
    proc_img_channels = []

    for channel in channels:
        proc_img = np.copy(channel)

        for j in range(0, height, param):
            for i in range(0, width, param):
                h_end = min(j+param, height)
                w_end = min(i+param, width)
                mean = proc_img[j:h_end,i:w_end].mean()
                proc_img[j:h_end,i:w_end].fill(mean)

        proc_img_channels.append(proc_img)

    merged = cv2.merge(proc_img_channels)
    return merged

    

if __name__ == '__main__':
    param = 10
    path = '../input/cap-2923682_640.jpg'
    img = cv2.imread(path)
    merged = main(img,param)
    cv2.imshow('Processed Image', merged)
    cv2.waitKey(0)
    cv2.destroyAllWindows()