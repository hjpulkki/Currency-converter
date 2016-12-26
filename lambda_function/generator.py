import converter
import sys

TOLERANCE = 0.0001

def plusminus(sign):
 if sign < 0:
  return "-"
 return "+"

 # Remove duplicates from the formula array. If two estimates give a rate within the TOLERANCE, the more difficult one will be removed from the array.
def cleanDuplicates(estimates):

 estimates_new = []
 while estimates:
  est1 = estimates.pop()
  flag = 1
  for est2 in estimates_new:
   if est1[0] < est2[0]*(1+TOLERANCE) and est1[0] > est2[0]*(1-TOLERANCE):
    if est1[1] >= est2[1]:
     flag = 0
    else:
     estimates_new.remove(est2)
    break
  if flag:
   estimates_new.append(est1)
 return estimates_new

 
def addEstimate(est1,estimates_new,estimates_final,diff_level):
 if est1[0] < 0.005 or est1[0] > 150:
  return [estimates_new,estimates_final]
 if est1[1] > diff_level:
  return [estimates_new,estimates_final]

 flag = 1
 for est2 in estimates_new:
  if est1[0] < est2[0]*(1+TOLERANCE) and est1[0] > est2[0]*(1-TOLERANCE):
   if est1[1] >= est2[1]:
    flag = 0
   else:
    estimates_new.remove(est2)
   break

 if flag:

  for est2 in estimates_final:
   if est1[0] < est2[0]*(1+TOLERANCE) and est1[0] > est2[0]*(1-TOLERANCE):
    if est1[1] >= est2[1]:
     flag = 0
    else:
     estimates_final.remove(est2)
    break

  estimates_new.append(est1)

 return [estimates_new,estimates_final]


# Generate all formulas with difficulty less than diff_level
def generateEstimates(diff_level):
 # value, difficulty, formula as string
 operators = [
				[lambda x: x*2, 2, lambda x: x + converter.CDOT + "2"],
				[lambda x: x*10, 1, lambda x: x + converter.CDOT + "10"],
				[lambda x: x*3, 4, lambda x: x + converter.CDOT + "3"],
				[lambda x: x/10.0, 1, lambda x: converter.FRAC + x + "}{10}"],
				[lambda x: x/2.0, 2, lambda x: converter.FRAC + x + "}{2}"],
				[lambda x: x*3.0, 6, lambda x: converter.FRAC + x + "}{3}"]
			]

 estimates_new = [[1, 0, "x"]]
 estimates_final = []

 i = 0
 while estimates_new:
  i += 1
  estimate = estimates_new.pop()

  for operator in operators:
   new_estimate = [operator[0](estimate[0]), operator[1]+estimate[1], operator[2](estimate[2])]
   [estimates_new, estimates_final] = addEstimate(new_estimate,estimates_new,estimates_final,diff_level)

  for estimate2 in estimates_new+estimates_final:
   for sign in [-1,1]:
    new_estimate = [estimate[0] + sign*estimate2[0],estimate[1]+estimate2[1]+3,"(" + estimate[2] + plusminus(sign) + estimate2[2] + ")"]
    [estimates_new,estimates_final] = addEstimate(new_estimate,estimates_new,estimates_final,diff_level)

  estimates_final.append(estimate)
  if i%100 == 0:
   estimates_final = cleanDuplicates(estimates_final)
   #print(len(estimates_new), len(estimates_final))

 estimates_final = cleanDuplicates(estimates_final)
 estimates_final = sorted(estimates_final, key=lambda est: -est[0])
 return estimates_final

# Save results in a csv file.
def saveEstimates(estimates):
 file = open(converter.FILENAME,'w')
 for est in estimates:
  if est[0] >= 0.1 and est[0] <= 10:
   file.write(str(est[0]) + converter.DELIMITER + str(est[1]) + converter.DELIMITER + str(est[2]) + '\n')

# Get input argument as maximum difficulty
max_diff = int(sys.argv[1])

# Generate formulas for starting from difficulty 1.
for diff in range(max_diff+1):
 estimates = generateEstimates(diff)
 saveEstimates(estimates)
 print("Estimates for difficulty", diff, "succesfully generated")