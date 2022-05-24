function [duplicate_daughter,incorrect_num_daughter] = DeletaAnalysis(dataset,mode,intervalTime,num_time_steps)

load(strcat('../../',dataset,'/',mode,'/2. results/Position000000.mat'),'res');

cellNumber=length(res{1}.lineage);
minLife=2;

incorrect_num_daughter=0;
incorrect_num_life_history_mother = 0;
daughters_ids = [];
duplicate_daughter = 0;

for i=1:cellNumber
    valid_frames_index = find(res{1}.lineage{i}.frames <=num_time_steps);
    valid_frames = res{1}.lineage{i}.frames(valid_frames_index);
    daughters =  res{1}.lineage{i}.daughters(valid_frames_index);
    if isempty(valid_frames)==0
        daughters = daughters(daughters~= 0);
        if length(daughters) ~=2
           incorrect_num_daughter = incorrect_num_daughter +1 ;
        end
        if length(daughters) >0
           daughters_ids = [daughters_ids , daughters]; 
        end
    end
end

duplicate_daughter = find(hist(daughters_ids,unique(daughters_ids))>1);
%duplicate_daughter
duplicate_daughter = length(duplicate_daughter);

