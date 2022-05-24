function [duplicate_daughter,num_incorrect_daughter,num_incorrect_lifehistory] = SuperSegger_lifeHistory_based_features(dataset,mode,intervalTime,num_time_steps)

load(strcat('../../',dataset,'/',mode,'/xy1/clist.mat'),'data');
num_incorrect_daughter = 0;
num_incorrect_lifehistory = 0;
duplicate_daughter = 0;

cellNumber=size(data,1);

for i=1:cellNumber
    %append to list
    % column 62: Daughter1 ID
    % column 63: Daughter2 ID
    if (isnan(data(i,62))==0 && isnan(data(i,62))~=0) || (isnan(data(i,62))~=0 && isnan(data(i,62))==0)
       num_incorrect_daughter = num_incorrect_daughter + 1; 
    end
    % column 4: 'Cell birth time'
    % column 5: 'Cell death time'
    if isnan(data(i,62))==0
        daughter_id = data(i,62);
        if daughter_id <= max(cellNumber)
           if data(i,5) > data(daughter_id,4)
              num_incorrect_lifehistory = num_incorrect_lifehistory + 1;
           end    
        end
    else    
        if isnan(data(i,63))==0
                daughter_id = data(i,63);
                if daughter_id <= max(cellNumber)
                    if data(i,5) > data(daughter_id,4)
                        num_incorrect_lifehistory = num_incorrect_lifehistory + 1;
                    end    
                end
        end
    end
end

% duplicate daughter
daughter1 = transpose(data(:,62));
daughter2 = transpose(data(:,63));
daughter1 = [daughter1,daughter2];
daughter1 = daughter1(~isnan(daughter1));
duplicate_daughter = find(hist(daughter1,unique(daughter1))>1);

duplicate_daughter = length(duplicate_daughter);


