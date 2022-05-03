import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

def plot_subplots(
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
    x_lable,
    y_lable
):

    fig, ax = plt.subplots(nrows=3, ncols=2)
    if plot_title in ["distribution of life history for each object","Detected divisions in object lineage"]:
        num_bins = int((df1.values.max()+1)-(df1.values.min()))
        a_heights, a_bins = np.histogram(df1, bins=num_bins, range=(df1.values.min(), df1.values.max()+1))
        num_bins = int((df2.values.max()+1)-(df2.values.min()))
        b_heights, b_bins = np.histogram(df2, bins=num_bins, range=(df2.values.min(), df2.values.max()+1))
        num_bins = int((df3.values.max()+1)-(df3.values.min()))
        c_heights, c_bins = np.histogram(df3, bins=num_bins, range=(df3.values.min(), df3.values.max()+1))
        num_bins = int((df4.values.max()+1)-(df4.values.min()))
        d_heights, d_bins = np.histogram(df4, bins=num_bins, range=(df4.values.min(), df4.values.max()+1))
        num_bins = int((df4.values.max()+1)-(df4.values.min()))
        e_heights, e_bins = np.histogram(df5, bins=num_bins, range=(df5.values.min(), df5.values.max()+1))
    else:
        a_heights, a_bins = np.histogram(df1, bins=num_bins, range=(df1.values.min(), df1.values.max()+1))
        b_heights, b_bins = np.histogram(df2, bins=num_bins, range=(df2.values.min(), df2.values.max()+1))
        c_heights, c_bins = np.histogram(df3, bins=num_bins, range=(df3.values.min(), df3.values.max()+1))
        d_heights, d_bins = np.histogram(df4, bins=num_bins, range=(df4.values.min(), df4.values.max()+1))
        e_heights, e_bins = np.histogram(df5, bins=num_bins, range=(df5.values.min(), df5.values.max()+1))        

    ax[0,0].bar(
        a_bins[:-1],
        a_heights,
        facecolor="yellow",
        width=(a_bins[1] - a_bins[0]) / 5,
        label=Tools_name[0]
        )
    ax[0,0].legend(loc='upper right', prop={'size': 8})

    ax[0,1].bar(
            b_bins[:-1],
            b_heights,
            facecolor="black",
            width=(b_bins[1] - b_bins[0]) / 5,
            label=Tools_name[1],
    )
    ax[0,1].legend(loc='upper right', prop={'size': 8})
    
    ax[1,0].bar(
        c_bins[:-1],
        c_heights,
        facecolor="#00ff00",
        width=(c_bins[1] - c_bins[0]) / 5,
        label=Tools_name[2],
    )
    ax[1,0].legend(loc='upper right', prop={'size': 8})
    
    ax[1,1].bar(
            d_bins[:-1],
            d_heights,
            facecolor="red",
            width=(d_bins[1] - d_bins[0]) / 5,
            label=Tools_name[3],
    )
    ax[1,1].legend(loc='upper right', prop={'size': 8})
    
    ax[2,0].bar(
        e_bins[:-1],
        e_heights,
        facecolor="blue",
        width=(e_bins[1] - e_bins[0]) / 5,
        label=Tools_name[4],
    )
    ax[2,0].legend(loc='upper right', prop={'size': 8})
    #print(ax)
    fig.delaxes(ax[2,1])

    # bins
    bins_str_0 = []
    bins_str_1 = []
    bins_str_2 = []
    bins_str_3 = []
    bins_str_4 = []

    if plot_title in ["distribution of life history for each object","Detected divisions in object lineage"]:
        for i in range(len(a_bins) - 1):
                    bins_str_0.append(
                        str(int(a_bins[i]))
                    )
        for i in range(len(b_bins) - 1):
                    bins_str_1.append(
                        str(int(b_bins[i]))
                    )
        for i in range(len(c_bins) - 1):
                    bins_str_2.append(
                        str(int(c_bins[i]))
                    )
        for i in range(len(d_bins) - 1):
                    bins_str_3.append(
                        str(int(d_bins[i]))
                    )
        for i in range(len(e_bins) - 1):
                    bins_str_4.append(
                        str(int(e_bins[i]))
                    )
    else:
        for i in range(len(a_bins) - 1):
                    bins_str_0.append(
                       str(np.round(a_bins[i], 2)) + "-" + str(np.round(a_bins[i + 1], 2))
                    )
        for i in range(len(b_bins) - 1):
                    bins_str_1.append(
                        str(np.round(b_bins[i], 2)) + "-" + str(np.round(b_bins[i + 1], 2))
                    )
        for i in range(len(c_bins) - 1):
                    bins_str_2.append(
                        str(np.round(c_bins[i], 2)) + "-" + str(np.round(c_bins[i + 1], 2))
                    )
        for i in range(len(d_bins) - 1):
                    bins_str_3.append(
                        str(np.round(d_bins[i], 2)) + "-" + str(np.round(d_bins[i + 1], 2))
                    )
        for i in range(len(e_bins) - 1):
                    bins_str_4.append(
                        str(np.round(e_bins[i], 2)) + "-" + str(np.round(e_bins[i + 1], 2))
                    )                
                    
    plt.sca(ax[0, 0])
    plt.xticks(
        ticks=a_bins[: len(a_bins) - 1], labels=bins_str_0, rotation=90, fontsize=2
    )
    plt.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
    ax[0, 0].yaxis.get_offset_text().set_fontsize(8)

    plt.sca(ax[0, 1])                
    plt.xticks(
        ticks=b_bins[: len(b_bins) - 1], labels=bins_str_1, rotation=90, fontsize=2
    )
    plt.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
    ax[0, 1].yaxis.get_offset_text().set_fontsize(8)

    plt.sca(ax[1, 0])
    plt.xticks(
        ticks=c_bins[: len(c_bins) - 1], labels=bins_str_2, rotation=90, fontsize=2
    )
    plt.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
    ax[1 , 0].yaxis.get_offset_text().set_fontsize(8)

    plt.sca(ax[1, 1])
    plt.xticks(
        ticks=d_bins[: len(d_bins) - 1], labels=bins_str_3, rotation=90, fontsize=2
    )
    plt.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
    ax[1, 1].yaxis.get_offset_text().set_fontsize(8)

    plt.sca(ax[2, 0])                
    plt.xticks(
        ticks=e_bins[: len(e_bins) - 1], labels=bins_str_4, rotation=90, fontsize=2
    )
    plt.ticklabel_format(axis='y', style='sci', scilimits=(0,0))
    ax[2 , 0].yaxis.get_offset_text().set_fontsize(8)
    
    fig.subplots_adjust(bottom=0.5)
    plt.suptitle(plot_title, fontsize=14, fontweight="bold")
    ax[0,0].set_ylabel(y_lable,fontsize=6)
    ax[1,0].set_ylabel(y_lable,fontsize=6)
    ax[1,1].set_xlabel(x_lable,fontsize=6)
    ax[2,0].set_xlabel(x_lable,fontsize=6)
    ax[2,0].set_ylabel(y_lable,fontsize=6)    
    #plt.legend()
    # set the spacing between subplots
    plt.subplots_adjust(left=0.1,
                        bottom=0.1, 
                        right=0.9, 
                        top=0.9, 
                        wspace=0.4, 
                        hspace=0.4)

    
    #plt.show()
    fig.savefig("../plots/" +dataset+"/"+ plot_title + "_" + dataset+"_WithoutIlastik_subplots" + ".png", dpi=1200)
    # close fig
    fig.clf()
    plt.close()





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
    x_lable,
    y_lable
):

    fig, ax = plt.subplots()
    if plot_title in ["distribution of life history for each object","Detected divisions in object lineage"]:
        min_val = np.round(min_val)
        max_val = np.round(max_val)+1
        num_bins = int(max_val - min_val)
    else:
        max_val = max_val +1
    a_heights, a_bins = np.histogram(df1, bins=num_bins, range=(min_val, max_val))
    b_heights, b_bins = np.histogram(df2, bins=num_bins, range=(min_val, max_val))
    c_heights, c_bins = np.histogram(df3, bins=num_bins, range=(min_val, max_val))
    d_heights, d_bins = np.histogram(df4, bins=num_bins, range=(min_val, max_val))
    e_heights, e_bins = np.histogram(df5, bins=num_bins, range=(min_val, max_val))
    width = (a_bins[1] - a_bins[0]) / 5

    ax.bar(a_bins[:-1], a_heights, width=width, facecolor="yellow", label=Tools_name[0])

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
        facecolor="#00ff00",
        label=Tools_name[2],
    )
    ax.bar(
            d_bins[:-1] + 3 * width,
            d_heights,
            width=width,
            facecolor="red",
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

    if plot_title in ["distribution of life history for each object","Detected divisions in object lineage"]:
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
    plt.suptitle(plot_title, fontsize=14, fontweight="bold")
    ax.set_xlabel(x_lable)
    ax.set_ylabel(y_lable)
    plt.legend()
    # plt.show()
    fig.savefig("../plots/" +dataset+"/"+ plot_title + "_" + dataset+"_WithoutIlastik" + ".png", dpi=1200)
    # close fig
    fig.clf()
    plt.close()


def life_history_based_distribution(
    features, end_of_file_name, Tools_name, datasets, main_directories, plot_titles, plot_x_lable
):
    num_bins = 30
    for feature in features:
        for dataset in datasets:
            CP_csv_file = (
                main_directories["CP_directory"]
                + dataset
                + "/1. Raw Images/post-processing/results/"
                + Tools_name[0]
                + "_"
                + end_of_file_name
                + ".csv"
            )
            DeLTA_csv_file = (
                    main_directories["DeLTA_directory"]
                    + dataset
                    + "/1. Raw Images/post-processing/results/"
                    + Tools_name[1]
                    + "_"
                    + end_of_file_name
                    + ".csv"
            )
            FAST_csv_file = (
                main_directories["FAST_directory"]
                + dataset
                + "/1. Raw Images/post-processing/results/"
                + Tools_name[2]
                + "_"
                + end_of_file_name
                + ".csv"
            )
            Oufti_csv_file = (
                    main_directories["Oufti_directory"]
                    + dataset
                    + "/1. Raw Images/post-processing/results/"
                    + Tools_name[3]
                    + "_"
                    + end_of_file_name
                    + ".csv"
            )
            SuperSegger_csv_file = (
                main_directories["SuperSegger_directory"]
                + dataset
                + "/1. Raw Images/post-processing/results/"
                + Tools_name[4]
                + "_"
                + end_of_file_name
                + ".csv"
            )
            # read csv file
            df_cp = pd.read_csv(CP_csv_file, usecols=[str(feature)])
            # remove nan values
            df_cp = df_cp.loc[df_cp[str(feature)].notnull()]
            # remove outliers
            # https://www.askpython.com/python/examples/detection-removal-outliers-in-python
            q75,q25 = np.percentile(df_cp.loc[:,str(feature)],[75,25])
            intr_qr = q75-q25
            max_val = q75+(1.5*intr_qr)
            min_val = q25-(1.5*intr_qr)
            df_cp = df_cp.loc[(df_cp[str(feature)] >= min_val) & (df_cp[str(feature)]<= max_val)]
    
            df_delta = pd.read_csv(DeLTA_csv_file, usecols=[str(feature)])
            # remove nan values
            df_delta = df_delta.loc[df_delta[str(feature)].notnull()]
            # remove outliers
            q75,q25 = np.percentile(df_delta.loc[:,str(feature)],[75,25])
            intr_qr = q75-q25
            max_val = q75+(1.5*intr_qr)
            min_val = q25-(1.5*intr_qr)
            df_delta = df_delta.loc[(df_delta[str(feature)] >= min_val) & (df_delta[str(feature)]<= max_val)]
            
            df_fast = pd.read_csv(FAST_csv_file, usecols=[str(feature)])
            # remove nan values
            df_fast = df_fast.loc[df_fast[str(feature)].notnull()]
            # remove outliers
            q75,q25 = np.percentile(df_fast.loc[:,str(feature)],[75,25])
            intr_qr = q75-q25
            max_val = q75+(1.5*intr_qr)
            min_val = q25-(1.5*intr_qr)
            df_fast = df_fast.loc[(df_fast[str(feature)] >= min_val) & (df_fast[str(feature)]<= max_val)]
            
            df_oufti = pd.read_csv(Oufti_csv_file, usecols=[str(feature)])
            # remove nan values
            df_oufti = df_oufti.loc[df_oufti[str(feature)].notnull()]
            # remove outliers
            q75,q25 = np.percentile(df_oufti.loc[:,str(feature)],[75,25])
            intr_qr = q75-q25
            max_val = q75+(1.5*intr_qr)
            min_val = q25-(1.5*intr_qr)
            df_oufti = df_oufti.loc[(df_oufti[str(feature)] >= min_val) & (df_oufti[str(feature)]<= max_val)]
            
            df_supersegger = pd.read_csv(SuperSegger_csv_file, usecols=[str(feature)])
            # remove nan values
            df_supersegger = df_supersegger.loc[df_supersegger[str(feature)].notnull()]
            # remove outliers
            q75,q25 = np.percentile(df_supersegger.loc[:,str(feature)],[75,25])
            intr_qr = q75-q25
            max_val = q75+(1.5*intr_qr)
            min_val = q25-(1.5*intr_qr)
            df_supersegger = df_supersegger.loc[(df_supersegger[str(feature)] >= min_val) & (df_supersegger[str(feature)]<= max_val)]                         
            
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
                    plot_x_lable[plot_titles[feature]],
                    'Number of Objects'
            )
            plot_subplots(
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
                    plot_x_lable[plot_titles[feature]],
                    'Number of Objects'
            )    


