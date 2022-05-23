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
        result_dict["lable"].append(lable)
        result_dict["NumberOfDivision"].append(division_df.shape[0])
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


def ProcessData(input_file, interval_time, growth_rate_method="Average"):

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
        dataFrame, interval_time, growth_rate_method
    )
    lineage_based_analysis_results = lineage_based_analysis(df)
    Num_cells_in_each_timeStep_results = Num_cells_in_each_timeStep(df)

    # write to csv
    path_lifehistory = "../results/CP_LifeHistory_based_Analysis"
    path_lineage = "../results/CP_lineage_based_analysis"
    path_bacteria_based_features = "../results/CP_bacteria_feature_analysis"
    path_Num_cells_in_each_timeStep = "../results/CP_Num_cells_in_each_timeStep"

    life_history_based_analysis.to_csv(path_lifehistory + ".csv", index=False)
    lineage_based_analysis_results.to_csv(path_lineage + ".csv", index=False)
    df.to_csv(path_bacteria_based_features + ".csv", index=False)
    Num_cells_in_each_timeStep_results.to_csv(
        path_Num_cells_in_each_timeStep + ".csv", index=False
    )


if __name__ == "__main__":
    input_file = "../../4. CP outputs/MyExpt_IdentifySecondaryObjects.csv"
    interval_time = 1
    ProcessData(input_file, interval_time)
