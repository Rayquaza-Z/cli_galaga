n,t=map(int, input().split())
arr=list(map(int, input().split()))
s=1
e=max(arr)*t
ans=0
#p=t
while s<=e:
    p=t
    m=(s+e)//2
    for i in arr:
         p-=m//i
    if p<=0:
        e=m-1
        ans=m
    else:
        s=m+1
print(ans)
