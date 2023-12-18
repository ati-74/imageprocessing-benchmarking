import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import cv2
import os
import shutil


def bac_info(bac_in_timestep):
    """
    Extract key information about bacteria from a given dataframe for a specific time step.

    @param bac_in_timestep DataFrame containing bacteria information for a particular time step.

    Returns:
    tuple: A tuple containing four elements:
           - Objects_center_x (Series): The x-coordinates of the centers of the bacteria.
           - Objects_center_y (Series): The y-coordinates of the centers of the bacteria.
           - Objects_major_axis (Series): The lengths of the major axes of the bacteria.
           - Objects_orientation (Series): The orientations of the bacteria.
    """

    # center coordinate
    Objects_center_x = bac_in_timestep["Center_X"]
    Objects_center_y = bac_in_timestep["Center_Y"]

    # major axis length
    Objects_major_axis = bac_in_timestep["Major_axis"]

    # orientation
    Objects_orientation = bac_in_timestep["Orientation"]

    return Objects_center_x, Objects_center_y, Objects_major_axis, Objects_orientation


def find_vertex(center_x, center_y, major, angle_rotation, angle_tolerance=1e-6):
    """
    Calculate the vertices of an ellipse based on its center coordinates, major axis length, and angle of rotation.

    @param center_x float The x-coordinate of the ellipse's center.
    @param center_y float The y-coordinate of the ellipse's center.
    @param major float The length of the major axis of the ellipse.
    @param angle_rotation float The angle of rotation of the ellipse from the horizontal axis in radians.
    @param angle_tolerance float(optional) A small tolerance value used to handle floating-point errors.
    Default is 1e-6.

    Returns:
    list: A list containing two lists, each representing the x and y coordinates of a vertex.

    Note:
    The function checks for two special cases:
    1. When the ellipse is nearly parallel to the vertical axis (angle_rotation ≈ π/2).
    2. When the ellipse is nearly parallel to the horizontal axis (angle_rotation ≈ 0).
    For these cases, the vertices are calculated differently to avoid numerical instability.
    """

    # (x- center_x) * np.sin(angle_rotation) - (y-center_y) * np.cos(angle_rotation) = 0
    # np.power((x - center_x) * np.cos(angle_rotation) + (y - center_y) * np.sin(angle_rotation), 2) =
    # np.power(major, 2)

    # Special case: Ellipse is nearly vertical
    if np.abs(np.abs(angle_rotation) - np.pi / 2) < angle_tolerance:  # Bacteria parallel to the vertical axis
        vertex_1_x = center_x
        vertex_1_y = center_y + major / 2
        vertex_2_x = center_x
        vertex_2_y = center_y - major / 2
    # Special case: Ellipse is nearly horizontal
    elif np.abs(angle_rotation) < angle_tolerance:  # Bacteria parallel to the horizontal axis
        vertex_1_x = center_x + major / 2
        vertex_1_y = center_y
        vertex_2_x = center_x - major / 2
        vertex_2_y = center_y
    else:
        # General case: Ellipse at an arbitrary angle
        semi_major = major
        vertex_1_x = float(semi_major / (np.cos(angle_rotation) + np.tan(angle_rotation) * np.sin(angle_rotation)) +
                           center_x)
        vertex_1_y = float((vertex_1_x - center_x) * np.tan(angle_rotation) + center_y)
        vertex_2_x = float(-semi_major / (np.cos(angle_rotation) + np.tan(angle_rotation) * np.sin(angle_rotation)) +
                           center_x)
        vertex_2_y = float((vertex_2_x - center_x) * np.tan(angle_rotation) + center_y)

    return [[vertex_1_x, vertex_1_y], [vertex_2_x, vertex_2_y]]


def lineage_life_history_plot(df_current, img_dir, TimeStep, axis, clr, prefix_raw_name):
    """
    Plot the lineage life history of cells in a given time step on a background image.

    @param df_current DataFrame containing cell information.
    @param img_dir str Directory path where the background images are stored.
    @param TimeStep int The current time step for which the plot is generated.
    @param axis matplotlib.axes.Axes The matplotlib axis on which to plot.
    @param clr str Color used for plotting the cells.
    @param prefix_raw_name str Prefix for the raw image files.
    """

    # draw Objects
    TimeStep = int(TimeStep)
    ax = axis

    # Adjust image file name format based on the length of TimeStep string
    if len(str(TimeStep - 1)) == 1:
        img_name = prefix_raw_name + "_T0" + str(TimeStep - 1) + ".tif"
    elif len(str(TimeStep)) == 2:
        img_name = prefix_raw_name + "_T" + str(TimeStep - 1) + ".tif"
    elif len(str(TimeStep)) == 3:
        img_name = prefix_raw_name + "_T" + str(TimeStep - 1) + ".tif"

    print(img_dir + img_name)

    # Read and display the background image
    img = cv2.imread(img_dir + img_name)
    plt.imshow(img)
    ax.imshow(img)

    # Extract objects' information from the current time step
    (Objects_center_coord_x, Objects_center_coord_y, Objects_major_current, Objects_orientation_current) = \
        bac_info(df_current)

    # Plot each cell
    num_cells = df_current.shape[0]
    for cell_indx in range(num_cells):
        # Get the current cell's information
        center_current = (Objects_center_coord_x[cell_indx],  Objects_center_coord_y[cell_indx])
        major_current = (Objects_major_current.iloc[cell_indx]) / 2
        # radian
        angle_current = Objects_orientation_current.iloc[cell_indx]

        # Calculate the endpoints of the cell
        ends = find_vertex(center_current[0], center_current[1], major_current, angle_current)
        # endpoints
        node_x1_x_current = ends[0][0]
        node_x1_y_current = ends[0][1]
        node_x2_x_current = ends[1][0]
        node_x2_y_current = ends[1][1]

        # plot current bac
        ax.plot([node_x1_x_current, node_x2_x_current], [node_x1_y_current, node_x2_y_current], lw=1,
                solid_capstyle="round", color=clr)

        # Add cell ID and parent ID as text
        pos1x = np.abs(node_x1_x_current + center_current[0]) / 2
        pos2x = np.abs(node_x2_x_current + center_current[0]) / 2

        pos1y = np.abs(node_x1_y_current + center_current[1]) / 2
        pos2y = np.abs(node_x2_y_current + center_current[1]) / 2

        final_pos1x = np.abs(pos1x + center_current[0]) / 2
        final_pos2x = np.abs(pos2x + center_current[0]) / 2

        final_pos1y = np.abs(pos1y + center_current[1]) / 2
        final_pos2y = np.abs(pos2y + center_current[1]) / 2

        if TimeStep > 32:
            try:
                ax.text(final_pos1x, final_pos1y, int(df_current.iloc[cell_indx]["CellLifeId"]), fontsize=6,
                        color="#ff0000")
            except:
                ax.text(final_pos1x, final_pos1y, int(df_current.iloc[cell_indx]["CellId"]), fontsize=6,
                        color="#ff0000")
            ax.text(final_pos2x, final_pos2y, int(df_current.iloc[cell_indx]["parent"]), fontsize=6,
                    color="#0000ff")
        else:
            try:
                ax.text(final_pos1x, final_pos1y, int(df_current.iloc[cell_indx]["CellLifeId"]), fontsize=6,
                        color="#ff0000")
            except:
                ax.text(final_pos1x, final_pos1y, int(df_current.iloc[cell_indx]["CellId"]), fontsize=6,
                        color="#ff0000")
            ax.text(final_pos2x, final_pos2y, int(df_current.iloc[cell_indx]["parent"]), fontsize=6,
                    color="#0000ff")


