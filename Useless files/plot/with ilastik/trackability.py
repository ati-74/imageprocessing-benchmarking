import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics.pairwise import euclidean_distances
from statistics import stdev
from matplotlib.ticker import MaxNLocator


def single_plot(t, trackability_score, name, plot_title, dataset,color):
    fig, ax = plt.subplots()
    plt.plot(t, trackability_score, "-", c=color, label=name)
    plt.xticks(rotation=90, fontsize=6)
    fig.subplots_adjust(bottom=0.2)
    plt.suptitle(
        plot_title + "\n(" + dataset + " (With Ilastik))",
        fontsize=14,
        fontweight="bold",
    )
    plt.legend(loc="upper right")
    ax.set_xlabel('Time Step')
    ax.set_ylabel('Trackability score')
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    # plt.show()
    fig.savefig(
        "../trackability plots/"+dataset + "/" + plot_title + "_" + dataset + "_" + name + ".png",
        dpi=600,
    )
    # close fig
    fig.clf()
    plt.close()

def sort_lists_by_min(*lists):
    return sorted(lists, key=lambda x: sorted(x))

def topN_index_columns_from_symmmdist(dist_df):
    rows_to_list = dist_df.values.tolist()
    num_rows = dist_df.shape[0]
    min_row =rows_to_list[0]
    min_row_indx = 0
    for i in range(1,num_rows):
        min_row = sort_lists_by_min(rows_to_list[i],min_row)[0]
        if min_row == rows_to_list[i]:
            min_row_indx = i
    min_val = min(min_row)
    col_index = min_row.index(min_val)
    min_row_indx = list(dist_df.index)[min_row_indx]
    col_index = list(dist_df.columns.values)[col_index]
    return [min_row_indx,min_val,col_index]


def trackability_calc(df):
    uniq_timeSteps = list(set(df["TimeStep"].values))
    trackability_values = []
    timeStep_val = []
    for timestep in range(len(uniq_timeSteps) - 1):
        print(timestep)
        df_current_timeStep = df.loc[df["TimeStep"] == uniq_timeSteps[timestep]]
        df_next_timeStep = df.loc[df["TimeStep"] == uniq_timeSteps[timestep + 1]]
        # distance matrix
        cols = ["Center_X", "Center_Y"]
        distance_df = pd.DataFrame(
            euclidean_distances(df_current_timeStep[cols], df_next_timeStep[cols])
        )
        # min distance values in each rows
        min_distance_in_each_rows = distance_df.values.min(axis=1).tolist()
        col_index_min_distance = distance_df.values.argmin(axis=1).tolist()
        num_bac = df_current_timeStep.shape[0]
        distance = []
        rows = []
        for i in range(num_bac):
            if distance_df.shape[1]:
                min_info = topN_index_columns_from_symmmdist(distance_df)
                distance.append(min_info[1])
                rows.append(min_info[0])
                # row
                distance_df.drop(min_info[0], axis=0, inplace=True)
                # column
                distance_df.drop(min_info[2], axis=1, inplace=True)
        if len(distance) > 1:
            delta_x_stdev = stdev(distance)
            x = np.sqrt(
                df_current_timeStep["Center_X"] ** 2
                + df_current_timeStep["Center_Y"] ** 2
            )
            x_stdev = stdev(x)
            if delta_x_stdev != 0:
                trackability = (
                    np.log2(x_stdev / delta_x_stdev)
                    + 0.5 * np.log2(6 / (np.pi * np.exp(1)))
                    - np.log2(num_bac)
                )
                trackability_values.append(trackability)
                timeStep_val.append(timestep + 1)
    return timeStep_val, trackability_values


