R1 = 10;
R2 = 5;
h = 0.1;

L = 1;



Point(1) = {0,0,0,h};
Point(2) = {R1,0,0,h};
Point(3) = {0,R2,0,h};
Point(4) = {-R1,0,0,h};
Point(5) = {0,-R2,0,h};

Ellipse(1) = {2,1,3,3};
Ellipse(2) = {3,1,4,4};
Ellipse(3) = {4,1,5,5};
Ellipse(4) = {5,1,2,2};