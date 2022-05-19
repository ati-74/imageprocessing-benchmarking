import csv
import pandas as pd
import numpy as np
import os
from ExperimentalDataProcessing import BacteriaAnalysis


def lineage_based_analysis(df):
    uniq_lable = list(set(df["lable"].values))
    result_dict = {
        "lable": [],
        "NumberOfDivision": [],
    }
    for lable in uniq_lable:
        df_current_lable = df.loc[df["lable"] == lable]
        division_df = df_current_lable.loc[df_current_lable["divideFlag"] == True]
        # save results
        if division_df.shape[0]>1:
            result_dict["NumberOfDivision"].append(division_df.shape[0])
        else:
            result_dict["NumberOfDivision"].append("NaN")
        result_dict["lable"].append(lable)
        
    # rename some columns
    results = pd.DataFrame.from_dict(result_dict, orient="index").transpose()
    return results


def Num_cells_in_each_timeStep(df):
    uniq_timeSteps = list(set(df["TimeStep"].values))
    result_dict = {
        "TimeStep": [],
        "NumberOfCells": [],
    }
    for timestep in uniq_timeSteps:
        df_current_timestep = df.loc[df["TimeStep"] == timestep]
        # save results
        result_dict["TimeStep"].append(timestep)
        result_dict["NumberOfCells"].append(df_current_timestep.shape[0])
    # rename some columns
    results = pd.DataFrame.from_dict(result_dict, orient="index").transpose()
    return results


def ProcessData(input_file, interval_time,output_directory):

    # Parsing CellProfiler output
    dataFrame = pd.read_csv(input_file)
    # remove Nan lables and zero MajorAxisLength
    dataFrame = dataFrame.loc[
        (dataFrame["TrackObjects_Label_50"].notnull())
        & (dataFrame["AreaShape_MajorAxisLength"] != 0)
    ].reset_index(drop=True)
    dataFrame = dataFrame.reset_index(drop=True)

    # process the tracking data
    df, life_history_based_analysis = BacteriaAnalysis(
        dataFrame, interval_time
    )
    lineage_based_analysis_results = lineage_based_analysis(df)
    Num_cells_in_each_timeStep_results = Num_cells_in_each_timeStep(df)

    # write to csv
    path_lifehistory = output_directory+"CellProfiler_LifeHistory_based_Analysis"
    path_lineage = output_directory+"CellProfiler_lineage_based_analysis"
    path_bacteria_based_features = output_directory+"CellProfiler_bacteria_feature_analysis"
    path_Num_cells_in_each_timeStep = output_directory+"CellProfiler_Num_cells_in_each_timeStep"

    life_history_based_analysis.to_csv(path_lifehistory + ".csv", index=False)
    lineage_based_analysis_results.to_csv(path_lineage + ".csv", index=False)
    df.to_csv(path_bacteria_based_features + ".csv", index=False)
    Num_cells_in_each_timeStep_results.to_csv(
        path_Num_cells_in_each_timeStep + ".csv", index=False
    )


if __name__ == "__main__":

    datasets = ["E.coli_chamber","E.coli_mono_agarose","E.coli_mono_agarose_skipTimeSteps2","E.coli_mono_agarose_skipTimeSteps",
                "E.coli_mono_agarose_noisy","Pseudomonas_agarose","Pseudomonas_chamber",
                "SuperSegger sample images set","Xanthomonase_agarose","Xanthomonase_chamber"]
    modes = ['1. Raw Images','2. Ilastik Output']

    interval_time =[1.5, 1.5 , 30 ,15, 1.5, 1.5, 1.5, 1, 1.5, 1.5]

    for i , dataset in enumerate(datasets):
        for mode in modes:
            input_file = "../../"+dataset+"/"+mode+"/CP outputs/MyExpt_IdentifySecondaryObjects.csv"
            interval_time_value = interval_time[i]
            output_directory = "../../"+dataset+"/"+mode+"/post-processing/results/"
            print("dataset:" + dataset)
            print("interval time: "+str(interval_time_value))
            
            if mode == '1. Raw Images':
                if dataset != 'E.coli_mono_agarose_skipTimeSteps' and dataset !="E.coli_mono_agarose_skipTimeSteps2":
                        ProcessData(input_file, interval_time_value,output_directory)
                        ProcessData(input_file, interval_time_value,output_directory)
            else:
                if dataset != "E.coli_chamber" and dataset != "E.coli_mono_agarose_noisy":
                    ProcessData(input_file, interval_time_value,output_directory)








