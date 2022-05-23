import pandas as pd


def lineage_based_features(df):
    unique_lables = list(set(df["lable"].values))
    result_dict = {
        "lable": [],
        "NumberOfDivision": [],
    }

    for lable in unique_lables:
        df_lineage = df.loc[df["lable"] == lable]
        # number of division
        num_division = len(list(set(df_lineage["parent"].values))) - 1
        result_dict["lable"].append(lable)
        result_dict["NumberOfDivision"].append(num_division)
        # Division-centred average

    results = pd.DataFrame.from_dict(result_dict, orient="index").transpose()
    return results
