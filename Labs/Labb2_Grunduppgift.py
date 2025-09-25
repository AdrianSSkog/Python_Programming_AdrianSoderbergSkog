import matplotlib.pyplot as plt
import re
import numpy as np

def euclidean_distance(p1, p2, q1 , q2):
    distance = np.sqrt((p1 - q1)**2 + (p2 - q2)**2)
    return distance

def read_file(filename, delimiter= ", "):
    with open(filename, "r") as textfile:
        readed_file = []
        for line in textfile:
            row = line.strip().split(delimiter)
            readed_file.append(row)
    return readed_file

def split_x_and_y(data):
    x = [p[0] for p in data]
    y = [p[1] for p in data]
    return x, y

def Sort_by_Label(data):
    group0 = [[float(i) for i in x] for x in data if x[2] == "0"]
    group1 = [[float(i) for i in x] for x in data if x[2] == "1"]
    return group0, group1

def Clean_Test_Data(testData):
    testData.pop(0)
    data = [[x[1], x[2]] for x in testData]

    cleanedTestData = []
    for row in data:
        new_Row = []
        for i in row:
            cleaned = re.sub(r"[(),]", "", i)
            new_Row.append(float(cleaned))
        cleanedTestData.append(new_Row)
    return cleanedTestData

def plott_Points(x1, y1, x2, y2, t1, t2, u1, u2):
    plt.figure(dpi= 100)
    plt.scatter(x1, y1, color="#fffb00", alpha= 0.6, label= "Pichu")
    plt.scatter(x2, y2, color="#0000ff", alpha= 0.6, label= "Pikatchu")
    plt.scatter(t1, t2, color="#ff0000", marker= "x", alpha= 0.8, label= "Test Data")
    plt.scatter(u1, u2, color="#0eab00", marker= "x", alpha= 0.8, label= "User Data")
    plt.xlabel("Width cm")
    plt.ylabel("Height cm")
    plt.legend()
    plt.show()

def meassure_distances(datapoints, TestX, TestY):
    distancesFromTest = []

    for pointX, pointY in zip(TestX, TestY):
        distances = []
        for point in datapoints:
            distancefromTest = euclidean_distance(pointX, pointY, point[0], point[1])
            distances.append((distancefromTest, point[2]))

        distances.sort()    
        distancesFromTest.append(distances)
    return distancesFromTest

def Classify(distances, TestData, k = 1): 
    i = 0
    classifiedPoints = []
    for testpoint in distances:
        
        Pikatchu_Neighbors = [x for x in testpoint[:k] if x[1] == 1]
        if len(Pikatchu_Neighbors) > k/2:
            classifiedPoints.append(f"Point {i+1} {TestData[i]} classified as Pikatchu")
        else:
            classifiedPoints.append(f"Point {i+1} {TestData[i]} classified as Pichu")
        i += 1
    return classifiedPoints

def Collect_from_user(numberOfPoints = 1):
    UserDataPoints = []
    for i in range(numberOfPoints):
        while True:
            try:
                userPoint_X = float(input(f"Point {i+1} - Enter the width in cm: "))
                userPoint_Y = float(input(f"Point {i+1} - Enter the height in cm: "))
                if userPoint_X <= 0 or userPoint_Y <= 0:
                    raise ValueError("Invalid input! Values for height and width must be a positive number")
            except ValueError:
                print("Invalid input, enter only numbers")
                continue
            else:
                UserDataPoints.append([userPoint_X, userPoint_Y])
                break
    return UserDataPoints

def main():
    dataPoints = read_file("datapoints.txt", ", ")
    testData = read_file("testpoints.txt", " ")
    cleanTestData = Clean_Test_Data(testData)

    dataPoints[0] = ["Width cm", "Height cm", "Lable"]

    pointsGroup0, pointsGroup1 = Sort_by_Label(dataPoints)

    dataPointsClean = pointsGroup0 + pointsGroup1

    Pichu = [(x[0], x[1]) for x in pointsGroup0]
    Pikatchu = [(x[0], x[1]) for x in pointsGroup1]

    Pichu_x, Pichu_y = split_x_and_y(Pichu)
    Pikatchu_x, Pikatchu_y = split_x_and_y(Pikatchu)
    Test_x, Test_y = split_x_and_y(cleanTestData)

    distancesTest = meassure_distances(dataPointsClean, Test_x, Test_y)
    classifiedTestData = Classify(distancesTest, cleanTestData, k = 1)

    UserData = Collect_from_user(4)
    User_X, User_Y = split_x_and_y(UserData)
    distancesUser = meassure_distances(dataPointsClean, User_X, User_Y)
    classifiedUserData = Classify(distancesUser, UserData, k = 10)

    print("Test data: ")
    for p in classifiedTestData:
        print(p)
    print("User data: ")
    for p in classifiedUserData:
        print(p)

    plott_Points(Pichu_x, Pichu_y, Pikatchu_x, Pikatchu_y, Test_x, Test_y, User_X, User_Y)

main()