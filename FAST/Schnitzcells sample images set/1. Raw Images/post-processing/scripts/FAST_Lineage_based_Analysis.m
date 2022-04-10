
load('../../Tracks.mat','procTracks');

cellNumber=length(procTracks);

%based on linedivision
lable=[];
division=[];
NumDivision=[];
last_lable_value=0;
dict1=containers.Map(0,0);

for i=1:cellNumber
    if isempty(procTracks(i).M)==1
        division_value=0;
        last_lable_value=last_lable_value+1;
        lable_value=last_lable_value;
    else
        parent=procTracks(i).M;
        lable_value=lable(parent);
        division_value=division(parent)+1;
    end
    dict1(lable_value)=division_value;
    %save Results
    %append to list
    lable(length(lable)+1)=lable_value;
    division(length(division)+1)=division_value;
    
end

remove(dict1,0)
%add to table
T = table(transpose(dict1.keys),transpose(dict1.values));
%add column name
T.Properties.VariableNames={'Cell_lable','NumberOfDivision'};

% write to csv
writetable(T,'../results/FAST_Lineage_based_Analysis.csv','Delimiter',',','QuoteStrings',true)

