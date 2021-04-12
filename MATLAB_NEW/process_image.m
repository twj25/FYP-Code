function process_image(t_lat,t_lon)
    [x_size, y_size] = size(t_lat);
    img_data = imread("T072142A269_.gif");
    
    t_lat = t_lat - min(min(t_lat));
    t_lon = t_lon - min(min(t_lon));
    
    t_lat = round(t_lat);
    t_lon = round(t_lon);
    
    new_size = max(max(t_lon));
    
    new_img = zeros(new_size+1:new_size+1);
    for y_pos = 1:y_size -1
        for x_pos = 1:x_size -1
            latitude = round(t_lat(x_pos,y_pos)+1);
            londitude = round(t_lon(x_pos,y_pos)+1);
            if isnan(latitude) || isnan(londitude)
                latitude = round(new_size/2);
                londitude = round(new_size/2);
            end
            new_img(latitude,londitude) = img_data(x_pos,y_pos);
        end
    end
end
