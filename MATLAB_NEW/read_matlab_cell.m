function [az,el] = read_matlab_cell(cell)

    cell_content = split(cell,',');
    
    az = str2double(cell_content(1));
    el = str2double(cell_content(2));
end