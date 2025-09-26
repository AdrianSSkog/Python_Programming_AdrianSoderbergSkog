import matplotlib.pyplot as plt
import re
import numpy as np
import statistics 

def euclidean_distance(p1, p2, q1 , q2):
    distance = np.sqrt((p1 - q1)**2 + (p2 - q2)**2)
    return distance

def read_file(filename, delimiter= ", "):
#Läser in textfiler och returnerar en 2D lista med strings
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
#Tar bort allt onödigt och ger tillbaka endast värden för bredd och höjd.
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

def plot_Points(x1, y1, x2, y2, tx, ty, ux, uy):
    plt.figure(dpi= 100)
    plt.scatter(x1, y1, color="#c7a900", alpha= 0.6, label= "Pichu")
    plt.scatter(x2, y2, color="#0000ff", alpha= 0.6, label= "Pikatchu")
    plt.scatter(tx, ty, color="#ff0000", marker= "+", alpha= 0.8, label= "Test Data")
    plt.scatter(ux, uy, color="#18f005", marker= "*", alpha= 0.8, label= "User Data", s= 150, edgecolors= "#4B1905")
    plt.xlabel("Width cm")
    plt.ylabel("Height cm")
    plt.legend()
    plt.show()

def meassure_distances(datapoints, UnlabeldX, UnlabeldY): 
#Räknar ut euklidiskt avstånd mellan de oidentifierade punkterna och alla träningspunkter.
#Returnerar en lista med alla avstånd sorterade i storleksordning ihop med punkternas label.
    distancesFromTest = []

    for pointX, pointY in zip(UnlabeldX, UnlabeldY):
        distances = []
        for point in datapoints:
            distancefromTest = euclidean_distance(pointX, pointY, point[0], point[1])
            distances.append((distancefromTest, point[2]))

        distances.sort()    
        distancesFromTest.append(distances)
    return distancesFromTest

def Classify(distances, TestData, k = 1): 
#Använder K nearest neighbors för att klassifiera punkter. 
#Man kan skicka in önskat k-värde annars används 1 som default. 
    classifiedPoints = []
    
    for i, testpoint in enumerate(distances):
        
        Pikatchu_Neighbors = [x for x in testpoint[:k] if x[1] == 1]
        if len(Pikatchu_Neighbors) > k/2:
            classifiedPoints.append(f"Point {i+1} {TestData[i]} classified as Pikatchu")
        else:
            classifiedPoints.append(f"Point {i+1} {TestData[i]} classified as Pichu")
    return classifiedPoints

def Collect_from_user(numberOfPoints = 1):
#De nummer som du skickar in avgör hur många punkter du hämtar från användaren. 
    UserDataPoints = []
    for i in range(numberOfPoints):
        while True:
            try:
                userPoint_X = float(input(f"Point {i+1} - Enter the width in cm: "))
                userPoint_Y = float(input(f"Point {i+1} - Enter the height in cm: "))
                if userPoint_X <= 0 or userPoint_Y <= 0:
                    raise ValueError("Invalid input! Values for height and width must be a positive number")
            except ValueError:
                print("Invalid input! Enter numbers only")
                continue
            else:
                UserDataPoints.append([userPoint_X, userPoint_Y])
                break
    return UserDataPoints

def training_test_split(datapoints):
    datapoints = np.array(datapoints[1:], dtype= float)
    Group0 = datapoints[datapoints[:,2] == 0]
    Group1 = datapoints[datapoints[:,2] == 1]

    np.random.shuffle(Group0)
    np.random.shuffle(Group1)

    training = np.vstack((Group0[:50], Group1[:50]))
    test = np.vstack((Group0[50:], Group1[50:]))
    np.random.shuffle(training)
    np.random.shuffle(test)
    return training, test

def calculate_accuracy(TP, TN, FP, FN):
    accuracy = (TP + TN)/sum([TP, TN, FP, FN])
    return accuracy

