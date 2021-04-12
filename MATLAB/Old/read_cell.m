function [az,el] = read_cell(cell)
    
    
    cell_content = split(cell,',');
    az = string(cell_content(1,1));
    el = string(cell_content(2,1));

    az = strtok(az,'(');
    el = strtok(el,')');

    az = str2double(az);
    el = str2double(el);
    
end