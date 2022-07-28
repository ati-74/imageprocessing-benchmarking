import sys

sys.path.append("scripts\lowner-john-ellipse\src")
from lownerJohnEllipse import welzl, plot_ellipse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import pandas as pd


def aspect_plot(bac_df, ellipses, TimeStep, output_directory):
    """
    Goal: this function plots the whole story! that means it shows bacteria with
    both end points and ellipse that are fitted to colonies' boundaries and reports
    their aspect ratio as a single number in the middle of the colony.
    
    @param bac_df     data frame   bacterial info like x,y center and orientation, etc.
    @param ellipses   list         ellipses' parameters that are fitted to micro-colonies
    """    

    fig, ax = plt.subplots()
    # bacteria information
    (
        bacteria_center_coord,
        bacteria_major,
        bacteria_minor,
        bacteria_orientation,
    ) = bac_info(bac_df)
    # number of cells
    num_cells = bac_df.shape[0]
    # draw bacteria
    ax = plt.gca()
    for cell_indx in range(num_cells):
        center = (
            bacteria_center_coord.iloc[cell_indx]["AreaShape_Center_X"],
            bacteria_center_coord.iloc[cell_indx]["AreaShape_Center_Y"],
        )
        minor = bacteria_minor.iloc[cell_indx] / 2
        major = bacteria_major.iloc[cell_indx] / 2
        # radian
        angle = -(bacteria_orientation.iloc[cell_indx] + 90) * np.pi / 180
        # endpoints
        Node_x1_x = center[0] + major * np.cos(angle)
        Node_x1_y = center[1] + major * np.sin(angle)
        Node_x2_x = center[0] - major * np.cos(angle)
        Node_x2_y = center[1] - major * np.sin(angle)
        plt.plot(
            [Node_x1_x, Node_x2_x],
            [Node_x1_y, Node_x2_y],
            lw=minor,
            solid_capstyle="round",
        )

    # ellipses
    for ellipse_params in ellipses:
        plot_ellipse(ellipse_params, str="k--")
        # ellipse: a tuple (c, a, b, t), where c = (x, y) is the center, a and
        # b are the major and minor radii, and t is the rotation angle.
        center_pos, major, minor, theta = ellipse_params
        aspect_ratio = round(minor / major, 2)
        # Adding text inside a rectangular box by using the keyword 'bbox'
        plt.text(center_pos[0], center_pos[1], aspect_ratio, color="red")
    plt.title("Aspect ratio for each microcolonies at timestep " + str(TimeStep))
    ax.set_ylim(ax.get_ylim()[::-1])
    # plt.show()
    fig.savefig(
        output_directory + "/img/Aspect Ratio/aspect_ratio_t" + str(TimeStep) + ".png",
        dpi=300,
    )
    # close fig
    fig.clf()
    plt.close()


def fit_enclosing_ellipse(points):
    # convert dataframe to numpy array
    points = points.to_numpy()
    # print(points)
    # finds the smallest ellipse covering a finite set of points
    # https://github.com/dorshaviv/lowner-john-ellipse
    enclosing_ellipse = welzl(points)
    return enclosing_ellipse


def bac_info(bac_in_microcolony):
    """
    Goal: this fuction returns important features of bacteria in the each micro-colony that we
    study (ex: orientation, minor/major axis length, etc.). we need this data for calculating endpoints for fitting ellipse and plotting bacteria.
    
    @param bac_in_microcolony     data frame   information(orinetation, major/minor axis length, etc.) about each bacteria in each micro-colony in current time-step.
    """     
    # center coordinate
    bacteria_center_coord = bac_in_microcolony[
        ["AreaShape_Center_X", "AreaShape_Center_Y"]
    ]
    # major axis length
    bacteria_major_axis = bac_in_microcolony["AreaShape_MajorAxisLength"]
    # minor axis length
    bacteria_minor_axis = bac_in_microcolony["AreaShape_MinorAxisLength"]
    # orientation
    bacteria_orientation = bac_in_microcolony["AreaShape_Orientation"]

    return bacteria_center_coord, bacteria_major_axis, bacteria_minor_axis, bacteria_orientation


def aspect_ratio_calc(bac_in_microcolony):
    # bacteria info
    (
        bacteria_center_coord,
        bacteria_major,
        bacteria_minor,
        bacteria_orientation,
    ) = bac_info(bac_in_microcolony)
    bac_angle = -(bacteria_orientation + 90) * np.pi / 180
    # endpoints
    endpoint1_x = bacteria_center_coord["AreaShape_Center_X"] + (
        bacteria_major / 2
    ) * np.cos(bac_angle)
    endpoint1_y = bacteria_center_coord["AreaShape_Center_Y"] + (
        bacteria_major / 2
    ) * np.sin(bac_angle)
    endpoint2_x = bacteria_center_coord["AreaShape_Center_X"] - (
        bacteria_major / 2
    ) * np.cos(bac_angle)
    endpoint2_y = bacteria_center_coord["AreaShape_Center_Y"] - (
        bacteria_major / 2
    ) * np.sin(bac_angle)
    endpoint1 = pd.concat([endpoint1_x, endpoint1_y], axis=1)
    endpoint2 = pd.concat([endpoint2_x, endpoint2_y], axis=1)
    endpoints = pd.concat([endpoint1, endpoint2], axis=0)
    # fit ellipse
    ellipse_params = fit_enclosing_ellipse(endpoints)
    # calculate aspect ratio
    center_pos, major, minor, theta = ellipse_params
    aspect_ratio = round(minor / major, 2)

    return ellipse_params, aspect_ratio
