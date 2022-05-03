
load('../../output/Position000000.mat','res');

TimeSteps = 203;

initiallycellNumber=length(res{1}.lineage);
cellId = [];

for i=1:initiallycellNumber
    valid_frames_index = find(res{1}.lineage{i}.frames <=TimeSteps);
    if isempty(valid_frames_index)==0
        cellId(end+1) = i;
    end
end

%based on linedivision
lable=[];
last_lable_value=0;
num_division = [];
lable_for_final_table = [];
cell_id = [];
mother_id = [];

cellNumber = length(cellId);

for i=1:cellNumber
    cell_id (end + 1) = cellId(i);
    if res{1}.lineage{cellId(i)}.mother==0
        last_lable_value=last_lable_value+1;
        lable_value=last_lable_value;
    else
        parent_id=res{1}.lineage{cellId(i)}.mother;
        lable_indx = find(cell_id==parent_id);
        lable_value=lable(lable_indx);
    end
    %save Results
    %append to list
    mother_id(end+1) = res{1}.lineage{cellId(i)}.mother;
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
writetable(T2,'../results/DeLTA_lineage_based_analysis.csv','Delimiter',',','QuoteStrings',true)

