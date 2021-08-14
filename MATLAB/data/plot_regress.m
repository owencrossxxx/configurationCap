%vpos = net_owen(test(:,4:10)')';
vpos = [x_regress.predictFcn(steady_test(:,4:10)),y_regress.predictFcn(steady_test(:,4:10)),z_regress.predictFcn(steady_test(:,4:10))];
st_pos = steady_test(:,11:13);

xratio=98/363.21;
zratio = 98/351.14;

figure
x1 = vpos(:,1)*xratio;
y1 = vpos(:,2)*zratio;
z1 = vpos(:,3)*zratio;
scatter3(x1,y1,z1,'r.')
hold on
x2 = st_pos(:,1)*xratio;
y2 = st_pos(:,2)*zratio;
z2 = st_pos(:,3)*zratio;
scatter3(x2,y2,z2,'b.')
legend('Prediction','Ground-truth')
xlabel('x (mm)')
ylabel('y (mm)')
zlabel('z (mm)')


figure
subplot(3,1,1)
plot(x1,'r')
hold on
plot(x2,'b')
ylabel('x (mm)')
legend('Prediction','Ground-truth')
subplot(3,1,2)
plot(y1,'r')
hold on
plot(y2,'b')
ylabel('y (mm)')
legend('Prediction','Ground-truth')
subplot(3,1,3)
plot(z1,'r')
hold on
plot(z2,'b')
ylabel('z (mm)')
legend('Prediction','Ground-truth')

x_rsmer = sqrt(immse(x1, x2));
y_rsmer = sqrt(immse(y1, y2));
z_rsmer = sqrt(immse(z1, z2));

x_mean_errorr = mean(x1-x2);
y_mean_errorr = mean(y1-y2);
z_mean_errorr = mean(z1-z2);

x_SEMr = std(x1-x2);
y_SEMr = std(y1-y2);
z_SEMr = std(z1-z2);

%mean_abs_err = mean(abs(vpos-st_pos));
