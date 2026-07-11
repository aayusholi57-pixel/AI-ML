point=[120,80,200,50,300]
total=0
for p in point:
    total=total + p
print(total)
cheapest=min(point)
print(cheapest)
dearest=max(point)
append=point.append(400)
count=len(point)
print(count)
average=total/count
print(average)