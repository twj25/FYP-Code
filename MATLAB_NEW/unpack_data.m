function [az_m,el_m] = unpack_data(azel_matrix)
    [x_size, y_size] = size(azel_matrix);
    for y_pos = 1:y_size
       for x_pos = 1:x_size
           
           cell_content = azel_matrix(x_pos,y_pos);
           [az,el] = read_matlab_cell(cell_content);
           
           az_m(x_pos,y_pos) = az;
           el_m(x_pos,y_pos) = el;
           
       end
    end

end