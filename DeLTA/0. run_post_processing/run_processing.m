
datasets = ["E.coli_chamber","E.coli_mono_agarose","E.coli_mono_agarose_noisy",...
"E.coli_mono_agarose_skipTimeSteps","Pseudomonas_agarose","Pseudomonas_chamber",...
"SuperSegger sample images set","Xanthomonase_agarose","Xanthomonase_chamber"];

modes = ["1. Raw Images","2. Ilastik Output"];

interval_time = [1.5 1.5 1.5 15 1.5 1.5 1 1.5 1.5];

num_timesteps = [314 112 112 12 176 156 60 279 203];

num_datasets = length(datasets);
num_modes = length(modes);



for i=1:num_datasets
    for j=1:num_modes
       dataset = datasets (i);
       dataset
       mode = modes (j);
       mode
       num_time_step = num_timesteps(i);
       num_time_step
       intervalTime = interval_time(i);
       intervalTime
       if mode == '2. Ilastik Output'
               if dataset ~= 'E.coli_mono_agarose_noisy' && dataset ~= "E.coli_chamber"
                   bac_lable = DeLTA_Lineaged_base_features(dataset,mode,num_time_step);
                   DeLTA_bacteria_based_features_each_timestep(dataset,mode,num_time_step,bac_lable); 
                   DeletaAnalysis(dataset,mode,intervalTime,num_time_step);  
               end
       else
           if dataset ~= 'E.coli_mono_agarose_skipTimeSteps'
               bac_lable = DeLTA_Lineaged_base_features(dataset,mode,num_time_step);
               DeLTA_bacteria_based_features_each_timestep(dataset,mode,num_time_step,bac_lable); 
               DeletaAnalysis(dataset,mode,intervalTime,num_time_step);      
           end
       end
    end
end

