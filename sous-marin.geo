Mesh.MshFileVersion = 2.2;


R1 = 1;
R2 = 0.5;
h = 0.02;

L = 1;


// Centre d'ellipse
Point(1) = {0,0,0,h};

// Points d'ellipse
Point(2) = {R1,0,0,h};
Point(3) = {0,R2,0,h};
Point(4) = {-R1,0,0,h};
Point(5) = {0,-R2,0,h};

Ellipse(1) = {2,1,3,3};
Ellipse(2) = {3,1,4,4};
Ellipse(3) = {4,1,5,5};
Ellipse(4) = {5,1,2,2};

Curve Loop(1) = {1,2,3,4};


// Points sous-marin
Point(6) = {L/2,0,0,h};
Point(7) = {2*L/5,0,0,h};
Point(8) = {2*L/5,0.1,0,h};
Point(9) = {L/3.8,0.115,0,h};
Point(10) = {L/3.8,0.2,0,h};
Point(11) = {L/4,0.25,0,h};
Point(12) = {L/6,0.23,0,h};
Point(13) = {L/10,0.2,0,h};
Point(14) = {L/14,0.115,0,h};
Point(15) = {-L/3.8,0.115,0,h};
Point(16) = {-L/3,0.10,0,h};
Point(17) = {-L/2.5,0.07,0,h};
Point(18) = {-L/2,0,0,h};
Point(19) = {-L/2.5,-0.07,0,h};
Point(20) = {-L/3,-0.10,0,h};
Point(21) = {2*L/5,-0.1,0,h};
Point(22) = {-L/3,0.18,0,h};
Point(23) = {-L/2.5,0.13,0,h};
Point(24) = {-L/2.5,-0.18,0,h};
Point(25) = {-L/3,-0.13,0,h};

// Curves sous-marin
Circle(5) = {6,7,8};
Circle(6) = {21,7,6};
Spline(7) = {8,9,10,11,12,13,14};
Line(8) = {14,15};
Spline(9) = {15,16};//,17,18,19,20};

Line(10) = {22,16};
Line(11) = {23,22};
Line(12) = {17,23};
Spline(13) = {16,17};
Curve Loop(2) = {13,12,11,10};


Spline(14) = {17,18,19};
Line(15) = {24,19};
Line(16) = {25,24};
Line(17) = {20,25};
Spline(18) = {19,20};
Curve Loop(3) = {15,16,17,18};

Line(19) = {20,21};
Curve Loop(4) = {5,7,8,9,13,14,18,19,6};

Plane Surface(1) = {1,2,3,4};
Physical Surface(1) = {1};