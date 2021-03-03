function [array_mag] = convert_to_mag(array_2D)
    array_mag = zeros(255,255);
    for y = 1:255
        for x = 1:255
            [xmag, ymag] = read_matlab_cell(array_2D(x,y));
            array_mag(x,y) = abs(xmag)+abs(ymag);
        end
    end
end