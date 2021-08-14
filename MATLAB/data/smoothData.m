[r,c] = size(test);
s_test=zeros(r,c);

for i = 1:13
    s_test(:,i) = smooth(test(:,i));
end
