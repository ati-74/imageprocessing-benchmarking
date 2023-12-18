function label = FAST_Lineaged_based_Analysis(FAST_output_directory, write_directory)
%FAST_Lineaged_based_Analysis Labels bacterial lineage based on mother cell IDs
%
% This function performs lineage-based analysis of bacterial cells using
% the FAST output, which contains mother cell IDs. It assigns a unique label
% to each family tree of bacteria. Additionally, it counts the number of
% divisions in each lineage and outputs the results as a CSV file.
%
% Inputs:
%   FAST_output_directory: The directory containing the FAST output.
%   write_directory: The directory to which the results will be written.
%
% Output:
%   label: A vector containing lineage labels for each bacterial cell.

% Load the processed tracks from the FAST output
load(strcat(FAST_output_directory,'/Tracks.mat'), 'procTracks');

% Initialize various arrays and values for processing
cellNumber = size(procTracks, 2);            % number of cells
cell_id = zeros(1, cellNumber);              % id of bacteria
label = zeros(1, cellNumber);                % store label of bacteria
mother_id = zeros(1, cellNumber);            % mother id
last_label_value = 0;                        % last label that was assigned to a bacteria
num_division = [];                           % number of division in each lineage
label_for_final_table = [];                  % used for creating the final table

% Assign labels based on mother IDs
for i = 1:cellNumber
    cell_id(i) = i;

    % Column 61 of clist.mat file contains the Mother ID
    if isempty(procTracks(i).M) == 1
        last_label_value = last_label_value + 1;
        label_value = last_label_value;
        mother_id(i) = 0;
    else
        parent_id = procTracks(i).M;
        label_indx = find(cell_id == parent_id);
        
        if isempty(label_indx)
            last_label_value = last_label_value + 1;
            label_value = last_label_value;
            mother_id(i) = 0;    
        else
            label_value = label(label_indx);
            mother_id(i) = parent_id;
        end
    end
    label(i) = label_value; % Save results
end

% Create a table with cell ID, label, and mother ID
T = table(transpose(cell_id), transpose(label), transpose(mother_id));
T.Properties.VariableNames = {'Cell_id', 'Cell_label', 'mother_id'};

% Calculate the number of divisions in each lineage
unique_labels = unique(label);
for element_indx = 1:length(unique_labels)
    family_tree_label = unique_labels(element_indx);
    Table = T(T.Cell_label == family_tree_label, :);

    if height(Table) > 1
        num_division_val = length(unique(Table.mother_id)) - 1;
        num_division(end + 1) = num_division_val;
        label_for_final_table(end+1) = family_tree_label;
    else
        num_division(end + 1) = 0;
        label_for_final_table(end+1) = family_tree_label;
    end
end

% Create a table with the number of divisions
T2 = table(transpose(label_for_final_table), transpose(num_division));
T2.Properties.VariableNames = {'Cell_lable', 'NumberOfDivision'};

% Write the table to a CSV file
writetable(T2, strcat(write_directory, '/FAST_lineage_based_analysis.csv'), 'Delimiter', ',', 'QuoteStrings', true);

end