def tracking_bac(raw_img, csv_files_path, output_dir, colors, tools, prefix_raw_name_list):
    """
    Generate tracking plots for bacteria over different time steps using data from CSV files.

    @param raw_img list list of directories where the raw images for each dataset are stored.
    @param csv_files_path dict dictionary where keys are dataset names and values are lists of paths to CSV files
                           for each tool used in the dataset.
    @param output_dir list A list of directories where the output plots should be saved for each dataset.
    @param colors list A list of colors used for plotting in each dataset.
    @param tools list A list of tools or methods used for tracking in each dataset.
    @param prefix_raw_name_list list A list of prefixes used in the naming of raw image files for each dataset.
    """

    for index, dataset in enumerate(csv_files_path.keys()):
        print(dataset)
        print(csv_files_path[dataset])
        prefix_raw_name = prefix_raw_name_list[index]
        for i, csv_file in enumerate(csv_files_path[dataset]):
            print(csv_file)
            print(tools[i])
            print(output_dir[index] + '/' + tools[i] + '/tracking_plot/')
            # read csv files
            csv_file = csv_file

            img_dir = raw_img[index]
            # read csv file
            df = pd.read_csv(csv_file)
            df = df.loc[(df["Center_X"].notnull()) & (df["Center_Y"].notnull()) & (df["Major_axis"] != 0)]

            # time steps
            t = list(set(df['TimeStep'].values))
            num_digit = len(str(t[-1]))

            if os.path.exists(output_dir[index] + '/' + tools[i] + '/tracking_plot/'):
                shutil.rmtree(output_dir[index] + '/' + tools[i] + '/tracking_plot/')
            os.makedirs(output_dir[index] + '/' + tools[i] + '/tracking_plot/')

            for timestep in t:

                df_current = df.loc[df["TimeStep"] == timestep]
                df_current = df_current.reset_index(drop=True)

                # plot
                fig, ax = plt.subplots()
                lineage_life_history_plot(df_current, img_dir, timestep, ax, colors[i], prefix_raw_name)

                plt.suptitle("Tracking objects in time step = " + str(timestep), fontsize=14,
                             fontweight="bold")
                parent_patch = mpatches.Patch(color='#0000ff', label='parent', )
                id_patch = mpatches.Patch(color='#ff0000', label='identity id', )
                plt.legend(handles=[parent_patch, id_patch], loc='upper right', ncol=6,
                           bbox_to_anchor=(.75, 1.07), prop={'size': 7})

                # plt.show()
                fig.savefig(output_dir[index] + '/' + tools[i] + '/tracking_plot/' + "timeStep t = " +
                            '0' * (num_digit - len(str(timestep))) + str(timestep) + ".png", dpi=600)
                # close fig
                fig.clf()
                plt.close()


if __name__ == "__main__":
    # dataset : paths
    csv_files_path = {
        'baby_17': [
            "baby17++/CP/results/CP_bacteria_feature_analysis.csv",
            "baby17++/CP_Omnipose/results/CP_Omnipose_bacteria_feature_analysis.csv",
            "baby17++/DeLTA/results/DeLTA_bacteria_feature_analysis.csv",
            "baby17++/FAST/results/FAST_bacteria_feature_analysis.csv",
            "baby17++/SuperSegger/results/SuperSegger_bacteria_feature_analysis.csv",
        ],
    }

    raw_img_dir = [
        'baby17++/raw/',
    ]

    output_dir = [
        "baby17++/",
    ]

    prefix_raw_name = [
        'baby17',
    ]

    colors = ["#FFD700", '#FF7F50', '#40E0D0', '#DAA520', '#32CD32']

    tools = ['CP', 'CP_Omnipose', 'DeLTA', 'FAST', 'SuperSegger']

    # life history based distribution
    tracking_bac(raw_img_dir, csv_files_path, output_dir, colors, tools, prefix_raw_name)
