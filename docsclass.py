import re
import math

def getwords(doc):
	splitter=re.compile('\\W*')
	words = [ s.lower() for s in splitter.split(doc) if len(s)>2 and len(s)<20 ]
	return dict( [ (w,1) for w in words ] )


def simpletrain(c1):
	c1.train('Nobody owns the water.', 'good')
	c1.train('the quick rabbit jumps fences', 'good')
	c1.train('buy pharmaceuticals now', 'bad')
	c1.train('make quick money at the online casino', 'bad')
	c1.train('the quick brown fox jumps', 'good')


class classifier:
	def __init__(self,getfeatures,filename=None):
		self.fc = {}
		self.cc = {}
		self.getfeatures = getfeatures

	def incf(self,f,cat):
		self.fc.setdefault(f,{})
		self.fc[f].setdefault(cat,0)
		self.fc[f][cat] += 1

	def incc(self,cat):
		self.cc.setdefault(cat,0)
		self.cc[cat] += 1

	def fcount(self,f,cat):
		if f in self.fc and cat in self.fc[f]:
			return float(self.fc[f][cat])
		return 0.0

	def catcount(self,cat):
		if cat in self.cc:
			return float(self.cc[cat])
		return 0.0

	def totalcount(self):
		return sum(self.cc.values())

	def categories(self):
		return self.cc.keys()

	def train(self,item,cat):
		features = self.getfeatures(item)
		for f in features:
			self.incf(f,cat)
		self.incc(cat)


	def fprob(self,f,cat):
		if self.catcount(cat) == 0: return 0.0
		return self.fcount(f,cat) / self.catcount(cat)

	def weightedprob(self,f,cat,prf,weight=1.0,ap = 0.5):
		basicprob = prf(f,cat)
		totals = sum([ self.fcount(f,c) for c in self.categories() ])
		bp = (weight*ap + basicprob*totals)/(weight+totals)
		return bp

class naivebayes(classifier):
	def docprob(self,item,cat):
		features = self.getfeatures(item)
		p = 1.
		for f in features: p *= self.weightedprob(f,cat,self.fprob)
		return p

	def prob(self,item,cat):
		catprob = self.catcount(cat) / self.totalcount()
		docprob = self.docprob(item,cat)
		return catprob * docprob