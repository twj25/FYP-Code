function [x,y,z] = read_matlab_cell3D(cell)

    cell_content = split(cell,',');
    
    x = str2double(cell_content(1));
    y = str2double(cell_content(2));
    z = str2double(cell_content(3));
end