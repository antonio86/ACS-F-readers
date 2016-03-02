clear;
% tested with Matlab R2014a

Data = reader_acsf('ACS-F2');

% compute the training/test data
list_session = [Data(:).session];
Train_Data = Data(list_session == 1);
Test_Data = Data(list_session == 2);
nModels = length(unique([Data(:).label]));

% Training phase
% K is the number of Gaussians
K = 40;
Points = [Train_Data(:).data_mat]'; 
label_points = [];
for i = 1:length(Train_Data) % create the two matrixes
    label_points = [label_points repmat(Train_Data(i).label, 1,size(Train_Data(i).data_mat,2))];
end
Model = [];
for i = 1:nModels  
    try
        rng(i);
        Model{i} = fitgmdist(Points(label_points == i,:), K,'Regularize', 0.05);
    catch exception
        sprintf('error --> i = %d', i)
        error = exception.message;
    end
end

% Testing phase
ConfMat = zeros(nModels);
for i = 1:length(Test_Data)
    scoreval = zeros(1,nModels);
    for c = 1:nModels
        log_scores = log(Model{c}.pdf(Test_Data(i).data_mat')');
        log_scores(isinf(log_scores)) = -50;
        scoreval(c) = sum(log_scores);     
    end
    [~, idx] = max(scoreval);
    ConfMat(idx, Test_Data(i).label) = ConfMat(idx, Test_Data(i).label) + 1; 
end 
disp(ConfMat);
disp(trace(ConfMat) / sum(ConfMat(:)));