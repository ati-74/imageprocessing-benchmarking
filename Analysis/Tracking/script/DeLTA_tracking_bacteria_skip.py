import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.patheffects as mpe
import matplotlib.patches as mpatches
import cv2



def plot_without_skip(df_current,img_dir,TimeStep,Tool,dataset,mode_title,axis):
 
    # draw Objects
    ax = axis

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
        if df_current.iloc[cell_indx]["width"] > df_current.iloc[cell_indx]["height"] :
            angle_current = (Objects_orientation_current.iloc[cell_indx]) * np.pi / 180
        else:
            angle_current = (Objects_orientation_current.iloc[cell_indx]+90) * np.pi / 180 
        # endpoints
        Node_x1_x_current = center_current[0] + major_current * np.cos(angle_current)
        Node_x1_y_current = center_current[1] + major_current * np.sin(angle_current)
        Node_x2_x_current = center_current[0] - major_current * np.cos(angle_current)
        Node_x2_y_current = center_current[1] - major_current * np.sin(angle_current)      

        #plot current bac
        ax.plot(
                    [Node_x1_x_current, Node_x2_x_current],
                    [Node_x1_y_current, Node_x2_y_current],
                    lw=1,
                    solid_capstyle="round",
                    color = "#FF7F00"
        )
        #adding text inside the plot
        # original 
        # x , y -> 833
        if Node_x1_y_current>=278.5 and Node_x1_y_current <= 485.5 and Node_x2_y_current>=278.5 and Node_x2_y_current <= 455.5:
            ax.text(center_current[0], center_current[1],int(df_current.iloc[cell_indx]["lable"]) , fontsize = 4 , color = "blue")       

    ax.set_title("Without Skip", fontsize=10, fontweight="bold")
    ax.set_ylim(485.5,278.5)
    ax.set_xlim(0,max(Objects_center_coord_current["Center_X"].max(),img.shape[1]))




def plot(df_current,img_dir,TimeStep,Tool,dataset,mode_title,axis):

    TimeStep = ((TimeStep-1)*10)+1
    # draw Objects
    ax = axis

    if len(str(TimeStep)) ==1:
        img_name = "pos1cha1fra00"+str(TimeStep)+".tif"
    elif len(str(TimeStep)) ==2:
        img_name = "pos1cha1fra0"+str(TimeStep)+".tif"
    elif len(str(TimeStep)) ==3:
        img_name = "pos1cha1fra"+str(TimeStep)+".tif"

    img = cv2.imread(img_dir+img_name)
    crop_img = img[0:180, 0:177]
    ax.imshow(crop_img)

  
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
        # radian
        if df_current.iloc[cell_indx]["width"] > df_current.iloc[cell_indx]["height"] :
            angle_current = (Objects_orientation_current.iloc[cell_indx]) * np.pi / 180
        else:
            angle_current = (Objects_orientation_current.iloc[cell_indx]+90) * np.pi / 180 
        # endpoints
        Node_x1_x_current = center_current[0] + major_current * np.cos(angle_current)
        Node_x1_y_current = center_current[1] + major_current * np.sin(angle_current)
        Node_x2_x_current = center_current[0] - major_current * np.cos(angle_current)
        Node_x2_y_current = center_current[1] - major_current * np.sin(angle_current)      

        #plot current bac
        if Node_x1_y_current <= 180 and Node_x2_y_current <= 180 and Node_x1_x_current <= 177 and Node_x2_x_current <= 177:
            ax.plot(
                        [Node_x1_x_current, Node_x2_x_current],
                        [Node_x1_y_current, Node_x2_y_current],
                        lw=1,
                        solid_capstyle="round",
                        color = "#FF7F00"
            )
            #adding text inside the plot
            ax.text(center_current[0], center_current[1],int(df_current.iloc[cell_indx]["lable"]) , fontsize = 4 , color = "blue")        
        
    ax.set_title("With Skip", fontsize=10, fontweight="bold")
    ax.set_ylim(max(crop_img.shape[0],180),0)
    ax.set_xlim(0,max(177,crop_img.shape[1]))
    #ax.set_ylim(max(crop_img.shape[0],Objects_center_coord_current["Center_Y"].max()),0)
    #ax.set_xlim(0,max(Objects_center_coord_current["Center_X"].max(),crop_img.shape[1]))
        

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


