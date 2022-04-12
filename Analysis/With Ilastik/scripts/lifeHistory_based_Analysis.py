import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd


def plot(
    df1,
    df2,
    df3,
    df4,
    df5,
    dataset,
    plot_title,
    min_val,
    max_val,
    num_bins,
    Tools_name,
    feature,
):

    fig, ax = plt.subplots()
    if plot_title in ["distribution of life history for each cell","detected cell division in cells lineage"]:
        min_val = np.round(min_val)
        max_val = np.round(max_val)+1
        num_bins = int(max_val - min_val)
    else:
        max_val = max_val +1
    a_heights, a_bins = np.histogram(df1, bins=num_bins, range=(min_val, max_val))
    b_heights, b_bins = np.histogram(df2, bins=num_bins, range=(min_val, max_val))
    c_heights, c_bins = np.histogram(df3, bins=num_bins, range=(min_val, max_val))
    if dataset !='Schnitzcells sample images set':
        d_heights, d_bins = np.histogram(df4, bins=num_bins, range=(min_val, max_val))
    e_heights, e_bins = np.histogram(df5, bins=num_bins, range=(min_val, max_val))
    width = (a_bins[1] - a_bins[0]) / 5

    ax.bar(a_bins[:-1], a_heights, width=width, facecolor="red", label=Tools_name[0])

    ax.bar(
            b_bins[:-1] + width,
            b_heights,
            width=width,
            facecolor="black",
            label=Tools_name[1],
    )
    ax.bar(
        c_bins[:-1] + 2 * width,
        c_heights,
        width=width,
        facecolor="green",
        label=Tools_name[2],
    )
    if dataset !='Schnitzcells sample images set':
        ax.bar(
            d_bins[:-1] + 3 * width,
            d_heights,
            width=width,
            facecolor="yellow",
            label=Tools_name[3],
        )
    ax.bar(
        e_bins[:-1] + 4 * width,
        e_heights,
        width=width,
        facecolor="blue",
        label=Tools_name[4],
    )
    plt.grid(False, axis="x")

    # bins
    bins_str = []

    if plot_title in ["distribution of life history for each cell","detected cell division in cells lineage"]:
        for i in range(len(a_bins) - 1):
                bins_str.append(
                    str(int(a_bins[i]))
                )
    else:
        for i in range(len(a_bins) - 1):
                bins_str.append(
                    str(np.round(a_bins[i], 2)) + "-" + str(np.round(a_bins[i + 1], 2))
                )
                
    plt.xticks(
        ticks=a_bins[: len(a_bins) - 1], labels=bins_str, rotation=90, fontsize=6
    )
    fig.subplots_adjust(bottom=0.2)
    plt.suptitle(plot_title + "\n(" + dataset + " (With Ilastik))", fontsize=14, fontweight="bold")
    plt.legend(loc="upper right")
    # plt.show()
    fig.savefig("../plots/" + plot_title + "_" + dataset + ".png", dpi=1200)
    # close fig
    fig.clf()
    plt.close()


