function plot_coordinates3D(xyz_matrix, plot_rec)
    [x_size, y_size] = size(xyz_matrix);
    xs = [0];
    ys = [0];
    zs = [0];
    for y_pos = 1:y_size
        for x_pos = 1:x_size

            cell_content = xyz_matrix(x_pos,y_pos);
            [x,y,z] = read_matlab_cell3D(cell_content);
            xs(end + 1) = x;
            ys(end + 1) = y;
            zs(end + 1) = z;
        end
    end
    c = linspace(1,10,length(xs));
    scatter3(xs,ys,zs,[],c)

    if plot_rec == true
        hold on

        lat = 30;
        lon = -104;
        alt = 2085;
        % Convert lat and lon to radians
        lat = lat / (180/pi);
        lon = lon / (180/pi);

        [x,y,z] = lla2ecef(lat,lon,alt);
        scatter3(x,y,z);
    end
end