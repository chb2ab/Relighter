%% get video stack
pngfiles = dir('*.jpg');
z = [];
it = 0;
for k = 1:10:length(pngfiles)
    filename = pngfiles(k).name;
    I = imread(filename);
    %I = rgb2gray(I);
    %x = x(40:790,15:1020);%for leaves
    %x = x(40:550,15:520);%for cookie
    imwrite(uint8(I), strcat('cube110/', num2str(it), '.jpg'));
    it = it+1
end