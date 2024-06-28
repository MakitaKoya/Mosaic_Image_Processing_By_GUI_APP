import cv2
import numpy as np

def main(input_image,num_superpixels):
    height,width,channel = input_image.shape[:3]
    num_iterations = 4
    prior = 2
    double_step = False
    num_levels = 4
    num_histogram_bins = 5
    seeds = cv2.ximgproc.createSuperpixelSEEDS(width, height, channel, num_superpixels,
            num_levels, prior, num_histogram_bins, double_step)

    # 画像のスーパーピクセルセグメンテーションを計算
    # 入力画像は,HSVまたはL*a*b*
    converted = cv2.cvtColor(input_image, cv2.COLOR_BGR2HSV)
    seeds.iterate(converted, num_iterations)

    # スーパーピクセルセグメンテーションの境界を取得
    contour_mask = seeds.getLabelContourMask(False)
    result = input_image.copy()
    result[0 < contour_mask] = ( 0, 255, 255)

    # セグメンテーション数の取得
    nseg = seeds.getNumberOfSuperpixels()

    # セグメンテーション分割情報の取得
    labels = seeds.getLabels()

    # セグメンテーション毎のBGR平均値を取得
    segavgimg = np.zeros((height, width, channel), dtype=np.uint8)
    lb = np.zeros((height, width), dtype=np.uint8)
    for m in range(0, nseg):
        lb.fill(0)
        lb[labels == m] = 255
        bgrm = cv2.mean(input_image, lb) # BGR平均値を取得

        # tuple float形式の平均値情報をint形式に変換
        bgr = [int(bgrm[0]), int(bgrm[1]), int(bgrm[2])]
        segavgimg[lb == 255] = bgr
    
    return segavgimg



if __name__ == "__main__":
    path = '../input/cap-2923682_640.jpg'
    img = cv2.imread(path)
    num_superpixels = 1000
    super_pixel_img = main(img,num_superpixels)

    cv2.imshow('mean',super_pixel_img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    