from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv('API_KEY')



import openpyxl

wb = openpyxl.load_workbook('US Uni Details.xlsx')
MainSheet = wb['Sheet1']

di = dict()

def stringSplit(inputString):
    finalStringList = list()
    #print(inputString)
    splitInputString = inputString.split(',')
    spiltInputStringLen = len(splitInputString)
    #print(splitInputString)

    for i in range(0, spiltInputStringLen):
            splitInputStringWithSpaces = splitInputString[i].split()
            finalStringList = finalStringList + [x.lower () for x in splitInputStringWithSpaces]
    return finalStringList

for college in range(1, 329):
    collegeName = list()
    collegeName.append(MainSheet.cell(row=college, column=2).value)
    finalCollegeName = list()
    collegeNameString = ''.join(collegeName)
    finalCollegeName = stringSplit(collegeNameString)

    for college in finalCollegeName:
        
        count = di.get(college, 0) + 1
        di[college] = count

temp = list()
for k,v in di.items():
    newt = (v,k)
    temp.append(newt)

temp = sorted(temp, reverse=True)

print(temp[:20])

