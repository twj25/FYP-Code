function [x_val,y_val] = solve_equ(az,el,select)
    syms y x

    R = 6370;
    H = 90;

    psi = ((y^2)*(sec(az)^2))/(R+H);
    a = 2*(R + H)*sin(psi/2);
    alpha = 0.5*(pi - psi);
    c = (H^2 + a^2 - (2*H*a)*cos(alpha))^0.5;

    eqn = (a/c)*sin(alpha) - cos(el) == 0;

    y1 = solve(eqn,y);

    x = y1*tan(az);

    try
        x_val = double(x(select));
    catch 
        x_val = 0;
    end
        
    if az ~= 0
        y_val = x_val/tan(az);
    else
        y_val = el/(1/127);
    end
%     disp(x_val)
%     disp(y_val)
end