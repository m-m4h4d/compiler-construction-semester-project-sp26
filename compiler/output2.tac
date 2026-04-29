func main:
begin_func
sum = 0
i = 0
L1:
t1 = i < 10
if_false t1 goto L2
t2 = sum + i
sum = t2
t3 = i + 1
i = t3
goto L1
L2:
j = 0
L3:
t4 = j < 5
if_false t4 goto L4
t5 = sum + j
sum = t5
t6 = j + 1
j = t6
goto L3
L4:
return sum
end_func