def compare_Predicted_Actual(actual, predicted):
    TP, TN, FP, FN = 0, 0, 0, 0
    for a, p in zip(actual, predicted):
        if a == 0 and p == 0:
            TN += 1
        elif a == 1 and p == 1:
            TP += 1
        elif a == 0 and p == 1:
            FP += 1 
        elif a == 1 and p == 0:
            FN += 1
    return TP, TN, FP, FN

def plot_accuracy(accuracy, repetitions, mean):
    x = [i+1 for i in range(repetitions)]
    plt.figure(dpi= 100)
    plt.plot(x, accuracy, color= "#0000ff", label= "Accuracy")
    plt.axhline(mean, color="#ff0000", linestyle= "--", label= f"Average = {mean:.2%}")
    plt.legend()
    plt.xlabel("Repetition")
    plt.ylabel("Accuracy")
    plt.show()

def main_basic():
#Huvudfunktionen för grunduppgifterna
#Printar ut resultatet för testpunkt som matas in av användaren 
#Printar också ut resultatet för de 4 testpunkterna
    dataPoints = read_file("datapoints.txt", ", ")
    testData = read_file("testpoints.txt", " ")
    cleanTestData = Clean_Test_Data(testData)

    dataPoints[0] = ["Width cm", "Height cm", "Label"]
    pointsGroup0, pointsGroup1 = Sort_by_Label(dataPoints)
    dataPointsClean = pointsGroup0 + pointsGroup1

    Pichu = [(x[0], x[1]) for x in pointsGroup0]
    Pikatchu = [(x[0], x[1]) for x in pointsGroup1]

    Pichu_x, Pichu_y = split_x_and_y(Pichu)
    Pikatchu_x, Pikatchu_y = split_x_and_y(Pikatchu)
    Test_x, Test_y = split_x_and_y(cleanTestData)

    distancesTest = meassure_distances(dataPointsClean, Test_x, Test_y)
    classifiedTestData = Classify(distancesTest, cleanTestData, k = 10)

    UserData = Collect_from_user(1) 
    User_X, User_Y = split_x_and_y(UserData)
    distancesUser = meassure_distances(dataPointsClean, User_X, User_Y)
    classifiedUserData = Classify(distancesUser, UserData, k = 10)

    print("Test data: ")
    for p in classifiedTestData:
        print(p)
    print("User data: ")
    for p in classifiedUserData:
        print(p)

    plot_Points(Pichu_x, Pichu_y, Pikatchu_x, Pikatchu_y, Test_x, Test_y, User_X, User_Y)

def main_bonus():
#Huvudfunktionen för bonusuppgifterna
    repetitions = 10
    accuracyList = []
    for i in range(repetitions):
        DataPoints = read_file("datapoints.txt", ", ")
        trainingData, testData = training_test_split(DataPoints)

        Test_X, Test_Y = split_x_and_y(testData)

        distances = meassure_distances(trainingData, Test_X, Test_Y)
        classifiedData = Classify(distances, testData, 10)

        predictions = []    #Konverterar den classifierade datan till lista med 1 och 0
        for row in classifiedData:
            if row.split()[-1] == "Pikatchu":
                predictions.append(1)
            elif row.split()[-1] == "Pichu":
                predictions.append(0)
        
        actualLabels = [int(x[2]) for x in testData]

        TP, TN, FP, FN = compare_Predicted_Actual(actualLabels, predictions)

        accuracy = calculate_accuracy(TP, TN, FP, FN)

        accuracyList.append(accuracy)
    mean = statistics.mean(accuracyList)

    print(f"The Average accuracy is {mean:.2%}")
    plot_accuracy(accuracyList, repetitions, mean)

#main_basic()
main_bonus()


"""
Källor:
AI25-Programmering - Lecture_notes
W3schools.com
chatGPT för felsökning och feedback
disskussioner med klasskanmrater
Strukturen är till viss del inspirerad av Hamids kod
"""