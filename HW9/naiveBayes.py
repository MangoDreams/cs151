def normalize(L):
	sum = 0.0
	fraction = 0.0
	
	
	for p in L:
		print "Before normalization: ", p
		sum += p
	
	for p in L:
		fraction = p/sum	
		print "Normalized: ", fraction

def calculate(prob,list):
	
	for p in list:
		prob *= p
	
	return prob


def main():
	k = float(0)
	n = float(15)
	A_prob = (4+k)/(n+3*k)
	B_prob = (8+k)/(n+3*k)
	C_prob = (3+k)/(n+3*k)	

	A_list = [1.0, 0.0,.25]
	B_list = [1.0, 1.0,.375]
	C_list = [.6666,.3333,.000]
	
	print "A_prob: ", A_prob
	print "B_prob: ", B_prob
	print "C_prob: ", C_prob
	
	list = []
	list.append(calculate(A_prob,A_list))
	list.append(calculate(B_prob,B_list))
	list.append(calculate(C_prob,C_list))
	
	normalize(list)	
	
	print "With k = 2 it becomes "
	k = float(2)
	n = float(15)
	A_prob = (4+k)/(n+3*k)
	B_prob = (8+k)/(n+3*k)
	C_prob = (3+k)/(n+3*k)

	print "A_prob: ", A_prob
	print "B_prob: ", B_prob
	print "C_prob: ", C_prob
	
	A_list = [.75, .25,.375]
	B_list = [.8333, .8333,.417]
	C_list = [.571, .714,.286]
	
	list = []
	list.append(calculate(A_prob,A_list))
	list.append(calculate(B_prob,B_list))
	list.append(calculate(C_prob,C_list))
	
	normalize(list)	


if __name__ == "__main__":
	main()
