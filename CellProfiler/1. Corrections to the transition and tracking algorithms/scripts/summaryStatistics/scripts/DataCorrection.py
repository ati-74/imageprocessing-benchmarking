import pandas as pd
import numpy as np


def lineageBacteriaAfterThisTimeStep(dataFrame, Bacteria):
    dataFrameOfLineage = dataFrame.loc[
        (dataFrame["TrackObjects_Label_50"] == Bacteria["TrackObjects_Label_50"])
        & (dataFrame["ImageNumber"] >= Bacteria["ImageNumber"])
    ]
    return dataFrameOfLineage


def divisionOccurrence(dataFrameOfLineage, Bacteria, Bacid):
    Parent_time_step_of_cell = Bacteria["ImageNumber"]
    Parent_index_of_cell = Bacteria["ObjectNumber"]
    division_occ = False
    lifehistoryIndex = []

    Bacteriaindex = Bacid
    lifehistoryIndex.append(Bacteriaindex)
    incorrectBacteriumIndex = 0
    LastTimeStep = dataFrameOfLineage["ImageNumber"].iloc[-1]

    while (division_occ == False) and (LastTimeStep != Parent_time_step_of_cell):
        reletive_Bacteria_in_next_timestep = dataFrameOfLineage.loc[
            (
                dataFrameOfLineage["TrackObjects_ParentImageNumber_50"]
                == Parent_time_step_of_cell
            )
            & (
                dataFrameOfLineage["TrackObjects_ParentObjectNumber_50"]
                == Parent_index_of_cell
            )
        ]

        Number_of_reletive_bacteria = reletive_Bacteria_in_next_timestep.shape[0]

        if Number_of_reletive_bacteria == 1:
            Parent_index_of_cell = reletive_Bacteria_in_next_timestep.iloc[0][
                "ObjectNumber"
            ]
            Parent_time_step_of_cell = reletive_Bacteria_in_next_timestep.iloc[0][
                "ImageNumber"
            ]
            Bacteriaindex = reletive_Bacteria_in_next_timestep.index.tolist()[0]
            lifehistoryIndex.append(Bacteriaindex)
        elif Number_of_reletive_bacteria == 2:
            division_occ = True
            last_timestep_before_division = Parent_time_step_of_cell

        elif Number_of_reletive_bacteria == 0:  # interupt
            last_timestep_before_division = Parent_time_step_of_cell
            break
        else:
            Length = reletive_Bacteria_in_next_timestep[
                "AreaShape_MajorAxisLength"
            ].values
            minLength = min(
                reletive_Bacteria_in_next_timestep["AreaShape_MajorAxisLength"].values
            )
            incorrectBacterium = np.where(Length == minLength)
            incorrectBacteriumIndex = reletive_Bacteria_in_next_timestep.index.values[
                incorrectBacterium
            ][0]
            division_occ = True
            last_timestep_before_division = Parent_time_step_of_cell
            print("Warning: Three cells are produced from a single cell!")
            print("Lable:" + str(dataFrameOfLineage["TrackObjects_Label_50"].iloc[0]))

    if division_occ == False and LastTimeStep == Parent_time_step_of_cell:
        last_timestep_before_division = dataFrameOfLineage["ImageNumber"].iloc[-1]

    division_status = {
        "division_occ": division_occ,
        "last_timestep_before_division": last_timestep_before_division,
        "lifeHistoryIndex": lifehistoryIndex,
        "incorrectBacteriumIndex": incorrectBacteriumIndex,
    }

    return division_status


def LifeHistory(dataFrameOfLineage, lifehistoryIndex):
    dfLifehistory = dataFrameOfLineage.loc[lifehistoryIndex]

    return dfLifehistory


def SameIdBacteria(dataFrame, id_of_bacteria):
    dataFrameOfSameBacteria = dataFrame.loc[dataFrame["id"] == id_of_bacteria]
    SameBacteriaIndex = dataFrameOfSameBacteria.index.tolist()
    return SameBacteriaIndex


def incorrect_df(dataFrame):
    dataFrame = dataFrame.loc[dataFrame["drop"] == True].reset_index(drop=True)
    return dataFrame


def dropIndex(dataFrame):
    dataFrame = dataFrame.loc[dataFrame["drop"] == False].reset_index(drop=True)
    return dataFrame


def finding_incorrect_bacteria(dataFrame):
    dataFrame["checked"] = ""
    dataFrame["drop"] = False

    # remove Nan lables and zero MajorAxisLength
    nan_zero_bac = dataFrame.loc[
        (dataFrame["TrackObjects_Label_50"].isnull())
        | (dataFrame["AreaShape_MajorAxisLength"] == 0)
    ]

    # correct data
    dataFrame = dataFrame.loc[
        (dataFrame["TrackObjects_Label_50"].notnull())
        & (dataFrame["AreaShape_MajorAxisLength"] != 0)
    ]

    for index, row in dataFrame.iterrows():
        if not dataFrame.iloc[index]["checked"]:
            dataFrameOfLineage = lineageBacteriaAfterThisTimeStep(dataFrame, row)

            division_status = divisionOccurrence(dataFrameOfLineage, row, index)

            if division_status["incorrectBacteriumIndex"] != 0:
                drop_index = division_status["incorrectBacteriumIndex"]
                dataFrame.at[drop_index, "drop"] = True

            dfLifehistory = LifeHistory(
                dataFrameOfLineage, division_status["lifeHistoryIndex"]
            )
            LifehistoryIndex = dfLifehistory.index.tolist()

            if dataFrame.iloc[index]["drop"] == True:
                for idx in LifehistoryIndex:
                    dataFrame.at[idx, "drop"] = True
                    dataFrame.at[idx, "checked"] = True
            else:
                for idx in LifehistoryIndex:
                    dataFrame.at[idx, "checked"] = True

            if division_status["division_occ"]:
                lastTimeStepOfBacteria = LifehistoryIndex[-1]
                # duaghters
                divisionTime = division_status["last_timestep_before_division"] + 1
                dataFrameOfdaughters = dataFrameOfLineage.loc[
                    (dataFrameOfLineage["ImageNumber"] == divisionTime)
                ]
                daughterIndex = dataFrameOfdaughters.index.tolist()
                for daughetridx in daughterIndex:
                    if dataFrame.iloc[index]["drop"] == True:
                        dataFrame.at[daughetridx, "drop"] = True

    dataFrame_incorrect = incorrect_df(dataFrame)
    # correct bacteria
    df_correct = dropIndex(dataFrame)
    # get specific columns
    dataFrame_incorrect = dataFrame_incorrect[["ImageNumber", "ObjectNumber"]]
    nan_zero_bac = nan_zero_bac[["ImageNumber", "ObjectNumber"]]
    # merge dataframes
    df_incorrect = pd.concat([dataFrame_incorrect, nan_zero_bac], axis=0)
    return df_incorrect, df_correct
