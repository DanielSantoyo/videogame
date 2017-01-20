close all
clc

if !exist("mare","var")
   mare=input("sea level: ");
end

load collina.txt;
[x,y]=size(collina);
z=max(max(collina));
surf(collina(end:-1:1,end:-1:1));
hold on;
mesh(mare*ones(size(collina)));
axis([0 x 0 y 0 z]);
axis equal
axis off

pause(2)

print collina.jpg

clear x y z 