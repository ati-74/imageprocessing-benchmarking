import os
import networkx as nx
import pandas as pd
import numpy as np
import pickle
from ConnectedComponents import edge_list_to_adjmatrix, plot_graph
from DataCorrection import finding_incorrect_bacteria
from aspect_ratio import aspect_ratio_calc, aspect_plot
from anisotropy import Anisotropy_calc


def drop_incorrect_bac(adjmatrix, incorrect_bac_in_current_time_step):
    """
    Goal: some bacteria are detected wrongly by CP, so that we stored them (by the function
    called "finding_incorrect_bacteria"). What "drop_incorrect_bac" does is removing
    incorrect bacteria from adjacancy matrix. 
    
    @param adjmatrix                            data frame   adjacency matrix of the current time-step
    @param incorrect_bac_in_current_time_step   data frame   "ImageNumber", "ObjectNumber" of incrorrect bac. in current time-step
    """
    
    incorrect_index = incorrect_bac_in_current_time_step["ObjectNumber"].values
    # remove rows
    adjmatrix.drop(incorrect_index, axis=0, inplace=True)
    # remove columns
    adjmatrix.drop(incorrect_index, axis=1, inplace=True)
    return adjmatrix


def finding_subgraphs(graph):
  """
    Goal: Finding largest disconnected subgraphsba

    @param graph   graph  neighboring bacteria graph in current time-step
    """
  subgraphs = sorted(nx.connected_components(graph), key=len, reverse=True)
  return subgraphs


def CreatePickleFiles(df, TimeStep, num_microcolonies, path):
    data = {}
    data["stepNum"] = TimeStep
    data["numMicrocolonies"] = num_microcolonies
    data["microcolonyStates"] = df
    WrtiteToPickleFile(data, path, TimeStep)


def WrtiteToPickleFile(data, path, time_step):

    output_file = path + "/pickle/step-" + str(time_step) + ".pickle"

    with open(output_file, "wb") as export:
        pickle.dump(data, export, protocol=-1)


