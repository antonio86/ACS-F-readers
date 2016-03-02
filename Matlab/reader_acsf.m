function Data = reader_acsf (db_dir)

Data = [];
cnt = 1;
mod = 1;
folders = dir(db_dir);
for i=1:length(folders)
    if ~strcmp(folders(i).name(1),'.')
        files = dir([db_dir '/' folders(i).name '/*.mat']);
        for j=1:length(files)
            fid = fopen([db_dir '/' folders(i).name '/' files(j).name]); 
            data_mat = textscan(fid, '%f', 'CommentStyle','#');
            data_mat = cell2mat(data_mat);
            data_mat = reshape(data_mat,length(data_mat)/6,6)';
            fclose(fid);
            Data(cnt).data_mat = data_mat;
            Data(cnt).session = str2num(files(j).name(end-4));
            Data(cnt).label = mod;
            Data(cnt).name = files(j).name;
            cnt = cnt + 1;
        end
         mod = mod + 1;
    end
end