def life_history_based_distribution(
    features, end_of_file_name, Tools_name, datasets, main_directories, plot_titles
):
    num_bins = 30
    for feature in features:
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
            if dataset != "Mono Culture" or (
                feature not in ["AverageVelocity", "AverageLength"]
            ):
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
            if dataset !='Schnitzcells sample images set':
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
            df_cp = pd.read_csv(CP_csv_file, usecols=[str(feature)])
            # remove nan values
            df_cp = df_cp.loc[df_cp[str(feature)].notnull()]
            if dataset != "Mono Culture" or (
                feature not in ["AverageVelocity", "AverageLength"]
            ):
                df_delta = pd.read_csv(DeLTA_csv_file, usecols=[str(feature)])
                # remove nan values
                df_delta = df_delta.loc[df_delta[str(feature)].notnull()]
            df_fast = pd.read_csv(FAST_csv_file, usecols=[str(feature)])
            # remove nan values
            df_fast = df_fast.loc[df_fast[str(feature)].notnull()]
            if dataset !='Schnitzcells sample images set':
                df_oufti = pd.read_csv(Oufti_csv_file, usecols=[str(feature)])
                # remove nan values
                df_oufti = df_oufti.loc[df_oufti[str(feature)].notnull()]
            df_supersegger = pd.read_csv(SuperSegger_csv_file, usecols=[str(feature)])
            # remove nan values
            df_supersegger = df_supersegger.loc[df_supersegger[str(feature)].notnull()]
            if dataset =='Schnitzcells sample images set':
                # draw plot
                max_val = max(
                    df_cp.values.max(),
                    df_delta.values.max(),
                    df_fast.values.max(),
                    df_supersegger.values.max(),
                )
                min_val = min(
                    df_cp.values.min(),
                    df_delta.values.min(),
                    df_fast.values.min(),
                    df_supersegger.values.min(),
                )
                plot(
                    df_cp,
                    df_delta,
                    df_fast,
                    '',
                    df_supersegger,
                    dataset,
                    plot_titles[feature],
                    min_val,
                    max_val,
                    num_bins,
                    Tools_name,
                    feature,
                )

            else:
                # draw plot
                max_val = max(
                    df_cp.values.max(),
                    df_delta.values.max(),
                    df_fast.values.max(),
                    df_oufti.values.max(),
                    df_supersegger.values.max(),
                )
                min_val = min(
                    df_cp.values.min(),
                    df_delta.values.min(),
                    df_fast.values.min(),
                    df_oufti.values.min(),
                    df_supersegger.values.min(),
                )
                plot(
                    df_cp,
                    df_delta,
                    df_fast,
                    df_oufti,
                    df_supersegger,
                    dataset,
                    plot_titles[feature],
                    min_val,
                    max_val,
                    num_bins,
                    Tools_name,
                    feature,
                )


def lineage_based_distribution(
    features, end_of_file_name, Tools_name, datasets, main_directories, plot_titles
):
    num_bins = 30
    for feature in features:
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
            if dataset !='Schnitzcells sample images set':
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
            df_cp = pd.read_csv(CP_csv_file, usecols=[str(feature)])
            # remove nan values
            df_cp = df_cp.loc[df_cp[str(feature)].notnull()]
            df_delta = pd.read_csv(DeLTA_csv_file, usecols=[str(feature)])
            # remove nan values
            df_delta = df_delta.loc[df_delta[str(feature)].notnull()]
            df_fast = pd.read_csv(FAST_csv_file, usecols=[str(feature)])
            # remove nan values
            df_fast = df_fast.loc[df_fast[str(feature)].notnull()]
            if dataset !='Schnitzcells sample images set':
                df_oufti = pd.read_csv(Oufti_csv_file, usecols=[str(feature)])
                # remove nan values
                df_oufti = df_oufti.loc[df_oufti[str(feature)].notnull()]
            df_supersegger = pd.read_csv(SuperSegger_csv_file, usecols=[str(feature)])
            # remove nan values
            df_supersegger = df_supersegger.loc[df_supersegger[str(feature)].notnull()]
            if dataset !='Schnitzcells sample images set':
                # draw plot
                max_val = max(
                    df_cp.values.max(),
                    df_delta.values.max(),
                    df_fast.values.max(),
                    df_oufti.values.max(),
                    df_supersegger.values.max(),
                )
                min_val = min(
                    df_cp.values.min(),
                    df_delta.values.min(),
                    df_fast.values.min(),
                    df_oufti.values.min(),
                    df_supersegger.values.min(),
                )
                plot(
                    df_cp,
                    df_delta,
                    df_fast,
                    df_oufti,
                    df_supersegger,
                    dataset,
                    plot_titles[feature],
                    min_val,
                    max_val,
                    num_bins,
                    Tools_name,
                    feature,
                )
            else:
                # draw plot
                max_val = max(
                    df_cp.values.max(),
                    df_delta.values.max(),
                    df_fast.values.max(),
                    df_supersegger.values.max(),
                )
                min_val = min(
                    df_cp.values.min(),
                    df_delta.values.min(),
                    df_fast.values.min(),
                    df_supersegger.values.min(),
                )
                plot(
                    df_cp,
                    df_delta,
                    df_fast,
                    '',
                    df_supersegger,
                    dataset,
                    plot_titles[feature],
                    min_val,
                    max_val,
                    num_bins,
                    Tools_name,
                    feature,
                )
                
