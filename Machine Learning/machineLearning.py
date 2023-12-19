#Mick Leungpathomaram
import random
import math

class Node:
	
	 #name is a attribute/category, OR the final outcome i.e. YES or NO, EDIBLE/POISONOUS
	def __init__(self, name):
		self.name=name
		self.certainty="."
		self.childDict={} 
	#adds a child whose key is an outcome and value is the actual Child node
	def addChild(self, outcome,node):
		self.childDict[outcome]=node
	
	#recursive function which prints all nodes in a tree, in order.
	def printAll(self,indent):
		
		if len(self.childDict)==0:
			
			print("    "*(indent)+"Then "+category+" is "+self.name+self.certainty)
		else:
			
			print("    "*(indent)+"What is the "+self.name+self.certainty+"?")
			for child in self.childDict:
				
				print("    "*(indent+1)+"If it's "+child+self.certainty+":")
				self.childDict[child].printAll(indent+2)
#requires a functional tree. Takes in a testData set and uses the helper function checkSample to prin the number of correct/wrong responses and accuracy percentage
def testTree(data):
	numCorrect=0
	numWrong=0
	
	for sample in data:
		if checkSample(sample,head)==sample[category]:
			numCorrect+=1
		else:
			numWrong+=1
	print("The Tree got "+str(numCorrect)+" correct, "+str(numWrong)+" wrong. (" +str(numCorrect/(numWrong+numCorrect)*100)+"% accuracy)")
	return [numCorrect,numWrong,numCorrect/(numWrong+numCorrect)]
#takes a set of data and a node.  Recurses until it reaches a leaf node, at which point it returns one of the category outcomes(yes, no, etc)
def checkSample(sample,node):
	if len(node.childDict)==0:
		return node.name
	#returns the sample's outcome for the given attribute
	return checkSample(sample, node.childDict[sample[node.name]])
#takes in a set of examples, and outputs a dictionary with outcomes as the keys and the number of times they occured as the value, and a dictionary with attributes as keys and the possible outcomes as value.  
def getOutcomes(data):
	outcomesDict={}
	outcomesFreq={}
	
	for obj in header:
		outcomes=[]
		
		for sample in data:
			if sample[obj] in outcomesFreq:
				outcomesFreq[sample[obj]]+=1
			else:
				outcomesFreq[sample[obj]]=1
				
			if outcomes.count(sample[obj])==0:
				outcomes.append(sample[obj])		
		outcomesDict[obj]=outcomes
	
	return outcomesFreq,outcomesDict

#given a set of data and target outcome, returns a list of dictionaries where each dictionary is a sample in which the outcome occurred
def getSamplesByOutcome(data,attr,outcome):
	samplesByOutcome=[]
	for sample in data:
		
		if sample[attr]==outcome:
			samplesByOutcome.append(sample)
	return samplesByOutcome
			
#given a list of examples, calculates the entropy of the set.  RUN GETOUTCOMES FIRST
def entropyCalc(data):
	freqList=[]
	for outcome in outcomesDict[category]:
		freqList.append(len([sample[category] for sample in data if sample[category]==outcome]))
	freqPercentList=[]
	for ind in freqList:
		freqPercentList.append(ind/len(data))
	result=0
	for i in range(0,len(freqList)-1):
		if freqList[i]!=0:
			result-=freqPercentList[i]*math.log2(freqPercentList[i])
	return result
#given a list of examples and attribute, returns the outcome as the key and the gain as the value
def infoGain(data):
		
	gain=entropy
	infoGainDict={}
	for attr in attributesList:
		gain=entropy
		for outcome in outcomesDict[attr]:
			
			outcomeFilteredData=[]  #list of dictionaries containing data from days on which the "outcome" took place
			sampleNum=0
			for sample in data:
				
				if sample[attr]==outcome:
					outcomeFilteredData.append({})
					outcomeFilteredData[sampleNum][category]=sample[category]
					sampleNum+=1
			if len(outcomeFilteredData)!=0:
				
				gain-=(abs(outcomesFreq[outcome])/abs(len(data))*entropyCalc(outcomeFilteredData))
			
		infoGainDict[attr]=gain
	return infoGainDict
#takes in examples, returns most common category and its percent
def commonCategory(data):
	
	freqDict={}
	mostCommon=outcomesDict[category][0]
	for outcome in outcomesDict[category]:
		
		frequency=len([sample[category] for sample in data if sample[category]==outcome])
		freqDict[outcome]=frequency
		if freqDict[outcome]>freqDict[mostCommon]:
			mostCommon=outcome
	freqPercentList={}
	for ind in freqDict:
		freqPercentList[ind]=(freqDict[ind]/len(data))*100
	
	return (mostCommon,". NOTE: "+str(freqPercentList[mostCommon])+"% certainty")

def ID3(examples,attributes):
	
	if len(set([example[category] for example in examples]))==1:
		return Node(examples[0][category])
	
	if len(attributes)==0:
		commonCat=commonCategory(examples)
		output=Node(commonCat[0])
		output.certainty=commonCat[1]
		return output
	
	currentAttr=attributes[0]
	for attribute in attributes:
		if attributesGain[attribute]>attributesGain[currentAttr]:
			currentAttr=attribute
		
	outputNode=Node(currentAttr)
	
	for outcome in outcomesDict[currentAttr]:
		#if there are no target outcomes in the examples list, just pass the node the common category
		if [example[currentAttr] for example in examples].count(outcome)==0:
			commonCat=commonCategory(examples)
			output=Node(commonCat[0])
			output.certainty=commonCat[1]
			outputNode.addChild(outcome,output)
		else:
			newAttributes=attributes[:]
			newAttributes.remove(currentAttr)			
			
			outputNode.addChild( outcome, (ID3(getSamplesByOutcome(examples,currentAttr,outcome),newAttributes))  )
	return outputNode

fileName=input("Filename: ") +".txt"
#percentage of total data used for "learning"
samplePercentage=int(input("Learning sample percentage: "))
data=open(fileName,"r")
dataList=[] 
sampleData=[]
testData=[]

attributesList=[]
sampleCount=0

header=data.readline().strip().split(",")
category=header[0]
attributesList=header[1:]


for l in data:
	line=l.strip()
	attributes=line.split(",")
	
	dataList.append({})
	resultNum=0
	for result in attributes:
		dataList[sampleCount][header[resultNum]]=result
		resultNum+=1
	sampleCount+=1


random.shuffle(dataList)

outcomesFreq,outcomesDict=getOutcomes(dataList)

sampleData=dataList[0:int(len(dataList)*samplePercentage/100)]
testData=dataList[int(len(dataList)*(samplePercentage/100))+1:]

entropy=entropyCalc(sampleData)
attributesGain=infoGain(sampleData)

head=ID3(sampleData,attributesList)
head.printAll(0)

testTree(testData)