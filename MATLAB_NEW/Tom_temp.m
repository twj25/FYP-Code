[lat,lon] = azel2latlon(51,-5,t_az,t_el,ones(size(az)).*90000);
clf
for iX=1:1:size(t_az,1);for iY=1:1:size(t_az,2); plot(lon(iX,iY),lat(iX,iY),'kx');hold on; end; end;drawnow