%string('E.coli_chamber'),
datasets = [string('E.coli_mono_agarose'),string('E.coli_mono_agarose_noisy'),...
    string('E.coli_mono_agarose_skipTimeSteps'),string('Pseudomonas_agarose'),string('Pseudomonas_chamber'),...
    string('SuperSegger sample images set'),string('Xanthomonase_agarose'),string('Xanthomonase_chamber')];
modes = [string('1. Raw Images'),string('2. Ilastik Output')];
interval_time = [ 1.5 1.5 15 1.5 1.5 1 1.5 1.5];
% 1.5
num_datasets = length(datasets);
num_modes = length(modes);

for i=1:num_datasets
    for j=1:num_modes
       dataset = datasets (i);
       dataset
       mode = modes (j);
       mode
       if mode == '2. Ilastik Output'
           if dataset ~= 'E.coli_mono_agarose_noisy'
                ExtractCellFeatures(dataset,mode)
           end
       else
           if dataset ~= 'E.coli_mono_agarose_skipTimeSteps'
            ExtractCellFeatures(dataset,mode)
           end
       end
    end
end