def bac_feature(
    features, end_of_file_name, Tools_name, datasets, main_directories, plot_title
):
    for dataset in datasets:
        CP_csv_file = (
            main_directories["CP_directory"]
            + dataset
            + "/2. Ilastik Output/post-processing/results/"
            + Tools_name[0]
            + "_"
            + end_of_file_name
            + ".csv"
        )
        DeLTA_csv_file = (
            main_directories["DeLTA_directory"]
            + dataset
            + "/2. Ilastik Output/post-processing/results/"
            + Tools_name[1]
            + "_"
            + end_of_file_name
            + ".csv"
        )
        FAST_csv_file = (
            main_directories["FAST_directory"]
            + dataset
            + "/2. Ilastik Output/post-processing/results/"
            + Tools_name[2]
            + "_"
            + end_of_file_name
            + ".csv"
        )
        Oufti_csv_file = (
                main_directories["Oufti_directory"]
                + dataset
                + "/2. Ilastik Output/post-processing/results/"
                + Tools_name[3]
                + "_"
                + end_of_file_name
                + ".csv"
        )
        SuperSegger_csv_file = (
            main_directories["SuperSegger_directory"]
            + dataset
            + "/2. Ilastik Output/post-processing/results/"
            + Tools_name[4]
            + "_"
            + end_of_file_name
            + ".csv"
        )
        # read csv file
        df_cp = pd.read_csv(CP_csv_file, usecols=features)
        df_delta = pd.read_csv(DeLTA_csv_file, usecols=features)
        df_fast = pd.read_csv(FAST_csv_file, usecols=features)
        df_oufti = pd.read_csv(Oufti_csv_file, usecols=features)
        df_supersegger = pd.read_csv(SuperSegger_csv_file, usecols=features)

        # calculation of trackability
        t_CP, trackability_CP = trackability_calc(df_cp)
        # plot
        single_plot(t_CP, trackability_CP, Tools_name[0], plot_title, dataset,'red')        
        t_DeLTA, trackability_DeLTA = trackability_calc(df_delta)
        # plot
        single_plot(t_DeLTA, trackability_DeLTA, Tools_name[1], plot_title, dataset,'black')
        t_FAST, trackability_FAST = trackability_calc(df_fast)
        # plot
        single_plot(t_FAST, trackability_FAST, Tools_name[2], plot_title, dataset,'green')        
        t_Oufti, trackability_Oufti = trackability_calc(df_oufti)
        # plot
        single_plot(t_Oufti, trackability_Oufti, Tools_name[3], plot_title, dataset,'yellow')
        t_SuperSegger, trackability_SuperSegger = trackability_calc(df_supersegger)
        # plot
        single_plot(
            t_SuperSegger, trackability_SuperSegger, Tools_name[4], plot_title, dataset,'blue'
        )
        # all in one
        fig, ax = plt.subplots()
        plt.plot(t_CP, trackability_CP, "-", c="red", label=Tools_name[0])
        plt.plot(t_DeLTA, trackability_DeLTA, "-", c="black", label=Tools_name[1])
        plt.plot(t_FAST, trackability_FAST, "-", c="green", label=Tools_name[2])
        plt.plot(t_Oufti, trackability_Oufti, "-", c="yellow", label=Tools_name[3])
        plt.plot(
            t_SuperSegger, trackability_SuperSegger, "-", c="blue", label=Tools_name[4]
        )
        plt.xticks(rotation=90, fontsize=6)
        fig.subplots_adjust(bottom=0.2)
        plt.suptitle(
            plot_title + "\n(" + dataset + " (With Ilastik))",
            fontsize=14,
            fontweight="bold",
        )
        plt.legend(loc="upper right")
        ax.set_xlabel('Time Step')
        ax.set_ylabel('Trackability score')
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        # plt.show()
        fig.savefig(
            "../trackability plots/" + plot_title + "_" + dataset + ".png", dpi=600
        )
        # close fig
        fig.clf()
        plt.close()


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
    datasets = [
        "Mono Culture",
        "Schnitzcells sample images set",
        "SuperSegger sample images set",
    ]

    # features
    features = ["TimeStep", "Center_X", "Center_Y"]

    # end of file names
    end_of_file_names = {"feature_bac_feature": "bacteria_feature_analysis"}
    Tools_name = ["CP", "DeLTA", "FAST", "Oufti", "SuperSegger"]

    # bac_feature
    bac_feature(
        features,
        end_of_file_names["feature_bac_feature"],
        Tools_name,
        datasets,
        main_directories,
        "Trackability",
    )
