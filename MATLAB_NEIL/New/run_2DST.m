function [X,Y,ST] = run_2DST(filepath)


% height of the airglow layer above the ground
h = 90; % km (TOM CHECK THIS)

% Camera Lat/Lon (I don't know this, so I chose my house!)
% % Mcdonald
% cameralat = 30;
% cameralon = -104;
% Mercedes
cameralat = -29;
cameralon = -58;

% define a new regular distance  grid:
dx = 1; % spacing between points on new grid (km). Use a finer grid spacing if you want, but it'll take longer.
gridlim = 500; % km, I assume we want another square...
[newgridX,newgridY] = ndgrid(-gridlim:dx:gridlim,-gridlim:dx:gridlim);

% apply my function below:
[regridded_image,x_in,y_in,Lat,Lon] = regridairglowimage(filepath,cameralat,cameralon,h,newgridX,newgridY);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% APPLY THE 2DST TO THE AIRGLOW IMAGE - WITH BACKGROUND REMOVED
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%% here we're going to, as the title suggests, apply the 2DST to the
%%%% nicely regridded data and plot some parameters.
%%% you'll need nph_ndst() in the matlab path for this to work, I've
%%% included it in the email.

%%%% BUT FIRST: REMOVE BACKGROUND AIRGLOW FROM THE IMAGE
%%%% we're going to start with the regridded image from before.
im = regridded_image;
X = newgridX; Y = newgridY; % save typing time :)
% figure; pcolor(X,Y,IN); shading flat;

% CHECK REGRIDDING IS WORKING CORRECTLY
% figure(); pcolor(newgridX,newgridY,regridded_image); shading flat; axis square; set(gca,'tickdir','out')
% title('image on new regular distance grid (zoomed in)')
% boundary = 100;
% bx = boundary.*[-1 1 1 -1 -1];
% by = boundary.*[-1 -1 1 1 -1];
% xlim(2.*[-boundary boundary])
% ylim(2.*[-boundary boundary])
% xlabel('km');
% ylabel('km'); 
% colormap('gray')
% % add that same boundary:
% hold on; plot(bx,by,'m');

%%%% initially, give the image a little smooth to reduce retrieval noise:
im = movmean(movmean(im,3,1),3,2);

%%%% trim the image to a smaller square, away from any trees or shadows at
%%%% the edges.
newgridlim = 150;
region = {abs(newgridX(:,1)) < newgridlim,abs(newgridY(1,:)) < newgridlim};
X = X(region{:});
Y = Y(region{:});
im = im(region{:});

%%%% we need to establish a "background" sky to remove from the image to
%%%% reveal the perturbations. To make this, we'd normally smooth the data
%%%% then subtract this. But stars make this a problem as they artificially
%%%% boost any smoothing we may apply. So we must remove them first.

% first let's make the stars really prominent by squaring applying a power
% to the image:
im_sq = im;
stargradlim = 5;

%%%% let's try and remove some stars using a gradient method...
%%%% anywhere where the 2-point gradient is greater than some value
diff1 = diff(im_sq([1 1:end],:),[],1);
diff2 = diff(im_sq(:,[1 1:end]),[],2);
diffdiff = max(cat(3,diff1,diff2),[],3);
% figure; pcolor(X,Y,diffdiff); shading flat;
% oooooh we can see the stars, nice

% now remove anywhere where the gradient is above some value, sorry this is
% just gonna hev to be a number for now. There's def a better way of
% working one out but I'll leave to you :D
im_nostars = im;
starlocs = double(diffdiff > stargradlim);
% make the stars a little bit wider:
starlocs = movmean(movmean(starlocs,3,1),3,2);
starlocs(starlocs > 0) = 1;
im_nostars(logical(starlocs)) = NaN;
% figure; pcolor(X,Y,IN); shading flat; % check our working with a figure

%%%% now most stars are removed, we can do a background smoother to get
%%%% an idea of the background sky's airglow. A good smoother to use here
%%%% is movmean(), which can ignore NaNs...

filterwidth = 20 / dx; % try a 50km filter width
bg = movmean(movmean(im_nostars,filterwidth,1,'omitnan'),filterwidth,2,'omitnan');

% figure; pcolor(X,Y,bg); shading flat;
% check your working again. there should be no GWs at all left in our
% background.

% remove this from the input image:
im_perts = im_nostars - bg;
% figure; pcolor(X,Y,im); shading flat; % phwoar this looks great

% set these locations to zero for now.
im_perts(isnan(im_perts)) = 0;

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%% Now we're gonna apply the 2DST. Try these settings below and see how
%%%% you get on.

IN = im_perts;

% number of frequencies to analyse for
scales = 1000;
% spacing of the input data
grid_spacing = [dx dx];
% scale factor (try adjusting this and seeing what happens). This
% represents a trade off between spatial and spectral resolution.
c = [1 1];

% set a threshold for wavelengths to consider. We don't want any of the
% stars in our measurements
minwavelengths = [3 3]; % in km

ST = nph_ndst(IN,scales,grid_spacing,c,'minwavelengths',minwavelengths);
ST.LH = 1./sqrt(ST.F1.^2 + ST.F2.^2);
