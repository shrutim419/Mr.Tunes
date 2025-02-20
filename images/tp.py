
#op bro
nums=[1,4,3,3,2]
c=1
c1=1
inc=1
dec=1
for i in range(1,len(nums)):
    if nums[i]>nums[i-1]:
        c+=1
        c1=1
    elif nums[i]<nums[i-1]:
        c1+=1
        c=1
    else:
        c=1
        c1=1
    inc=max(inc,c)
    dec=max(dec,c1)
dec=max(dec,c1)
inc=max(inc,c1)
print(max(dec,inc))