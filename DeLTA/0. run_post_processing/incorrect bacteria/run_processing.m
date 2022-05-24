
datasets = ["E.coli_chamber","E.coli_mono_agarose","E.coli_mono_agarose_noisy",...
"E.coli_mono_agarose_skipTimeSteps","Pseudomonas_agarose","Pseudomonas_chamber",...
"SuperSegger sample images set","Xanthomonase_agarose","Xanthomonase_chamber"];

modes = ["1. Raw Images","2. Ilastik Output"];

interval_time = [1.5 1.5 1.5 15 1.5 1.5 1 1.5 1.5];

num_timesteps = [314 112 112 12 176 156 60 279 203];

num_datasets = length(datasets);
num_modes = length(modes);

final_dataset = {};
final_mode = {};
final_incorrect_num_daughter = [];
final_duplicate_daughter=[];



for i=1:num_datasets
    for j=1:num_modes
       dataset = datasets (i);
       %dataset
       mode = modes (j);
       %mode
       num_time_step = num_timesteps(i);
       %num_time_step
       intervalTime = interval_time(i);
       if mode == '2. Ilastik Output'
               if dataset ~= 'E.coli_mono_agarose_noisy' && dataset ~= "E.coli_chamber"
                   [duplicate_daughter,incorrect_num_daughter] = DeletaAnalysis(dataset,mode,intervalTime,num_time_step); 
                   final_dataset{end+1} = string(dataset);
                   final_mode{end+1} = mode;
                   final_incorrect_num_daughter(end+1) = incorrect_num_daughter;
                   final_duplicate_daughter(end+1) = duplicate_daughter;
               end
       else
           if dataset ~= 'E.coli_mono_agarose_skipTimeSteps' 
               [duplicate_daughter,incorrect_num_daughter] = DeletaAnalysis(dataset,mode,intervalTime,num_time_step); 
               final_dataset{end+1} = string(dataset);
               final_mode{end+1} = mode;
               final_incorrect_num_daughter(end+1) = incorrect_num_daughter;  
               final_duplicate_daughter(end+1) = duplicate_daughter;
           end
       end
    end
end


%add to table
T = table(transpose(final_dataset),transpose(final_mode),transpose(final_incorrect_num_daughter),transpose(final_duplicate_daughter));
%add column name
T.Properties.VariableNames={'dataset','mode','Number_of_incorrect_tracking','duplicate_daughter'};

% write to csv
writetable(T,'incorrect_num_daughters.csv','Delimiter',',','QuoteStrings',true)