def timestep_based_distribution(
    features, end_of_file_name, Tools_name, datasets, main_directories, plot_titles
):
    for feature in features:
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
            if dataset !='Schnitzcells sample images set':
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
            df_cp = pd.read_csv(CP_csv_file, usecols=[str(feature)])
            df_cp = df_cp.rename(columns={str(feature): "CellProfiler"})
            df_delta = pd.read_csv(DeLTA_csv_file, usecols=[str(feature)])
            df_delta = df_delta.rename(columns={str(feature): "DeLTA"})
            df_fast = pd.read_csv(FAST_csv_file, usecols=[str(feature)])
            df_fast = df_fast.rename(columns={str(feature): "FAST"})
            if dataset !='Schnitzcells sample images set':
                df_oufti = pd.read_csv(Oufti_csv_file, usecols=[str(feature)])
                df_oufti = df_oufti.rename(columns={str(feature): "Oufti"})
            df_supersegger = pd.read_csv(SuperSegger_csv_file, usecols=[str(feature)])
            df_supersegger = df_supersegger.rename(
                columns={str(feature): "SuperSegger"}
            )
            if dataset !='Schnitzcells sample images set':
                # concatinate columns
                df = pd.concat([df_cp, df_delta, df_fast, df_oufti, df_supersegger], axis=1)
                df.index = np.arange(1, len(df) + 1)
                plot = df.plot(
                    kind="bar", color=["red", "black", "green", "yellow", "blue"]
                )
                plt.xticks(rotation=90, fontsize=6)
                plt.suptitle(
                    plot_titles[feature] + "\n(" + dataset + ")",
                    fontsize=14,
                    fontweight="bold",
                )
                plt.legend(loc="upper right")
                # plt.show()
                fig = plot.get_figure()
                fig.savefig(
                    "../plots/" + plot_titles[feature] + "_" + dataset + ".png", dpi=1200
                )
                # close fig
                fig.clf()
                plt.close()
            else:
                 # concatinate columns
                df = pd.concat([df_cp, df_delta, df_fast,df_supersegger], axis=1)
                df.index = np.arange(1, len(df) + 1)
                plot = df.plot(
                    kind="bar", color=["red", "black", "green","blue"]
                )
                plt.xticks(rotation=90, fontsize=6)
                plt.suptitle(
                    plot_titles[feature] + "\n(" + dataset + ")",
                    fontsize=14,
                    fontweight="bold",
                )
                plt.legend(loc="upper right")
                # plt.show()
                fig = plot.get_figure()
                fig.savefig(
                    "../plots/" + plot_titles[feature] + "_" + dataset + ".png", dpi=1200
                )
                # close fig
                fig.clf()
                plt.close()               


