
load('../MonoCulture/results/Position000000.mat','res');

cellNumber=length(res{1}.lineage);

%based on linedivision
lable=[];
division=[];
NumDivision=[];
last_lable_value=0;
dict1=containers.Map(0,0);

for i=1:cellNumber
    if res{1}.lineage{i}.mother==0
        division_value=0;
        last_lable_value=last_lable_value+1;
        lable_value=last_lable_value;
    else
        parent=res{1}.lineage{i}.mother;
        lable_value=lable(parent);
        division_value=division(parent)+1;
    end
    dict1(lable_value)=division_value;
    %save Results
    %append to list
    lable(length(lable)+1)=lable_value;
    division(length(division)+1)=division_value;
    
end


%add to table
T = table(transpose(dict1.keys),transpose(dict1.values));
%add column name
T.Properties.VariableNames={'CellLiniedivision','NumberOfDivision'};

% write to csv
writetable(T,'results/DeLTA_DivisionAnalysis.csv','Delimiter',',','QuoteStrings',true)