def lineage_based_distribution(
    features, end_of_file_name, Tools_name, datasets, main_directories, plot_titles, plot_x_lable
):
    num_bins = 30
    for feature in features:
        for dataset in datasets:
            CP_csv_file = (
                main_directories["CP_directory"]
                + dataset
                + "/1. Raw Images/post-processing/results/"
                + Tools_name[0]
                + "_"
                + end_of_file_name
                + ".csv"
            )
            DeLTA_csv_file = (
                main_directories["DeLTA_directory"]
                + dataset
                + "/1. Raw Images/post-processing/results/"
                + Tools_name[1]
                + "_"
                + end_of_file_name
                + ".csv"
            )
            FAST_csv_file = (
                main_directories["FAST_directory"]
                + dataset
                + "/1. Raw Images/post-processing/results/"
                + Tools_name[2]
                + "_"
                + end_of_file_name
                + ".csv"
            )
            Oufti_csv_file = (
                    main_directories["Oufti_directory"]
                    + dataset
                    + "/1. Raw Images/post-processing/results/"
                    + Tools_name[3]
                    + "_"
                    + end_of_file_name
                    + ".csv"
            )
            SuperSegger_csv_file = (
                main_directories["SuperSegger_directory"]
                + dataset
                + "/1. Raw Images/post-processing/results/"
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
            
            df_oufti = pd.read_csv(Oufti_csv_file, usecols=[str(feature)])
            # remove nan values
            df_oufti = df_oufti.loc[df_oufti[str(feature)].notnull()]
            
            df_supersegger = pd.read_csv(SuperSegger_csv_file, usecols=[str(feature)])
            # remove nan values
            df_supersegger = df_supersegger.loc[df_supersegger[str(feature)].notnull()]

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
                    plot_x_lable[plot_titles[feature]],
                    'Number of Family Trees'
            )
            plot_subplots(
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
                    plot_x_lable[plot_titles[feature]],
                    'Number of Family Trees'
            )
                
