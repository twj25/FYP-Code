select = 3;

% T = readtable('test.csv');
% cell_content = T{254,128};
% [az,el] = read_cell(cell_content);

% B_mag = convert_to_mag(B);
% plot_mags(B_mag);

% x=3;
% y=4;
% cell_content = C(x,y);
% [az,el] = read_matlab_cell(cell_content);
% [x_val,y_val] = solve_equ(az,el,select);
% [az1,el1] = check_solve_ans(x_val,y_val);

[x_size, y_size] = size(C);


D = zeros(x_size,y_size);
D = string(D);
for y_pos = 1:y_size
    for x_pos = 1:x_size
        percentage = num2str(((((y_pos-1)*y_size)+x_pos)/(x_size*y_size))*100);
        print_percentage = [percentage,'%'];
        disp(print_percentage)
        cell_content = C(x_pos,y_pos);
        [az,el] = read_matlab_cell(cell_content);
        [x,y] = solve_equ(az,el,select);
        val = string([num2str(x),',', num2str(y)]);
        disp(val)
        D(x_pos,y_pos) = val;
    end
end



