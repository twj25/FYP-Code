az = 0:5:360;
el = logspace(log10(0.1),log10(90),30); el = [el,el(end-1:-1:1)];
[az,el] = meshgrid(az,el);
[lat,lon] = azel2latlon(51,-5,az,el,ones(size(az)).*90000);
clf
for iX=1:1:size(az,1);for iY=1:1:size(az,2); plot(lon(iX,iY),lat(iX,iY),'kx');hold on; end; end;drawnow
