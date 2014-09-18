#/usr/bin/python


def vectorAdd(w,f,k):
	for i in range(len(w)):
	 	w[i] = w[i] + k*f[i]
	return w


def update(weights,f,actual_idx,predicted_idx):
	
	finalResult = []
	w = weights[actual_idx]
	v = weights[predicted_idx]	


	if(dotProduct(w,f) > dotProduct(v,f)):
		weights[actual_idx] = vectorAdd(w,f,-1)
		weights[predicted_idx] = vectorAdd(v,f,1)
	else:
	
		weights[actual_idx] = vectorAdd(w,f,1)
		weights[predicted_idx] = vectorAdd(v,f,-1)

	return weights	

def createList(A,B,C):
	weights = []
	weights.append(A)
	weights.append(B)
	weights.append(C)
	return weights


def dotProduct(w,f):
	d = 0.0
	for i in range(len(f)):
		d += w[i]*f[i]
	return d

def classifyAndPredict(weights,f):
	dotProducts = []	
	for w in weights:
		dotProducts.append(dotProduct(w,f))
	print dotProducts
	idx = dotProducts.index(max(dotProducts))
	return idx			

def MultiClassPerceptron(weights,f,actual_idx):
	predicted_idx = classifyAndPredict(weights,f)
	weights = update(weights,f, actual_idx,predicted_idx)
	print weights	
	return weights

def main():
	A = [-.23, -1.46]
	B = [-.87, -1.55]
	C = [1.89, 1.59]
	f = [.36,.55]	
	f1 = [-1.07,.16]	
	
	weights = createList(A,B,C)
	
	weights = MultiClassPerceptron(weights,f,0)
	print "One iteration complete \n \n"
	weights = MultiClassPerceptron(weights,f1,2)
	
	print "Two iterations complete \n \n"
	Aconv = [5.12,.46]
	Bconv = [5.1,-.55]
	Cconv = [-9.43,-1.33]
	f2 = [-.69,.42]

	print dotProduct(Aconv,f2)
	print dotProduct(Bconv,f2)
	print dotProduct(Cconv,f2)
			


if __name__ == "__main__":
	main()
