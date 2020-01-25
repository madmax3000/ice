stat=0
d=0.2
t=1
for i in range(0,100):
	if i>=stat :
		if t==1:
			t=0
			stat=stat + 10*d
		else:
			t=1
			stat=stat +(1-d)*10
	print(t)
		
	