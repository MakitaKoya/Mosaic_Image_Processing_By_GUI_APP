import cv2

def main(img,serect_b,serect_g,serect_r):
    b_src, g_src, r_src = cv2.split(img)

    if serect_b:
        b_mean = b_src.mean()
        b_src.fill(b_mean)
    if serect_g:
        g_mean = g_src.mean()
        g_src.fill(g_mean)
    if serect_r:
        r_mean = r_src.mean()
        r_src.fill(r_mean)
        
    merged = cv2.merge((b_src, g_src, r_src))
    return merged

    

if __name__ == '__main__':
    serect_b = True
    serect_g = False
    serect_r = False

    path = '../input/cap-2923682_640.jpg'
    img = cv2.imread(path)
    merged = main(img,serect_b,serect_g,serect_r)
    cv2.imshow('origin',img)
    cv2.imshow('marged',merged)
    cv2.waitKey(0)
    cv2.destroyAllWindows