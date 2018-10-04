from flask import Flask, request, jsonify 
import json 
import os
import pandas as pd
import re

app = Flask(__name__) 
port = '80' 
dataframe = pd.read_csv('downloaded.csv')
dataframeAzure = pd.read_csv('azureVmSouth.csv')

@app.route('/', methods=['POST']) 
def index(): 
  data = json.loads(request.get_data())
  #input = data['nlp']['source']
  input = data['key']
  result = findResult(input)
  return jsonify( 
    status=200, 
    replies=[{ 
      'type': 'text', 
      'content': result, 
    }]
  ) 

@app.route('/errors', methods=['POST']) 
def errors(): 
  print(json.loads(request.get_data())) 
  return jsonify(status=200) 


stringExample = 'hello memory standard_g2'


instances= dataframe['Instance Type'].tolist()
#print(instances)
columnHeadings = dataframe.columns.values.tolist()
#print(columnHeadings)
columnHeadings = [x.lower() for x in columnHeadings]

def test1(input):
  
  instancePresent = ''
  columnHeadingsPresent = ''
  result = 'please include more information'
  
  for instance in instances:
    if instance in input:
      instancePresent = instance
  
  for column in columnHeadings:
    if column in input:
      columnHeadingsPresent = column.title()
      if columnHeadingsPresent in 'Vcpu':
        columnHeadingsPresent = 'vCPU'
    
  if 'price' in input:
    columnHeadingsPresent = 'PricePerUnit'
      
  if instancePresent and columnHeadingsPresent:
    #print('instancePresent and columnHeadings are equal to true')
    indexInstance = instances.index(instancePresent)
    dataValue = dataframe.iloc[indexInstance][columnHeadingsPresent]
    unitValue = dataframe.iloc[indexInstance]['Unit']
    currencyValue = dataframe.iloc[indexInstance]['Currency']
    if 'Price' in columnHeadingsPresent:
      return 'Instance type: ' + instancePresent + ', ' + columnHeadingsPresent + ': ' + str(dataValue) + ', ' + 'Unit: ' + unitValue + ', ' + 'Currency: ' + currencyValue
    else:
      return 'Instance type: ' + instancePresent + ', ' + columnHeadingsPresent + ': ' + str(dataValue)
    #get corresponding value of column value and store it
  
  else:
    return False
    
  return result
  

def test3(input):
  selectedPhrase= ''
  triggerPhraseDict = { 'compute':['c5', 'c4'], 'memory':['x1', 'r5', 'r4', 'z1d'], 'accelerated':['p3','p2','g3','f1'], 'general':['t3','t2','m5','m4'],'storage':['h1','i3','d2'] } 
  triggerPhrases = triggerPhraseDict.keys()
  result = []
  for phrase in triggerPhrases:
    if phrase in input:
      selectedPhrase = phrase
      for instance in instances:
          for keyInstance in triggerPhraseDict[selectedPhrase]:
            if keyInstance in instance:
              result.append(instance)
              
  result = list(set(result))
  stringResult = ''
  
  for item in result:
    stringResult += item
    stringResult += ', '
  #print(result)
  if not stringResult:
    return False
  return stringResult
  
def smallTalk(input):
  if 'hello' in input:
    return "Greetings"
  if 'hi' in input:
    oneWordCheck = re.compile(r'\b({0})\b'.format('hi'), flags=re.IGNORECASE).search
    result = oneWordCheck(input)
    if result:
      return "Greetings"
  if 'how' in input:
    return "I'm good thanks"
  if 'thank' in input:
    return "no problem"
  if 'bye' in input:
    return 'bye'
  return False

dataframeAzure['Name'] = dataframeAzure['Name'].str.lower()
instancesAzure= dataframeAzure['Name'].tolist()
#print(instancesAzure)
columnHeadingsAzure = dataframeAzure.columns.values.tolist()
#print(columnHeadings)
columnHeadingsAzure = ['memory','core']

def azureDetails(input):
  instanceAzure = ''
  columnPresent = ''
  for instance in instancesAzure:
    if instance in input:
      instanceAzure = instance
  
  for column in columnHeadingsAzure:
    if column in input:
      columnPresent = column
      
  if instanceAzure and columnPresent:
    indexInstance = instancesAzure.index(instanceAzure)
    memoryValue = dataframeAzure.iloc[indexInstance]['MemoryInMB']
    coresValue = dataframeAzure.iloc[indexInstance]['NumberOfCores']
    if 'memory' in columnPresent:
      return 'VM: ' + str(instanceAzure) + ', ' + 'Memory(Mb): ' + str(memoryValue)
    if 'core' in columnPresent:
      return 'VM: ' + str(instanceAzure) + ', ' + 'Cores: ' + str(coresValue)
  else:
    return False
    
def findResult(input):
  outcome1 = test1(input)
  outcome2 = azureDetails(input)
  outcome3 = smallTalk(input)
  outcome4 = test3(input)
  
  if outcome1:
    return outcome1
  if outcome2:
    return outcome2
  if outcome3:
    return outcome3
  if outcome4:
    return outcome4
  return 'Please include more information. See the examples for help.'


#variable = smallTalk(stringExample)
#print(variable)

#var = findResult(stringExample)
#print(var)

#var = azureDetails(stringExample)
#print(var)
#print(instances)
#test2()
app.run(port=port)

