import csv
import pandas as pd
from LifeHistoryAnalysis import life_history_based_features
from LineageAnalysis import lineage_based_features


if __name__ == "__main__":
    # csv file
    input_file = "../results/Oufti_bacteria_feature_analysis.csv"
    # interval time
    interval_Time = 1

    # Parsing bacteria features
    df = pd.read_csv(input_file)
    # calculation of life history based features
    life_history_based_results = life_history_based_features(df, interval_Time)
    # calculation of lineage based features
    lineage_based_results = lineage_based_features(df)

    # write to csv
    # life history based features
    path_lifehistory = "../results/Oufti_LifeHistory_based_Analysis"
    life_history_based_results.to_csv(path_lifehistory + ".csv", index=False)
    # lineage based features
    path_lineage = "../results/Oufti_lineage_based_analysis"
    lineage_based_results.to_csv(path_lineage + ".csv", index=False)
