T = int(raw_input())
for t in range(T):
	A, B = raw_input().split()
	A = int(A)
	cur = 0
	ans = 0
	for i in range(A+1):
		X=int(B[i])
		if X > 0 and i > cur:
			ans += i-cur
			cur = i
		cur += X
	print "Casee #"+str(t+1)+": "+str(ans)