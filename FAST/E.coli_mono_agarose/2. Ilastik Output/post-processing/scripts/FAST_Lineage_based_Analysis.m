
load('../../Tracks.mat','procTracks');

cellNumber=length(procTracks);

%based on linedivision
lable=[];
last_lable_value=0;
num_division = [];
lable_for_final_table = [];
cell_id = [];
mother_id = [];

for i=1:cellNumber
    cell_id (end + 1) = i;
    if isempty(procTracks(i).M)==1
        mother_id(end+1) = 0;
        last_lable_value=last_lable_value+1;
        lable_value=last_lable_value;
    else
        parent_id=procTracks(i).M;
        mother_id(end+1) = parent_id;
        lable_indx = find(cell_id==parent_id);
        lable_value=lable(lable_indx);
    end
    %save Results
    %append to list
    lable(end+1)=lable_value;
end

%add to table
T = table(transpose(cell_id),transpose(lable),transpose(mother_id));
%add column name
% ,'NumberOfDivision'
T.Properties.VariableNames={'Cell_id','Cell_lable','mother_id'};

unique_lable = unique(lable);
for element_indx = 1 : length(unique_lable)
    
    Table = T(T.Cell_lable == unique_lable(element_indx), :);
    num_division_val = length(unique(Table.mother_id))-1;
    num_division (end + 1) = num_division_val;
    lable_for_final_table (end+1) = unique_lable(element_indx);
end

%add to table
T2 = table(transpose(lable_for_final_table),transpose(num_division));
%add column name
T2.Properties.VariableNames={'Cell_lable','NumberOfDivision'};

% write to csv
writetable(T2,'../results/FAST_Lineage_based_Analysis.csv','Delimiter',',','QuoteStrings',true)

