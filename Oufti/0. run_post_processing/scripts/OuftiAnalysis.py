import csv
import pandas as pd
from LifeHistoryAnalysis import life_history_based_features
from LineageAnalysis import lineage_based_features


if __name__ == "__main__":

# ,'E.coli_chamber',
    datasets = ['E.coli_mono_agarose','E.coli_mono_agarose_noisy','Pseudomonas_agarose','SuperSegger sample images set','Xanthomonase_agarose',
                'Xanthomonase_chamber','E.coli_mono_agarose_skipTimeSteps','Pseudomonas_chamber'];
    modes = ['2. Ilastik Output','1. Raw Images'];
    #1.5,
    interval_time = [1.5,1.5,1,1.5,1.5,1.5,15,1.5];

    for i , dataset in enumerate(datasets):
        for mode in modes:
            input_file = "../../"+dataset+"/"+mode+"/post-processing/results/Oufti_bacteria_feature_analysis.csv"
            interval_time_value = interval_time[i]
            output_directory = "../../"+dataset+"/"+mode+"/post-processing/results/"
            print("dataset:" + dataset)
            print("mode: "+mode)
            print("interval time: "+str(interval_time_value))
            if mode == '2. Ilastik Output':
                if dataset != 'E.coli_mono_agarose_noisy':
                    # Parsing bacteria features
                    df = pd.read_csv(input_file)
                    # calculation of life history based features
                    life_history_based_results = life_history_based_features(df, interval_time_value)
                    # calculation of lineage based features
                    lineage_based_results = lineage_based_features(df)
                    # write to csv
                    # life history based features
                    path_lifehistory = "../../"+dataset+"/"+mode+"/post-processing/results/Oufti_LifeHistory_based_Analysis"
                    life_history_based_results.to_csv(path_lifehistory + ".csv", index=False)
                    # lineage based features
                    path_lineage = "../../"+dataset+"/"+mode+"/post-processing/results/Oufti_lineage_based_analysis"
                    lineage_based_results.to_csv(path_lineage + ".csv", index=False)
            else:
                if dataset != 'E.coli_mono_agarose_skipTimeSteps':
                    # Parsing bacteria features
                    df = pd.read_csv(input_file)
                    # calculation of life history based features
                    life_history_based_results = life_history_based_features(df, interval_time_value)
                    # calculation of lineage based features
                    lineage_based_results = lineage_based_features(df)
                    # write to csv
                    # life history based features
                    path_lifehistory = "../../"+dataset+"/"+mode+"/post-processing/results/Oufti_LifeHistory_based_Analysis"
                    life_history_based_results.to_csv(path_lifehistory + ".csv", index=False)
                    # lineage based features
                    path_lineage = "../../"+dataset+"/"+mode+"/post-processing/results/Oufti_lineage_based_analysis"
                    lineage_based_results.to_csv(path_lineage + ".csv", index=False)

