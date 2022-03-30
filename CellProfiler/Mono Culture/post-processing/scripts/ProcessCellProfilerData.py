import csv
import pandas as pd
import numpy as np
import os
from ExperimentalDataProcessing import BacteriaAnalysis


def ProcessData(input_file, interval_time=1, growth_rate_method="Average"):

    # Parsing CellProfiler output
    dataFrame = pd.read_csv(input_file)
    # remove Nan lables and zero MajorAxisLength
    dataFrame = dataFrame.loc[
        (dataFrame["TrackObjects_Label_50"] != "nan")
        & (dataFrame["AreaShape_MajorAxisLength"] != 0)
    ]
    dataFrame = dataFrame.reset_index(drop=True)

    # process the tracking data
    processed_data = BacteriaAnalysis(dataFrame, interval_time, growth_rate_method)

    # write to csv
    path = "../results/CPAnalysis"
    processed_data.to_csv(path + ".csv", index=False)


if __name__ == "__main__":
    input_file = (
        "../../4. CP outputs/MyExpt_IdentifySecondaryObjects - remove - Nan Lable.csv"
    )
    interval_time = 1.5
    ProcessData(input_file, interval_time)
