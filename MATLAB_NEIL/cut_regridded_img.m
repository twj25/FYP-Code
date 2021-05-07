xmin = 400;
xmax = 650;
ymin = 400;
ymax = 650;

% CUT IMAGE TO SIZE
new_img = regridded_image(xmin:xmax, ymin:ymax);
new_newgridX = newgridX(xmin:xmax, ymin:ymax);
new_newgridY = newgridY(xmin:xmax, ymin:ymax);

% PSF = fspecial('gaussian',80,20);
% new_img = edgetaper(new_img,PSF);

% new_img(1:50,:) = 0;
% new_img(end-50:end,:) = 0;
% 
% new_img(:,1:50) = 0;
% new_img(:,end-50:end) = 0;

figure(5);
pcolor(airs_img); shading flat; colormap('gray'); colorbar;


% PLOT REGRIDDED IMAGE
figure(1);
pcolor(new_newgridX,new_newgridY,new_img); shading flat; colormap('gray'); colorbar;

% REMOVE STARS
indices = find(abs(new_img)>160);
new_img(indices) = new_img(indices+4);

new_img = new_img - median(new_img,'all');
%new_img = new_img - 200;

% REMOVE BLACK PATCHES
% indices = find(new_img <-100);
% new_img(indices) = 0;

%new_img = new_img/5;
% REPLOT REGRIDDED IMAGE
figure(2);
pcolor(new_newgridX,new_newgridY,new_img); shading flat; colormap('gray'); colorbar;



% PLOT WAVE AMPLITUDE USING CORWIN FUNCTION
figure(3);
ST = nph_ndst(new_img,1000);
% ST2 = nph_ndst(new_img,1000);
% test = ST2.A - ST.A;
pcolor(ST.A); shading flat; colorbar; title("Amplitude"); caxis([0,60]);

% PLOT WAVE DIRECTION USING CORWIN FUNCTION
figure(4);
Direction = atan2d(ST.F2,ST.F1);
pcolor(Direction); shading flat; colorbar; title("Direction");
