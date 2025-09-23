import matplotlib.pyplot as plt
import re
import numpy as np

dataPoints = []
testData = []

def eucledian_distance(p1, p2, q1 , q2):
    distance = np.sqrt((p1 - q1)**2 + (p2 - q2)**2)
    return distance

with open("datapoints.txt", "r") as textfile:
    for line in textfile:
        row = line.strip().split(", ")

        dataPoints.append(row)

with open("testpoints.txt", "r") as test:
    for line in test:
        row = line.strip().split()
        testData.append(row)

testData.pop(0)
testData = [[x[1], x[2]] for x in testData]

cleanedTestData = []
for row in testData:
    new_Row = []
    for i in row:
        cleaned = re.sub(r"[(),]", "", i)
        new_Row.append(float(cleaned))
    cleanedTestData.append(new_Row) 


dataPoints[0] = ["Width cm", "Height cm", "Lable"]

pointsGroup0 = [[float(i) for i in x] for x in dataPoints if x[2] == "0"]
pointsGroup1 = [[float(i) for i in x] for x in dataPoints if x[2] == "1"]

dataPointsClean = pointsGroup0 + pointsGroup1

pointsGroup0 = [(x[0], x[1]) for x in pointsGroup0]
pointsGroup1 = [(x[0], x[1]) for x in pointsGroup1]

Pichu_x = [x[0] for x in pointsGroup0]
Pichu_y = [x[1] for x in pointsGroup0]

Pikatchu_x = [x[0] for x in pointsGroup1]
Pikatchu_y = [x[1] for x in pointsGroup1]

Test_x = [x[0] for x in cleanedTestData]
Test_y = [x[1] for x in cleanedTestData]

k = 1

distancesFromTest = []

for pointX, pointY in zip(Test_x, Test_y):
    distances = []
    for point in dataPointsClean:
        distancefromTest = eucledian_distance(pointX, pointY, point[0], point[1])
        distances.append((distancefromTest, point[2]))

    distances.sort()    
    distancesFromTest.append(distances)
i = 0
for testpoint in distancesFromTest:
    
    Pikatchu_Neighbors = [x for x in testpoint[:k] if x[1] == 1]
    if len(Pikatchu_Neighbors) > k/2:
        print(f"{cleanedTestData[i]} classified as Pikatchu")
    else:
        print(f"{cleanedTestData[i]} classified as Pichu")
    i += 1
    

plt.figure(dpi= 100)
plt.scatter(Pichu_x, Pichu_y, color="#fffb00", alpha= 0.6, label= "Pichu")
plt.scatter(Pikatchu_x, Pikatchu_y, color="#0000ff", alpha= 0.6, label= "Pikatchu")
plt.scatter(Test_x, Test_y, color="#ff0000", alpha= 0.8, label= "Test Data")
plt.xlabel("Width cm")
plt.ylabel("Height cm")
plt.legend()
plt.show()