import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import matplotlib.patheffects as mpe
import matplotlib.patches as mpatches
import cv2


def plot_fast(bc_df,t,tool,clr,dataset,mode_title): 

    fig, ax = plt.subplots()
    # draw Objects
    ax = plt.gca()

    for indx , df in enumerate(bc_df):
        # Objects information
        (
            Objects_center_coord,
            Objects_major,
            Objects_minor,
            Objects_orientation,
        ) = bac_info(df)
        # number of cells
        num_cells = df.shape[0]
        for cell_indx in range(num_cells):
            center = (
                Objects_center_coord.iloc[cell_indx]["Center_X"],
                Objects_center_coord.iloc[cell_indx]["Center_Y"],
            )
            minor = Objects_minor.iloc[cell_indx] / 2
            major = Objects_major.iloc[cell_indx] / 2
            # radian
            angle = -(Objects_orientation.iloc[cell_indx]) * np.pi / 180

            # endpoints
            Node_x1_x = center[0] + major * np.cos(angle)
            Node_x1_y = center[1] + major * np.sin(angle)
            Node_x2_x = center[0] - major * np.cos(angle)
            Node_x2_y = center[1] - major * np.sin(angle)
            print([Node_x1_x,Node_x1_y,Node_x2_x,Node_x2_y])
            plt.plot(
                    [Node_x1_x, Node_x2_x],
                    [Node_x1_y, Node_x2_y],
                    lw=minor/70+1,
                    solid_capstyle="round",
                    color = "#5d5d5d",
                    alpha = 0.5
            )
            plt.plot(
                    [Node_x1_x, Node_x2_x],
                    [Node_x1_y, Node_x2_y],
                    lw=minor/70,
                    solid_capstyle="round",
                    color = clr[indx],
                    alpha = 0.5
            )

    patch_0 = mpatches.Patch(color=clr[0], label=tool[0])
    plt.legend(handles=[patch_0])
    plt.suptitle("Objects in TimeStep "+ str(t), fontsize=14, fontweight="bold")
    ax.set_xlim((ax.get_xlim()[0],ax.get_xlim()[1]))
    ax.set_ylim((ax.get_ylim()[1],ax.get_ylim()[0]))
    plt.tight_layout()
    plt.show()
    fig.savefig(
         "../img/"+dataset+"/" +mode_title+"/"+ "Objects in TimeStep "+ str(t)+ "_" + dataset + "_FAST ("+mode_title+") .png",
        dpi=600,
    )
    # close fig
    fig.clf()
    plt.close()
    