def tracking_bac(end_of_file_name,Tools_name,datasets1,datasets2,main_directories,
                 plot_titles,modes,modes_title):

    for dataset in datasets1:
        for mode in modes:
        # read csv files
            DeLTA_csv_file = (
                    main_directories["DeLTA_directory"]
                    + dataset
                    + "/"+mode+"/post-processing/results/"
                    + Tools_name[0]
                    + "_"
                    + end_of_file_name
                    + ".csv"
                )

            DeLTA_csv_file_without_skip = (
                    main_directories["DeLTA_directory"]
                    + datasets2[datasets1.index(dataset)]
                    + "/"+mode+"/post-processing/results/"
                    + Tools_name[0]
                    + "_"
                    + end_of_file_name
                    + ".csv"
                )
            
            img_dir = "../../../DeLTA/" + dataset+ "/"+"1. Raw images"+"/1. Input images/"
            img_dir_without_skip = "../../../DeLTA/" + datasets2[datasets1.index(dataset)]+ "/"+"1. Raw images"+"/1. Input images/"
            # read csv file
            df_delta = pd.read_csv(DeLTA_csv_file)
            df_delta_without_skip = pd.read_csv(DeLTA_csv_file_without_skip)

            # time steps
            t = list(set(df_delta['TimeStep'].values))
            for i in range(len(t)):
                fig, ax = plt.subplots()
                df_current = df_delta.loc[df_delta["TimeStep"] == t[i]]
                df_current_without_skip = df_delta_without_skip.loc[df_delta_without_skip["TimeStep"] == ((t[i]-1)*10)+1]
                # plot
                Tool = ["DeLTA"]
                #plot_without_skip(df_current_without_skip,img_dir_without_skip,((t[i]-1)*10)+1,Tool,dataset,modes_title[mode],ax[0])
                plot(df_current,img_dir,t[i],Tool,dataset,modes_title[mode],ax)

                plt.suptitle("Tracking Objects in TimeStep "+ str(((t[i]-1)*10)+1), fontsize=14, fontweight="bold")
                #plt.show()
                fig.savefig(
                     "../img/"+dataset+"/"+modes_title[mode]+"/"+Tool[0]+"/" +"/"+ "Objects in TimeStep "+ str(((t[i]-1)*10)+1)+ "_" + dataset + " ("+modes_title[mode]+").png",
                    dpi=1200,
                )
                # close fig
                fig.clf()
                plt.close()                


if __name__ == "__main__":

    # main directory of each image processing tools
    main_directories = {
        "DeLTA_directory": "../../../DeLTA/",
    }

    # datasets
    #        "Pseudomonas_agarose",
    #    "SuperSegger sample images set",
    #    "Xanthomonase_agarose",
    datasets1 = [
        "E.coli_mono_agarose_skipTimeSteps"

    ]
    datasets2 = [
        "E.coli_mono_agarose"

    ]    
    #"2. Ilastik Output"
    # "1. Raw images"
    modes = ["2. Ilastik Output"]
    # "1. Raw images":"Without Ilastik"
    #"2. Ilastik Output":"With Ilastik"
    modes_title = {"2. Ilastik Output":"With Ilastik"}

    # titles
    plot_titles = ["Objects"]

    # end of file names
    end_of_file_name = "bacteria_feature_analysis"

    Tools_name = ["DeLTA"]

    # life history based distribution
    tracking_bac(
        end_of_file_name,
        Tools_name,
        datasets1,
        datasets2,
        main_directories,
        plot_titles,
        modes,
        modes_title
    )


