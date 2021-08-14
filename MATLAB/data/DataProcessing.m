% Remove bias and transition states
rmdata1 = [data1(:,1:3),(data1(:,4:10) -mean(data1(1:20,4:10))),data1(:,11:13)];
rmdata2 = [data2(:,1:3),(data2(:,4:10) -mean(data2(1:20,4:10))),data2(:,11:13)];
rmdata3 = [data3(:,1:3),(data3(:,4:10) -mean(data3(1:20,4:10))),data3(:,11:13)];
rmdata4 = [data4(:,1:3),(data4(:,4:10) -mean(data4(1:20,4:10))),data4(:,11:13)];
rmdata5 = [data5(:,1:3),(data5(:,4:10) -mean(data5(1:20,4:10))),data5(:,11:13)];

rmtest = [test(:,1:3),(test(:,4:10) -mean(test(1:20,4:10))),test(:,11:13)];


data = [rmdata1;rmdata2;rmdata3;rmdata4;rmdata5];

steady_data = data(1:5:end,:);
steady_test = rmtest(1:5:end,:);
