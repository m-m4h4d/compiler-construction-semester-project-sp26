func add:
begin_func
t1 = x + y
return t1
end_func

func main:
begin_func
alloc_array arr, 5
arr[0] = 10
arr[1] = 20
t2 = arr[0]
t3 = arr[1]
param t2
param t3
t4 = call add, 2
result = t4
return result
end_func
