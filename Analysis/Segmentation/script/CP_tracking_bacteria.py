import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.patheffects as mpe
import matplotlib.patches as mpatches
import cv2


def plot(df_current,img_dir,TimeStep,Tool,dataset,mode_title):
 
    fig, ax = plt.subplots()
    # draw Objects
    ax = plt.gca()

    if len(str(TimeStep)) ==1:
        img_name = "pos1cha1fra00"+str(TimeStep)+".tif"
    elif len(str(TimeStep)) ==2:
        img_name = "pos1cha1fra0"+str(TimeStep)+".tif"
    elif len(str(TimeStep)) ==3:
        img_name = "pos1cha1fra"+str(TimeStep)+".tif"

    img = cv2.imread(img_dir+img_name)
    ax.imshow(img)

  
    # Objects information in current time atep
    (
      Objects_center_coord_current,
      Objects_major_current,
      Objects_minor_current,
      Objects_orientation_current,
    ) = bac_info(df_current)    

    # number of cells in current time step
    num_cells = df_current.shape[0]
    for cell_indx in range(num_cells):
        #current bac
        center_current = (
                Objects_center_coord_current.iloc[cell_indx]["Center_X"],
                Objects_center_coord_current.iloc[cell_indx]["Center_Y"],
            )
        minor_current = Objects_minor_current.iloc[cell_indx] / 2
        major_current = Objects_major_current.iloc[cell_indx] / 2
        # radian
        angle_current = -(Objects_orientation_current.iloc[cell_indx]+90) * np.pi / 180
        # endpoints
        Node_x1_x_current = center_current[0] + major_current * np.cos(angle_current)
        Node_x1_y_current = center_current[1] + major_current * np.sin(angle_current)
        Node_x2_x_current = center_current[0] - major_current * np.cos(angle_current)
        Node_x2_y_current = center_current[1] - major_current * np.sin(angle_current)      

        #plot current bac
        plt.plot(
                    [Node_x1_x_current, Node_x2_x_current],
                    [Node_x1_y_current, Node_x2_y_current],
                    lw=1,
                    solid_capstyle="round",
                    color = "yellow"
        )
        #adding text inside the plot
        #plt.text(center_current[0], center_current[1],int(df_current.iloc[cell_indx]["lable"]) , fontsize = 4 , color = "red")       
        

    plt.suptitle("Tracking Objects in TimeStep "+ str(TimeStep), fontsize=14, fontweight="bold")
    ax.set_ylim(max(img.shape[0],Objects_center_coord_current["Center_Y"].max()),0)
    ax.set_xlim(0,max(Objects_center_coord_current["Center_X"].max(),img.shape[1]))
    #plt.show()
    fig.savefig(
         "../img/"+dataset+"/"+mode_title+"/"+Tool[0]+"/" +"/"+ "Objects in TimeStep "+ str(TimeStep)+ "_" + dataset + " ("+mode_title+").png",
        dpi=600,
    )
    # close fig
    fig.clf()
    plt.close()

        

def bac_info(bac_in_timestep):    
    # center coordinate
    Objects_center_coord = bac_in_timestep[
        ["Center_X", "Center_Y"]
    ]
    # major axis length
    Objects_major_axis = bac_in_timestep["Major_axis"]
    # minor axis length
    Objects_minor_axis = bac_in_timestep["Minor_axis"]
    # orientation
    Objects_orientation = bac_in_timestep["Orientation"]

    return Objects_center_coord, Objects_major_axis, Objects_minor_axis, Objects_orientation

def tracking_bac(end_of_file_name,Tools_name,datasets,main_directories,
                 plot_titles,modes,modes_title):

    for dataset in datasets:
        for mode in modes:
        # read csv files
            CP_csv_file = (
                    main_directories["CP_directory"]
                    + dataset
                    + "/"+mode+"/post-processing/results/"
                    + Tools_name[0]
                    + "_"
                    + end_of_file_name
                    + ".csv"
                )
            img_dir = "../../../DeLTA/" + dataset+ "/"+"1. Raw images"+"/1. Input images/"
            # read csv file
            df_cp = pd.read_csv(CP_csv_file)      

            # time steps
            t = list(set(df_cp['TimeStep'].values))
            for i in range(len(t)):
                df_current = df_cp.loc[df_cp["TimeStep"] == t[i]]
                # plot
                Tool = ["CellProfiler"]
                plot(df_current,img_dir,t[i],Tool,dataset,modes_title[mode])


if __name__ == "__main__":

    # main directory of each image processing tools
    main_directories = {
        "CP_directory": "../../../CellProfiler/",
    }

    # datasets
    #        "Pseudomonas_agarose",
    #    "SuperSegger sample images set",
    #    "Xanthomonase_agarose",
    datasets = [
        "E.coli_mono_agarose"

    ]
    #"2. Ilastik Output"
    # "1. Raw images"
    modes = ["1. Raw images","2. Ilastik Output"]
    # "1. Raw images":"Without Ilastik"
    #"2. Ilastik Output":"With Ilastik"
    modes_title = { "1. Raw images":"Without Ilastik","2. Ilastik Output":"With Ilastik"}

    # titles
    plot_titles = ["Objects"]

    # end of file names
    end_of_file_name = "bacteria_feature_analysis"

    Tools_name = ["CellProfiler"]

    # life history based distribution
    tracking_bac(
        end_of_file_name,
        Tools_name,
        datasets,
        main_directories,
        plot_titles,
        modes,
        modes_title
    )