def timestep_based_distribution(
    features, end_of_file_name, Tools_name, datasets, main_directories, plot_titles
):
    for feature in features:
        for dataset in datasets:
            CP_csv_file = (
                main_directories["CP_directory"]
                + dataset
                + "/1. Raw Images/post-processing/results/"
                + Tools_name[0]
                + "_"
                + end_of_file_name
                + ".csv"
            )
            DeLTA_csv_file = (
                main_directories["DeLTA_directory"]
                + dataset
                + "/1. Raw Images/post-processing/results/"
                + Tools_name[1]
                + "_"
                + end_of_file_name
                + ".csv"
            )
            FAST_csv_file = (
                main_directories["FAST_directory"]
                + dataset
                + "/1. Raw Images/post-processing/results/"
                + Tools_name[2]
                + "_"
                + end_of_file_name
                + ".csv"
            )
            Oufti_csv_file = (
                    main_directories["Oufti_directory"]
                    + dataset
                    + "/1. Raw Images/post-processing/results/"
                    + Tools_name[3]
                    + "_"
                    + end_of_file_name
                    + ".csv"
            )
            SuperSegger_csv_file = (
                main_directories["SuperSegger_directory"]
                + dataset
                + "/1. Raw Images/post-processing/results/"
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
            df_oufti = pd.read_csv(Oufti_csv_file, usecols=[str(feature)])
            df_oufti = df_oufti.rename(columns={str(feature): "Oufti"})
            df_supersegger = pd.read_csv(SuperSegger_csv_file, usecols=[str(feature)])
            df_supersegger = df_supersegger.rename(
                columns={str(feature): "SuperSegger"}
            )
            # concatinate columns
            fig, ax = plt.subplots(nrows=3, ncols=2)
            num_timesteps = round(len(df_cp) / 6)
            end_index = 1
            start = 0
            col_num = 0
            row_num = 0
            for i in range(6):
                if end_index !=1:
                    start = end + 1
                    end = (end_index)*num_timesteps
                else:
                    end = (end_index)*num_timesteps - 1
                if i==5:
                    end = len(df_cp)-1
                df = pd.concat([df_cp.loc[start:end], df_delta.loc[start:end], df_fast.loc[start:end], df_oufti.loc[start:end], df_supersegger.loc[start:end]], axis=1)
                df.index = np.arange(start+1, end+2)
                plot1 = df.plot(
                        ax=ax[row_num,col_num],kind="bar", color=["yellow", "black", "#00ff00", "red", "blue"], legend=False
                )
                if col_num ==0:
                    ax[row_num,col_num].set_ylabel('Number of Objects',fontsize=6)
                if row_num==2:
                    ax[row_num,col_num].set_xlabel("Time Step",fontsize=6)
                ax[row_num,col_num].yaxis.get_offset_text().set_fontsize(8)
                plt.sca(ax[row_num,col_num])
                plt.xticks(
                    rotation=90, fontsize=4
                    )
                
                plt.suptitle(
                        plot_titles[feature],
                        fontsize=14,
                        fontweight="bold",
                )
                # add end_index
                end_index = end_index + 1
                col_num = col_num + 1
                if col_num == 2:
                    col_num = 0
                    row_num +=1
                    
            handles, labels = ax[0,0].get_legend_handles_labels()
            fig.legend(handles, labels, loc='upper right', ncol=5, bbox_to_anchor=(.80, 0.945), prop={'size': 6})
            plt.subplots_adjust(left=0.1,
                        bottom=0.1, 
                        right=0.9, 
                        top=0.9, 
                        wspace=0.4, 
                        hspace=0.4)
            #plt.show()
            
            #fig = plot.get_figure()
            fig.savefig(
                    "../plots/" +dataset+"/"+ plot_titles[feature] + "_" + dataset+"_WithoutIlastik" + ".png", dpi=1200
            )
            # close fig
            fig.clf()
            plt.close()              


def bac_feature_distribution(
    features, end_of_file_name, Tools_name, datasets, main_directories, plot_titles,plot_x_lable
):
    num_bins = 30
    for feature in features:
        for dataset in datasets:
            CP_csv_file = (
                main_directories["CP_directory"]
                + dataset
                + "/1. Raw Images/post-processing/results/"
                + Tools_name[0]
                + "_"
                + end_of_file_name
                + ".csv"
            )
            DeLTA_csv_file = (
                    main_directories["DeLTA_directory"]
                    + dataset
                    + "/1. Raw Images/post-processing/results/"
                    + Tools_name[1]
                    + "_"
                    + end_of_file_name
                    + ".csv"
            )
            FAST_csv_file = (
                main_directories["FAST_directory"]
                + dataset
                + "/1. Raw Images/post-processing/results/"
                + Tools_name[2]
                + "_"
                + end_of_file_name
                + ".csv"
            )
            Oufti_csv_file = (
                    main_directories["Oufti_directory"]
                    + dataset
                    + "/1. Raw Images/post-processing/results/"
                    + Tools_name[3]
                    + "_"
                    + end_of_file_name
                    + ".csv"
            )
            SuperSegger_csv_file = (
                main_directories["SuperSegger_directory"]
                + dataset
                + "/1. Raw Images/post-processing/results/"
                + Tools_name[4]
                + "_"
                + end_of_file_name
                + ".csv"
            )
            # read csv file
            df_cp = pd.read_csv(CP_csv_file, usecols=[str(feature)])
            # remove nan values
            df_cp = df_cp.loc[df_cp[str(feature)].notnull()]
            df_delta = pd.read_csv(DeLTA_csv_file, usecols=[str(feature),'width','height'])
            # remove nan values
            df_delta = df_delta.loc[df_delta[str(feature)].notnull()]
            df_fast = pd.read_csv(FAST_csv_file, usecols=[str(feature)])
            # remove nan values
            df_fast = df_fast.loc[df_fast[str(feature)].notnull()]
            df_oufti = pd.read_csv(Oufti_csv_file, usecols=[str(feature)])
            # remove nan values
            df_oufti = df_oufti.loc[df_oufti[str(feature)].notnull()]
            df_supersegger = pd.read_csv(SuperSegger_csv_file, usecols=[str(feature)])
            # remove nan values
            df_supersegger = df_supersegger.loc[df_supersegger[str(feature)].notnull()]
            #convert degree to radian
            df_cp = -(df_cp+90) * np.pi / 180
            df_fast = -(df_fast) * np.pi / 180
            df_oufti = -(df_oufti) * np.pi / 180
            df_supersegger = -(df_supersegger) * np.pi / 180
            # for delta
            num_cells = df_delta.shape[0]
            for cell_indx in range(num_cells):
                if df_delta.iloc[cell_indx]["width"] > df_delta.iloc[cell_indx]["height"] :
                    df_delta.iloc[cell_indx][str(feature)] = (df_delta.iloc[cell_indx][str(feature)]) * np.pi / 180
                else:
                    df_delta.iloc[cell_indx][str(feature)] = (df_delta.iloc[cell_indx][str(feature)]+90) * np.pi / 180                
            df_delta = df_delta[str(feature)]
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
                    plot_x_lable[plot_titles[feature]],
                    'Number of Objects'
            )
            plot_subplots(
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
                    plot_x_lable[plot_titles[feature]],
                    'Number of Objects'
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
        "E.coli_mono_agarose",
        "SuperSegger sample images set"
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
            "birthLength": "Birth length distribution",
            "LifeHistory": "distribution of life history for each object",
            "GrowthRate": "distribution of growth rate",
            "AverageVelocity": "Velocity of bacteria in their life history",
            "AverageLength": "distribution of length in life history",
        },
        "feature_lineage_based": {
            "NumberOfDivision": "Detected divisions in object lineage"
        },
        "feature_bac_feature": {
            "Orientation": "Orientation of bacteria in each time step "
        },
        "feature_timeStep_based": {
            "NumberOfCells": "Number of objects in each time step"
        },
    }

    plot_x_lable = {"Birth length distribution": "Length (Pixel)",
                    "distribution of life history for each object": "Life History",
                    "distribution of growth rate": "Growth Rate",
                    "Velocity of bacteria in their life history":"velocity",
                    "distribution of length in life history": "Length (Pixel)",
                    "Detected divisions in object lineage": "Number of detected divisions",
                    "Orientation of bacteria in each time step ": "Orientation (radian)"}

    # end of file names
    end_of_file_names = {
        "features_lifehistory_based": "LifeHistory_based_Analysis",
        "feature_lineage_based": "lineage_based_analysis",
        "feature_bac_feature": "bacteria_feature_analysis",
        "feature_timeStep_based": "Num_cells_in_each_timeStep",
    }
    Tools_name = ["CellProfiler", "DeLTA", "FAST", "Oufti", "SuperSegger"]

    # timestep_based
    timestep_based_distribution(
        features["feature_timeStep_based"],
        end_of_file_names["feature_timeStep_based"],
        Tools_name,
        datasets,
        main_directories,
        plot_titles["feature_timeStep_based"],
    )

    # lineage based feature
    lineage_based_distribution(
        features["feature_lineage_based"],
        end_of_file_names["feature_lineage_based"],
        Tools_name,
        datasets,
        main_directories,
        plot_titles["feature_lineage_based"],
        plot_x_lable
    )

    # bac_feature
    bac_feature_distribution(
        features["feature_bac_feature"],
        end_of_file_names["feature_bac_feature"],
        Tools_name,
        datasets,
        main_directories,
        plot_titles["feature_bac_feature"],
        plot_x_lable
    )

    # life history based distribution
    life_history_based_distribution(
        features["features_lifehistory_based"],
        end_of_file_names["features_lifehistory_based"],
        Tools_name,
        datasets,
        main_directories,
        plot_titles["features_lifehistory_based"],
        plot_x_lable
    )