def microcolony_analysis(
    cells_info_file, neighbor_file, output_directory, summary_statistic_method
):
  """
    Goal: this is the main function; the function calls other function that are described above and
    calculates aspect ratio for each microcolony in each time-step and store the outputs in png format and pickle.

    @param cells_info_file            dataframe  all the required information of bac. like id, orientation,etc.
    @param neighbor_file              dataframe  object ralationship file that contains info. about each cell's neghibor.
    @param summary_statistic_method   string     the method that we apply on the micro-colonies
    
    """
  min_size_of_micro_colony = 2
  # read cells informations
  cell_information_df = pd.read_csv(cells_info_file)
  # finding incorrect bacteria
  df_incorrect, df_correct = finding_incorrect_bacteria(cell_information_df)

  # read neighbor file
  neighbor_df = pd.read_csv(neighbor_file)
  # filter `MeasureObjectNeighbors` module rows
  neighbor_df = neighbor_df.loc[neighbor_df["Module"] == "MeasureObjectNeighbors"]

  # In order to identify merged microcolonies, microcolony labels are stored.
  microcolonies = []
  Timesteps = list(set(df_correct["ImageNumber"].values))
  for TimeStep in Timesteps:
        # cells information in current time step
        df_current_time_step = df_correct.loc[df_correct["ImageNumber"] == TimeStep]
        # second image number is not checked because the neighborhood relationship is
        # a time-step to time-step relationship.
        edge_df = neighbor_df.loc[neighbor_df["First Image Number"] == TimeStep]
        adjmatrix = edge_list_to_adjmatrix(
            edge_df["First Object Number"], edge_df["Second Object Number"]
        )
        # find and remove incorrect bacteria in current time step from adjancy matrix
        incorrect_bac_in_current_time_step = df_incorrect.loc[
            df_incorrect["ImageNumber"] == TimeStep
        ]
        if not incorrect_bac_in_current_time_step.empty:
            adjmatrix = drop_incorrect_bac(
                adjmatrix, incorrect_bac_in_current_time_step
            )
        # makeing graph
        G = nx.from_pandas_adjacency(adjmatrix)
        # finding subgraphs
        subgraphs = finding_subgraphs(G)
        # store ellipses
        ellipses = []
        # create an empty DataFrame to store results in each timesteps
        microcolonies_info_current_time_step_df = pd.DataFrame(
            columns=["Object Numbers", "Aspect Ratio", "Anisotropy"]
        )

        for subgraph in subgraphs:
            if len(subgraph) >= min_size_of_micro_colony:
                nodes = list(subgraph)
                # find unique bacteria lables
                bacteria_lable = list(
                    set(
                        df_current_time_step[
                            df_current_time_step["ObjectNumber"].isin(nodes)
                        ]["TrackObjects_Label_50"].values.tolist()
                    )
                )
                # check microcolony
                common_index = []
                for indx, microcolony in enumerate(microcolonies):
                    common_elements = list(
                        set(microcolony).intersection(bacteria_lable)
                    )
                    if common_elements:
                        common_index.append(indx)

                if (
                    len(common_index) <= 1
                ):  # As a result, the microcolonies were not merged
                    # Add new labels to its microcolony list
                    if common_index:
                        microcolonies[common_index[0]].extend(bacteria_lable)
                        microcolonies[common_index[0]] = list(
                            set(microcolonies[common_index[0]])
                        )
                    else:
                        microcolonies.append(bacteria_lable)
                    # bacteri in this microcolony
                    bac_in_microcolony = df_current_time_step[
                        df_current_time_step["ObjectNumber"].isin(nodes)
                    ]
                    """
                        calculation of aspect ratio
                    """
                    if summary_statistic_method == "Aspect Ratio":
                        ellipse_params, aspect_ratio = aspect_ratio_calc(
                            bac_in_microcolony
                        )
                        # append ellipse
                        ellipses.append(ellipse_params)
                        # append row to microcolonies_info_current_time_step DataFrame
                        new_row_index = microcolonies_info_current_time_step_df.shape[0]
                        microcolonies_info_current_time_step_df.loc[new_row_index] = [
                            nodes,
                            aspect_ratio,
                            "",
                        ]
                    """
                        Finish
                    """


                    """
                        calculation of Anisotropy
                    """
                    if summary_statistic_method == "Anisotropy":
                        ellipse_params, mean_anisotropy = Anisotropy_calc(
                            bac_in_microcolony
                        )
                        # append ellipse
                        ellipses.append(ellipse_params)
                        # append row to microcolonies_info_current_time_step DataFrame
                        new_row_index = microcolonies_info_current_time_step_df.shape[0]
                        microcolonies_info_current_time_step_df.loc[new_row_index] = [
                            nodes,
                            "",
                            mean_anisotropy,
                        ]
                    """
                        Finish
                    """

                    

        """                
            draw aspect ratio plot
        """
        if summary_statistic_method == "Aspect Ratio":
            aspect_plot(df_current_time_step, ellipses, TimeStep, output_directory)
        """
            Finish
        """

        # plot graph
        plot_graph(G, TimeStep, output_directory)

        # save microcolonies information
        CreatePickleFiles(
            microcolonies_info_current_time_step_df,
            TimeStep,
            len(ellipses),
            output_directory,
        )


def ProcessData(
    input_file, relationship_file, output_directory_path, summary_statistic_method
):
    aspect_ratio_images_path = (
        output_directory_path + "/img/" + summary_statistic_method + "/"
    )
    graph_images_path = output_directory_path + "/img/graph/"
    pickle_path = output_directory_path + "/pickle/"

    if not os.path.exists(aspect_ratio_images_path):
        os.makedirs(aspect_ratio_images_path)
    if not os.path.exists(graph_images_path):
        os.makedirs(graph_images_path)
    if not os.path.exists(pickle_path):
        os.makedirs(pickle_path)
    # start analysis
    microcolony_analysis(
        input_file, relationship_file, output_directory_path, summary_statistic_method
    )