def plot(bc_df,t,tool,clr,dataset,mode_title):   

    fig, ax = plt.subplots()
    # draw Objects
    ax = plt.gca()

    for indx , df in enumerate(bc_df):
        # Objects information
        (
            Objects_center_coord,
            Objects_major,
            Objects_minor,
            Objects_orientation,
        ) = bac_info(df)
        # number of cells
        num_cells = df.shape[0]
        for cell_indx in range(num_cells):
            center = (
                Objects_center_coord.iloc[cell_indx]["Center_X"],
                Objects_center_coord.iloc[cell_indx]["Center_Y"],
            )
            minor = Objects_minor.iloc[cell_indx] / 2
            major = Objects_major.iloc[cell_indx] / 2
            # radian
            if tool[indx] == "CellProfiler":
                angle = -(Objects_orientation.iloc[cell_indx]+90) * np.pi / 180
            elif tool[indx] == "FAST" or tool[indx] =="Oufti":
                angle = -(Objects_orientation.iloc[cell_indx]) * np.pi / 180
            elif tool[indx] == "SuperSegger":
                angle = (Objects_orientation.iloc[cell_indx]) * np.pi / 180
            elif tool[indx] == "DeLTA":
                #center = (center[0],center[1])
                #angle = Objects_orientation.iloc[cell_indx]
                #dimension = (df.iloc[cell_indx]["width"],df.iloc[cell_indx]["height"])
                #pts = cv2.boxPoints((center,dimension,angle))
                if df.iloc[cell_indx]["width"] > df.iloc[cell_indx]["height"] :
                    angle = (Objects_orientation.iloc[cell_indx]) * np.pi / 180
                else:
                    angle = (Objects_orientation.iloc[cell_indx]+90) * np.pi / 180

                # endpoints
            Node_x1_x = center[0] + major * np.cos(angle)
            Node_x1_y = center[1] + major * np.sin(angle)
            Node_x2_x = center[0] - major * np.cos(angle)
            Node_x2_y = center[1] - major * np.sin(angle)
            plt.plot(
                    [Node_x1_x, Node_x2_x],
                    [Node_x1_y, Node_x2_y],
                    lw=minor+1,
                    solid_capstyle="round",
                    color = "#5d5d5d",
                    alpha = 0.5
            )
            #cv2.drawContours(pts,color = clr[indx],alpha = 0.5)
            plt.plot(
                    [Node_x1_x, Node_x2_x],
                    [Node_x1_y, Node_x2_y],
                    lw=minor,
                    solid_capstyle="round",
                    color = clr[indx],
                    alpha = 0.5
            )
    #if mode_title == "With Ilastik":
    #    patch_0 = mpatches.Patch(color=clr[0], label=tool[0])
    #    patch_1 = mpatches.Patch(color=clr[1], label=tool[1])
    #    patch_2 = mpatches.Patch(color=clr[2], label=tool[2])
    #    patch_3 = mpatches.Patch(color=clr[3], label=tool[3])
    #    patch_4 = mpatches.Patch(color=clr[4], label=tool[4])
    #    plt.legend(handles=[patch_0,patch_1,patch_2,patch_3,patch_4],loc='upper right', ncol=5, bbox_to_anchor=(1.09, 1.09))
    #else:
    patch_0 = mpatches.Patch(color=clr[0], label=tool[0])
    patch_1 = mpatches.Patch(color=clr[1], label=tool[1])
    patch_2 = mpatches.Patch(color=clr[2], label=tool[2])
    patch_3 = mpatches.Patch(color=clr[3], label=tool[3])
    plt.legend(handles=[patch_0,patch_1,patch_2,patch_3],loc='upper right', ncol=5, bbox_to_anchor=(1.01, 1.09))
    plt.suptitle("Objects in TimeStep "+ str(t), fontsize=14, fontweight="bold")
    ax.set_ylim(ax.get_ylim()[::-1])
    # plt.show()
    fig.savefig(
         "../img/"+dataset+"/" +mode_title+"/"+ "Objects in TimeStep "+ str(t)+ "_" + dataset + " ("+mode_title+").png",
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



def Overlapping_Objects(end_of_file_name,Tools_name,datasets,main_directories,
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
            
            DeLTA_csv_file = (
                    main_directories["DeLTA_directory"]
                    + dataset
                    + "/"+mode+"/post-processing/results/"
                    + Tools_name[1]
                    + "_"
                    + end_of_file_name
                    + ".csv"
            )
            #FAST_csv_file = (
            #    main_directories["FAST_directory"]
            #    + dataset
            #    + "/"+mode+"/post-processing/results/"
            #    + Tools_name[2]
            #    + "_"
            #    + end_of_file_name
            #    + ".csv"
            #)
            Oufti_csv_file = (
                    main_directories["Oufti_directory"]
                    + dataset
                    + "/"+mode+"/post-processing/results/"
                    + Tools_name[3]
                    + "_"
                    + end_of_file_name
                    + ".csv"
                )
            SuperSegger_csv_file = (
                main_directories["SuperSegger_directory"]
                + dataset
                + "/"+mode+"/post-processing/results/"
                + Tools_name[4]
                + "_"
                + end_of_file_name
                + ".csv"
            )
            # read csv file
            df_cp = pd.read_csv(CP_csv_file)
            df_delta = pd.read_csv(DeLTA_csv_file)
            #df_fast = pd.read_csv(FAST_csv_file)
            #df_fast = df_fast.loc[df_fast["Major_axis"].notnull()]
            df_oufti = pd.read_csv(Oufti_csv_file)
            df_supersegger = pd.read_csv(SuperSegger_csv_file)       

                # time steps
            t = list(set(df_cp['TimeStep'].values))
            for TimeStep in t:
                df_cp_t = df_cp.loc[df_cp["TimeStep"] == TimeStep]
                df_delta_t = df_delta.loc[df_delta["TimeStep"] == TimeStep]
                #df_fast_t = df_fast.loc[df_fast["TimeStep"] == TimeStep]
                df_oufti_t = df_oufti.loc[df_oufti["TimeStep"] == TimeStep]
                df_supersegger_t = df_supersegger.loc[df_supersegger["TimeStep"] == TimeStep]
                # plot
                #if mode == "2. Ilastik Output":
                #    bc_df = [df_cp_t,df_oufti_t,df_fast_t,df_delta_t,df_supersegger_t]
                #    color = ["yellow","red","#00ff00","black","blue"]
                #    Tool = ["CellProfiler","Oufti","FAST","DeLTA","SuperSegger"]
                #    plot(bc_df,TimeStep,Tool,color,dataset,modes_title[mode])
                #else:

                bc_df = [df_cp_t,df_oufti_t,df_delta_t,df_supersegger_t]
                    #bc_df = [df_delta_t]
                    #color = ["red"]
                    #Tool = ["DeLTA"]
                color = ["yellow","red","black","blue"]
                Tool = ["CellProfiler","Oufti","DeLTA","SuperSegger"]
                plot(bc_df,TimeStep,Tool,color,dataset,modes_title[mode])
                    #plot_fast([df_fast_t],TimeStep,["FAST"],["#00ff00"],dataset,modes_title[mode])
                #plot(df_delta,TimeStep,"DeLTA")
                #plot(df_oufti,TimeStep,"Oufti")


if __name__ == "__main__":

    # main directory of each image processing tools
    main_directories = {
        "CP_directory": "../../../CellProfiler/",
        "DeLTA_directory": "../../../DeLTA/",
        "FAST_directory": "../../../FAST/",
        "Oufti_directory": "../../../Oufti/",
        "SuperSegger_directory": "../../../SuperSegger/",
    }

    # datasets
    # E.coli_mono_agarose_noisy
    #"Pseudomonas_agarose"
    #        "Xanthomonase_agarose"
    # xanthomonas microfluidic each3 min-01-Image Export-02
    datasets = [
        "E.coli_mono_agarose_noisy"
    ]
    modes = ["1. Raw images", "2. Ilastik Output"]
    modes_title = { "1. Raw images":"Without Ilastik", "2. Ilastik Output":"With Ilastik"}

    # titles
    plot_titles = ["Objects"]

    # end of file names
    end_of_file_name = "bacteria_feature_analysis"

    Tools_name = ["CellProfiler", "DeLTA", "FAST", "Oufti", "SuperSegger"]

    # life history based distribution
    Overlapping_Objects(
        end_of_file_name,
        Tools_name,
        datasets,
        main_directories,
        plot_titles,
        modes,
        modes_title
    )

