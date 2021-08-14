
vpos = net(steady_test(:,4:10)')';
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

x_rsme = sqrt(immse(x1, x2));
y_rsme = sqrt(immse(y1, y2));
z_rsme = sqrt(immse(z1, z2));

x_mean_error = mean((x1-x2));
y_mean_error = mean(y1-y2);
z_mean_error = mean(z1-z2);

x_abs_mean_error = mean(abs(x1-x2));
y_abs_mean_error = mean(abs(y1-y2));
z_abs_mean_error = mean(abs(z1-z2));

x_SEM = std(x1-x2);
y_SEM = std(y1-y2);
z_SEM = std(z1-z2);

%mean_abs_err = mean(abs(vpos-st_pos));
