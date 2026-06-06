arr=[10,20,30,40]
n=len(arr)
arr.append(arr[-1])
for i in range(n-1,0,-1):
    arr[i]=arr[i-1]

arr[0]=5
print(arr)


    

