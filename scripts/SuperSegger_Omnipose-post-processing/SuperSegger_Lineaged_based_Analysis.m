function label = SuperSegger_Lineaged_based_Analysis(ss_output_directory, write_directory)
%SuperSegger_Lineaged_based_Analysis Performs lineage analysis on SuperSegger output.
%
%   label = SuperSegger_Lineaged_based_Analysis(ss_output_directory, write_directory) 
%   takes the output directory from SuperSegger and the desired directory 
%   to write results. It performs a lineage analysis and returns the label of 
%   each cell and writes the lineage-based analysis to a CSV file.
%
%   INPUTS:
%   ss_output_directory - Directory path where SuperSegger's output files (like clist.mat) are located.
%   write_directory - The directory path where the output CSV file will be stored.
%
%   OUTPUTS:
%   label - An array containing the label of each cell.

% Load the clist.mat file from SuperSegger's output directory
load(strcat(ss_output_directory, '/xy1/clist.mat'), 'data');

% Initialize variables
cellNumber = size(data, 1);                  % Total number of cells
cell_id = zeros(1, cellNumber);              % Store each cell's ID
label = zeros(1, cellNumber);                % Store label of each cell
last_label_value = 0;                        % Track the last assigned label value
num_division = [];                           % Number of divisions for each lineage
label_for_final_table = [];                  % Labels to be used in the final table

% Process each cell to determine lineage
for i = 1:cellNumber
    cell_id(i) = data(i, 1);  % Cell ID from the clist.mat file
    
    % Check if the cell has a mother (Mother ID from column 61)
    if data(i, 61) == 0
        last_label_value = last_label_value + 1;
        label_value = last_label_value;
    else
        parent_id = data(i, 61);
        label_indx = find(cell_id == parent_id);
        label_value = label(label_indx);
    end
    
    label(i) = label_value;  % Save the cell's lineage label
end

% Create a table of cell ID, their lineage label, and mother ID
T = table(data(:, 1), transpose(label), data(:, 61));
T.Properties.VariableNames = {'Cell_id', 'Cell_label', 'mother_id'};

% Analyze the number of divisions for each unique lineage label
unique_labels = unique(label);
for element_indx = 1:length(unique_labels)
    family_tree_label = unique_labels(element_indx);
    Table = T(T.Cell_label == family_tree_label, :);
    
    if height(Table) > 1
        num_division_val = length(unique(Table.mother_id)) - 1;
        num_division(end + 1) = num_division_val;
        label_for_final_table(end+1) = family_tree_label;        
    else
        num_division(end + 1) = 0; % No division
        label_for_final_table(end+1) = family_tree_label;        
    end
end

% Create a table of lineage labels and their corresponding number of divisions
T2 = table(transpose(label_for_final_table), transpose(num_division));
T2.Properties.VariableNames = {'Cell_label', 'NumberOfDivision'};

% Write the results to a CSV file
writetable(T2, strcat(write_directory, '/SuperSegger_lineage_based_analysis.csv'), ...
           'Delimiter', ',', 'QuoteStrings', true);

end
