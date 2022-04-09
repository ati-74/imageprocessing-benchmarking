
load('../../xy1/clist.mat','data');
load('../../xy1/clist.mat','def');

% total information about cells
SuperSegger_Results=array2table([def;num2cell(data)]);

% write to csv
% write full data
writetable(SuperSegger_Results,'../results/SuperSegger_Bacteria_features.csv','Delimiter',',','QuoteStrings',true,'WriteVariableNames',0)

