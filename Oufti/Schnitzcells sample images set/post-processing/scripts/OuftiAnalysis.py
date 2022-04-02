import csv
import pandas as pd
import numpy as np
import math


def AverageGrowthRate(divisionLength, birthLength, LifeHistoryLength, interval_Time):

    if LifeHistoryLength >= 2:
        t = LifeHistoryLength * interval_Time
        elongation_rate = round(
            (math.log(divisionLength) - math.log(birthLength)) / t, 3
        )
    else:
        elongation_rate = 0

    return elongation_rate


def Average_Velocity(pos1, pos2, LifeHistoryLength, interval_Time):

    x1 = math.sqrt(pos1["x_center"] ** 2 + pos1["y_center"] ** 2)
    x2 = math.sqrt(pos2["x_center"] ** 2 + pos2["y_center"] ** 2)

    average_velocity = round((x2 - x1) / (LifeHistoryLength * interval_Time), 3)

    return average_velocity


def ProcessData(df, interval_Time):
    unique_id = list(set(df["CellId"].values))
    result_dict = {
        "CellId": [],
        "birth Length": [],
        "Last Length": [],
        "AverageLength": [],
        "AverageOrientation": [],
        "AverageVelocity": [],
        "LifeHistory": [],
        "growth rate": [],
    }

    for indx in unique_id:
        df_lifeHistory = df.loc[df["CellId"] == indx]

        # lifeHistory
        LifeHistoryLength = df_lifeHistory.shape[0]
        # mean Length
        meanLength = np.mean(df_lifeHistory["MajorAxisLength"].values)
        # mean orientation
        meanOrientation = np.mean(df_lifeHistory["Orientation"].values)

        # Average Velocity
        pos1 = df_lifeHistory.iloc[0][["x_center", "y_center"]]
        pos2 = df_lifeHistory.iloc[-1][["x_center", "y_center"]]
        average_velocity = Average_Velocity(
            pos1, pos2, LifeHistoryLength, interval_Time
        )

        # growth rate
        birth_length = df_lifeHistory.iloc[0]["MajorAxisLength"]
        division_length = df_lifeHistory.iloc[-1]["MajorAxisLength"]
        growth_rate = AverageGrowthRate(
            division_length, birth_length, LifeHistoryLength, interval_Time
        )

        # store results
        result_dict["CellId"].append(indx)
        result_dict["birth Length"].append(birth_length)
        result_dict["Last Length"].append(division_length)
        result_dict["AverageLength"].append(meanLength)
        result_dict["AverageOrientation"].append(meanOrientation)
        result_dict["AverageVelocity"].append(average_velocity)
        result_dict["LifeHistory"].append(LifeHistoryLength)
        result_dict["growth rate"].append(growth_rate)

    results = pd.DataFrame.from_dict(result_dict, orient="index").transpose()
    return results


if __name__ == "__main__":
    # csv file
    input_file = "../results/OuftiResults.csv"
    # interval time
    interval_Time = 1

    # Parsing Oufti Results
    df = pd.read_csv(input_file)
    results = ProcessData(df, interval_Time)
    print(results)

    # write to csv
    path = "../results/OuftiAnalysis"
    results.to_csv(path + ".csv", index=False)
