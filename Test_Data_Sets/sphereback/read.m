%% get video stack
pngfiles = dir('*.png');
z = [];
it = 0;
for k = 1:1:length(pngfiles)
    filename = pngfiles(k).name;
    I = imread(filename);
    I = rgb2gray(I);
    %x = x(40:790,15:1020);%for leaves
    %x = x(40:550,15:520);%for cookie
    I = imresize(I,0.5);
    it = it+1
    z(:,:,it) = I;
end
%%
% r = 270, c = 480
[r,c,fr] = size(z)
vecf = zeros(fr,r*c);
for xr = 1:1:r
    for xc = 1:1:c
        vecf(:,(xr-1)*c + xc) = z(xr,xc,:);
    end
end

%%
cnt = 0;
test = zeros(r,c);
for x = 1:1:r
    for y = 1:1:c
        cnt = cnt+1;
        test(x,y) = vecf(4,cnt);
    end
end
imshow(uint8(test))