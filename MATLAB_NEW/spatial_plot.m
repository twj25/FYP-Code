function spatial_plot(lat,lon)
    img_data = imread("T072142A269_.gif");
    
    [x_size, y_size] = size(lat);
    lat((x_size+1)/2,:) = [];
    lat(:,(y_size+1)/2) = [];

    lon((x_size+1)/2,:) = [];
    lon(:,(y_size+1)/2) = [];
    
    h = pcolorm(lat,lon,img_data);
    set(h, 'EdgeColor', 'none')
%     worldmap([min(lat) max(lat)],[min(lon) max(lon)]) 
%     scatterm(lat,lon,20,img_data)
end