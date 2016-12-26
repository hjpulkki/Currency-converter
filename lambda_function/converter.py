import math
import csv
import sys

DELIMITER = ','
FILENAME = 'formulas.csv'
FRAC = "\\frac{"
CDOT = " \\cdot "


def find_est(rate, estimates):
 result = {}
 result['rate'] = rate
   
 exponent = math.floor(math.log(rate,10))
 rate /= 10**exponent
 print(exponent)
 print(rate)

 multStr = "1"
 for i in range(0,abs(int(exponent))):
  multStr += "0"

 error_tuples = []
 for estimate in estimates:
  error = abs(estimate[0]-rate)/rate
  error_tuples.append([error, estimate])
 error_tuples = sorted(error_tuples, key=lambda est: -est[0])
 
 diff = 99
 result['formulas'] = []
 while error_tuples:
  est = error_tuples.pop()
  #print(est, diff)
  if est[1][1] < diff:
   #print("(" + est[1][2] + ")" + multStr, est)
   formula = {}
   if exponent > 0:
    formula['expression'] = est[1][2] + CDOT + multStr
   else:
    if exponent < 0:
     formula['expression'] = FRAC + est[1][2] + "}{" + multStr + "}"
    else:
     formula['expression'] = est[1][2]
	
   formula['error'] = est[0]
   formula['rate'] = est[1][0]*10**exponent
   formula['difficulty'] = est[1][1]
   result['formulas' ].append(formula)
   diff = est[1][1]
 return result
   
def loadEstimates(filename):
 with open(filename, 'r') as file:
  estimates = []
  filereader = csv.reader(file, delimiter=DELIMITER)
  for row in filereader:
   estimates.append([float(row[0]), int(row[1]), str(row[2])])
  return estimates
     
def handler(event, context):
 if 'rate' in event:
  rate = float(event['rate'])
  estimates = loadEstimates(FILENAME)
  return find_est(rate,estimates)
 else:
  raise Exception("No rate given")
  
#print(handler({'rate': sys.argv[1]}, None))
