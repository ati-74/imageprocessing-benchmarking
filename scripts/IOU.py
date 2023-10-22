import os
import cv2
import glob
import numpy as np

import pandas as pd

if __name__ == '__main__':

    output_dir = 'baby20/'
    ground_truth_dir = output_dir + 'reference-mask/objects/'
    cp_output_dir = output_dir + 'CP/objects/'
    cp_omnipose_output_dir = output_dir + 'CP_Omnipose/objects/'
    fast_output_dir = output_dir + 'FAST/Segmentations/'
    ss_output_dir = output_dir + 'SuperSegger/xy1/BWObjects'
    delta_output_dir = output_dir + 'DeLTA/input/delta_results/segmentation/BW'

    ground_truth_imgs = sorted(glob.glob(ground_truth_dir + '/*.tif'))
    cp_output_imgs = sorted(glob.glob(cp_output_dir + '/*.tiff'))
    cp_omnipose_output_imgs = sorted(glob.glob(cp_omnipose_output_dir + '/*.tiff'))
    fast_output_imgs = sorted(glob.glob(fast_output_dir + '/*.tif'))
    ss_output_imgs = sorted(glob.glob(ss_output_dir + '/*.tif'))
    delta_output_imgs = sorted(glob.glob(delta_output_dir + '/*.tif'))

    images = [cp_output_imgs, cp_omnipose_output_imgs, fast_output_imgs, ss_output_imgs, delta_output_imgs]
    iou_results = []
    time_step = []

    for j, img_list in enumerate(images):
        iou_val_list = []
        for i in range(len(img_list)):

            ground_truth_img = cv2.imread(ground_truth_imgs[i], cv2.IMREAD_GRAYSCALE)
            ground_truth_height, ground_truth_width = ground_truth_img.shape[:2]

            pr_output_img = cv2.imread(img_list[i], cv2.IMREAD_GRAYSCALE)
            pr_height, pr_width = pr_output_img.shape[:2]

            if pr_height != ground_truth_height or pr_width != ground_truth_width:
                # it's for FAST
                print('warning' + str(img_list[i]))
                # resize the image
                pr_output_img = cv2.resize(pr_output_img, (ground_truth_width, ground_truth_height))

            # Apply a bitwise AND operation to find the intersection
            intersection = cv2.bitwise_and(ground_truth_img, pr_output_img)
            union = cv2.bitwise_or(ground_truth_img, pr_output_img)

            # Find the area of the intersection by counting the number of white pixels
            area_intersection = np.count_nonzero(intersection)

            area_union = np.count_nonzero(union)

            # print(round(area_intersection / area_union, 4))
            iou_val_list.append(round(area_intersection / area_union, 4))
            if j == 0:
                time_step.append(int(os.path.basename(cp_output_imgs[i]).split('.')[0].split('_T')[1]) + 1)

        iou_results.append(iou_val_list)

    df = pd.DataFrame({'time step': time_step , 'CellProfiler': iou_results[0], 'CellProfiler_Omnipose': iou_results[1],
                       'FAST': iou_results[2], 'SuperSegger': iou_results[3], 'DeLTA': iou_results[4]})
    df['time step'] = df['time step'].astype(float)
    df = df.sort_values('time step')
    df.to_csv(output_dir + '/' + output_dir.split('/')[1] + '_IOU.csv', index=False)