def bac_feature_distribution(
    features, end_of_file_name, Tools_name, datasets, main_directories, plot_titles
):
    num_bins = 30
    for feature in features:
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
            if dataset != "Mono Culture" or (feature not in ["Orientation"]):
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
            if dataset !='Schnitzcells sample images set':
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
            df_cp = pd.read_csv(CP_csv_file, usecols=[str(feature)])
            # remove nan values
            df_cp = df_cp.loc[df_cp[str(feature)].notnull()]
            if dataset != "Mono Culture" or (feature not in ["Orientation"]):
                df_delta = pd.read_csv(DeLTA_csv_file, usecols=[str(feature)])
                # remove nan values
                df_delta = df_delta.loc[df_delta[str(feature)].notnull()]
            df_fast = pd.read_csv(FAST_csv_file, usecols=[str(feature)])
            # remove nan values
            df_fast = df_fast.loc[df_fast[str(feature)].notnull()]
            if dataset !='Schnitzcells sample images set':
                df_oufti = pd.read_csv(Oufti_csv_file, usecols=[str(feature)])
                # remove nan values
                df_oufti = df_oufti.loc[df_oufti[str(feature)].notnull()]
            df_supersegger = pd.read_csv(SuperSegger_csv_file, usecols=[str(feature)])
            # remove nan values
            df_supersegger = df_supersegger.loc[df_supersegger[str(feature)].notnull()]
            if dataset =='Schnitzcells sample images set':
                # draw plot
                max_val = max(
                    df_cp.values.max(),
                    df_delta.values.max(),
                    df_fast.values.max(),
                    df_supersegger.values.max(),
                )
                min_val = min(
                    df_cp.values.min(),
                    df_delta.values.min(),
                    df_fast.values.min(),
                    df_supersegger.values.min(),
                )
                plot(
                    df_cp,
                    df_delta,
                    df_fast,
                    '',
                    df_supersegger,
                    dataset,
                    plot_titles[feature],
                    min_val,
                    max_val,
                    num_bins,
                    Tools_name,
                    feature,
                )

            else:
                # draw plot
                max_val = max(
                    df_cp.values.max(),
                    df_delta.values.max(),
                    df_fast.values.max(),
                    df_oufti.values.max(),
                    df_supersegger.values.max(),
                )
                min_val = min(
                    df_cp.values.min(),
                    df_delta.values.min(),
                    df_fast.values.min(),
                    df_oufti.values.min(),
                    df_supersegger.values.min(),
                )
                plot(
                    df_cp,
                    df_delta,
                    df_fast,
                    df_oufti,
                    df_supersegger,
                    dataset,
                    plot_titles[feature],
                    min_val,
                    max_val,
                    num_bins,
                    Tools_name,
                    feature,
                )


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
        "Schnitzcells sample images set",
        "SuperSegger sample images set",
    ]

    # features
    features = {
        "features_lifehistory_based": [
            "birthLength",
            "AverageLength",
            "AverageVelocity",
            "LifeHistory",
            "GrowthRate",
        ],
        "feature_lineage_based": ["NumberOfDivision"],
        "feature_bac_feature": ["Orientation"],
        "feature_timeStep_based": ["NumberOfCells"],
    }
    # titles
    plot_titles = {
        "features_lifehistory_based": {
            "birthLength": "birth length distribution",
            "LifeHistory": "distribution of life history for each cell",
            "GrowthRate": "distribution of growth rate",
            "AverageVelocity": "velocity of bacteria in their life history",
            "AverageLength": "distribution of length in life history",
        },
        "feature_lineage_based": {
            "NumberOfDivision": "detected cell division in cells lineage"
        },
        "feature_bac_feature": {
            "Orientation": "orientation of bacteria in each time step "
        },
        "feature_timeStep_based": {
            "NumberOfCells": "number of cells in each time step"
        },
    }

    # end of file names
    end_of_file_names = {
        "features_lifehistory_based": "LifeHistory_based_Analysis",
        "feature_lineage_based": "lineage_based_analysis",
        "feature_bac_feature": "bacteria_feature_analysis",
        "feature_timeStep_based": "Num_cells_in_each_timeStep",
    }
    Tools_name = ["CP", "DeLTA", "FAST", "Oufti", "SuperSegger"]

    # life history based distribution
    life_history_based_distribution(
        features["features_lifehistory_based"],
        end_of_file_names["features_lifehistory_based"],
        Tools_name,
        datasets,
        main_directories,
        plot_titles["features_lifehistory_based"],
    )
    # lineage based feature
    life_history_based_distribution(
        features["feature_lineage_based"],
        end_of_file_names["feature_lineage_based"],
        Tools_name,
        datasets,
        main_directories,
        plot_titles["feature_lineage_based"],
    )
    # bac_feature
    bac_feature_distribution(
        features["feature_bac_feature"],
        end_of_file_names["feature_bac_feature"],
        Tools_name,
        datasets,
        main_directories,
        plot_titles["feature_bac_feature"],
    )
    # timestep_based
    timestep_based_distribution(
        features["feature_timeStep_based"],
        end_of_file_names["feature_timeStep_based"],
        Tools_name,
        datasets,
        main_directories,
        plot_titles["feature_timeStep_based"],
    )
