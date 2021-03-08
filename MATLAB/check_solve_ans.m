function [az,el] = check_solve_ans(x,y)
    R = 6370;
    H = 90;
    
    r = (x^2+y^2)^0.5;
    psi = r/(R+H);
    a = 2*(R+H)*sin(psi/2);
    alpha = (pi - psi)/2;
    c = (H^2+a^2 - (2*H*a*cos(alpha)))^0.5;

    el = acos((a*sin(alpha)/c));
    az = atan(x/y);
end