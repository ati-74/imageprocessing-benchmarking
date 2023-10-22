import numpy as np
import pandas as pd
import cv2
import os


def coords_to_mask(coords, shape):
    """
    Converts given coordinates to a binary mask of specified shape.

    @param coords list of lists A list containing two lists - the x and y coordinates.
    @param shape tuple The desired shape of the mask, given as (height, width).

    Returns:
    mask np.array A binary mask of given shape where specified coordinates are set to 255.
    """

    mask = np.zeros(shape, dtype=np.uint8)
    mask[coords[1], coords[0]] = 255
    return mask


def find_objects(values_dict, max_y, max_x):
    """
    Finds and processes objects based on their coordinates and saves the resulting mask image.

    @param values_dict dict Dictionary containing object details like interval and label coordinates.
    @param max_y int Maximum y-coordinate.
    @param max_x int Maximum x-coordinate.
    """

    # Extracting time steps from values_dict
    time_steps_list = range(1, int(values_dict['interval'].split('],')[1].split(',')[-1]) + 2)

    for time_step in [time_steps_list[-1]]:
        print('time step:' + str(time_step))

        # Initializing lists to store coordinates for the current time step
        x_coords_time_step, y_coords_time_step = [], []

        # Iterating over each label in the dictionary
        for label, coords_str in values_dict['labels'].items():
            x_coords, y_coords = [], []

            # Parsing the coordinate strings for each label
            for coord_str in coords_str.split(']'):
                coord_str = coord_str.replace('[', '').strip()
                if coord_str:
                    x, y, t = map(int, [v for v in coord_str.split(',') if v != ''])
                    # Checking if time matches with the current time step
                    if t == time_step - 1:
                        x_coords.append(x)
                        y_coords.append(y)

            # Filtering objects based on specified conditions
            if len(x_coords) > 4 and 0 not in x_coords and max_x not in x_coords and 0 not in y_coords and \
                    max_y not in y_coords:
                x_coords_time_step.extend(x_coords)
                y_coords_time_step.extend(y_coords)

        # Generate mask for the individual object
        current_mask = coords_to_mask([x_coords_time_step, y_coords_time_step], shape=(max_y + 1, max_x + 1))

        # save the mask
        # Assumes existence of a variable 'label_file' and 'num_digit' elsewhere in your code
        cv2.imwrite(os.path.dirname(label_file) + "/objects/baby_bw_" +
                    '0' * (num_digit - len(str(time_step))) + str(time_step) + ".tif", current_mask)


if __name__ == '__main__':
    # The path to the label file containing object information.
    label_file = 'EcoliK12.T000.labeling'

    # Open the label file and read its content.
    with open(label_file, 'r') as file:
        content = file.read()

    # List of expected keys in the content.
    keys = ['interval', 'pixelSizes', 'labels', 'colors']

    # Extracting the 'interval' and 'pixelSizes' information from the content.
    values_dict = {
        'interval': content.split('interval')[1].split('pixelSizes')[0].replace('"', '').replace('{', '').replace('}',
                                                                                                                  '')[
                    1:-1],
        'pixelSizes': content.split('pixelSizes')[1].split('labels')[0].replace('"', '').replace('[', '').replace(']',
                                                                                                                  '')[
                      1:-1]
    }

    # Extracting the labels and their corresponding coordinates.
    coordinates = content.split('labels')[1].split('colors')[0][3:-3]
    labels_coordinate_dict = {}
    for val in coordinates.split('"'):
        if val != '':
            if val.count('Label') > 0:
                current_label = val
            else:
                labels_coordinate_dict[current_label] = val[2:-2]

    values_dict['labels'] = labels_coordinate_dict

    # Parsing the minimum and maximum coordinates, and the time steps from the 'interval' information.
    min_x, min_y, first_time_step = [int(v) for v in
                                     values_dict['interval'].split('min:')[1].split(',max')[0].replace(']', '').replace(
                                         '[', '').split(',')]
    max_x, max_y, last_time_step = [int(v) for v in
                                    values_dict['interval'].split('max:')[1].split(',n')[0].replace(']', '').replace(
                                        '[', '').split(',')]

    # Getting the list of time steps.
    max_time_step = int(values_dict['interval'].split('],')[1].split(',')[-1]) + 1
    time_steps_list = [i for i in range(1, max_time_step + 1)]

    # Calculate the number of digits in the largest time step for file naming.
    num_digit = len(str(time_steps_list[-1]))

    # Call the find_objects function to process the objects and save masks.
    find_objects(values_dict, max_y, max_x)
