function plot_coordinates2D(latlon_matrix)
    [x_size, y_size] = size(latlon_matrix);
    lats = [0];
    lons = [0];
    for y_pos = 1:y_size
        for x_pos = 1:x_size

            cell_content = latlon_matrix(x_pos,y_pos);
            [lat,lon] = read_matlab_cell(cell_content);
            lats(end + 1) = lat*100;
            lons(end + 1) = lon*100;
            
        end
    end
%     lats = lats(lats~=0);
%     lons = lons(lons~=0);
    c = linspace(1,10,length(lats));
    figure();
    scatter(lats,lons,[],c)
%     xlabel('lat');
%     ylabel('lon');
end