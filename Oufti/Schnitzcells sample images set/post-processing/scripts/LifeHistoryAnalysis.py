import numpy as np
import pandas as pd


def AverageGrowthRate(divisionLength, birthLength, LifeHistoryLength, interval_Time):

    if LifeHistoryLength >= 2:
        t = LifeHistoryLength * interval_Time
        elongation_rate = round((np.log(divisionLength) - np.log(birthLength)) / t, 3)
    else:
        elongation_rate = 0

    return elongation_rate


def Average_Velocity(pos1, pos2, LifeHistoryLength, interval_Time):

    x1 = np.sqrt(pos1["Center_X"] ** 2 + pos1["Center_Y"] ** 2)
    x2 = np.sqrt(pos2["Center_X"] ** 2 + pos2["Center_Y"] ** 2)

    average_velocity = round((x2 - x1) / (LifeHistoryLength * interval_Time), 3)

    return average_velocity


def life_history_based_features(df, interval_Time):
    unique_id = list(set(df["CellId"].values))
    result_dict = {
        "CellId": [],
        "birthLength": [],
        "AverageLength": [],
        "AverageVelocity": [],
        "LifeHistory": [],
        "GrowthRate": [],
    }

    for indx in unique_id:
        df_lifeHistory = df.loc[df["CellId"] == indx]

        # lifeHistory
        LifeHistoryLength = df_lifeHistory.shape[0]
        # mean Length
        meanLength = np.mean(df_lifeHistory["MajorAxisLength"].values)

        # Average Velocity
        pos1 = df_lifeHistory.iloc[0][["Center_X", "Center_Y"]]
        pos2 = df_lifeHistory.iloc[-1][["Center_X", "Center_Y"]]
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
        result_dict["birthLength"].append(birth_length)
        result_dict["AverageLength"].append(meanLength)
        result_dict["AverageVelocity"].append(average_velocity)
        result_dict["LifeHistory"].append(LifeHistoryLength)
        result_dict["GrowthRate"].append(growth_rate)

    results = pd.DataFrame.from_dict(result_dict, orient="index").transpose()
    return results
