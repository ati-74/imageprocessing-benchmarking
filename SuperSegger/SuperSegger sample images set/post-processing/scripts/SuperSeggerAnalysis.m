
load('../../xy1/clist.mat','data');
load('../../xy1/clist.mat','def');

cellNumber=length(data);

for i=1:cellNumber
    %append to list
    growth_rate=data(:,102);
    birthLength=data(:,10);
    lifeHistory=data(:,6)+1;
end

SuperSegger_Results=array2table([def;num2cell(data)]);

%add to table
T = table(transpose(1:length(growth_rate)),growth_rate,birthLength,lifeHistory);
%add column name
T.Properties.VariableNames={'CellNumber','GrowthRate','BirthLength','LifeHistory'};

% write to csv
writetable(T,'../results/SuperSeggerAnalysis.csv','Delimiter',',','QuoteStrings',true)
% write full data
writetable(SuperSegger_Results,'../results/SuperSeggerResults.csv','Delimiter',',','QuoteStrings',true,'WriteVariableNames',0)

