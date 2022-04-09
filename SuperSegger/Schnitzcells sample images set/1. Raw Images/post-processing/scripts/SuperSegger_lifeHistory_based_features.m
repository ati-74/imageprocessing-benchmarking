
load('../../xy1/clist.mat','data');

cellNumber=length(data);
intervalTime = 1;

for i=1:cellNumber
    %append to list
    growth_rate=data(:,102);
    birthLength=data(:,10);
    lifeHistory=data(:,6)+1;
end

%calculation of average length and average velocity
[AverageVelocity,AverageLength] = SupperSegger_Extract_lifeHistory_based_features(intervalTime);

%add to table
T = table(transpose(1:length(growth_rate)),growth_rate,birthLength,lifeHistory,transpose(AverageVelocity),transpose(AverageLength));
%add column name
T.Properties.VariableNames={'CellNumber','GrowthRate','birthLength','LifeHistory','AverageVelocity','AverageLength'};

% write to csv
%life history based features
writetable(T,'../results/SuperSegger_LifeHistory_based_Analysis.csv','Delimiter',',','QuoteStrings',true)

