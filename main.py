#Akram B
#Nikhil U
#EE 122 SPRING 2016


from LTE import *
import numpy as np
import random



NUM_STATIONS = 10 # number of cellular stations

#possible of noise and signal strength and computation of SNR obtained from information page below
#http://www.speedguide.net/faq/how-to-read-rssisignal-and-snrnoise-ratings-440



SRRI_RANGE = range(-50,1)# range of average signal stength in dB
NOISE_RANGE = range(-120,-80) #range of noise level in dB

LOCATION_X = range(0,500)#0 to 500 possible x coordinates
LOCATION_Y = range(0,500)#0 to 500 possible x coordinates


SPEED_RANGE = range(0, 40)
STATIONS = []


#random locations, signal strength and noise. SNR is the difference between the two
# def generateStations():
for _ in range(NUM_STATIONS):
    pos = Location(random.choice(LOCATION_X), random.choice(LOCATION_Y))
    srri = random.choice(SRRI_RANGE)
    noise = random.choice(NOISE_RANGE)
    STATIONS.append( eNB(pos, srri, noise))

#computing inverse distances from one stations to all the other ones (used for transition probability matrix)
#closer distances get higher values :)
def computeInverseDistances():
    distanceDic = {}
    
    for stationA in STATIONS:
        distanceDic [stationA]= []
        for stationB in STATIONS:
            dif = euclideanD(stationA.location, stationB.location)
            if dif >0:
                distanceDic[stationA].append(1/dif)
            else:
                distanceDic[stationA].append(0)
    
    return distanceDic
    

def computeProbabilityMatrix(distanceDic):
    """Computes transition matrix, where P(i|j) represents the probability of transitioning from i to j
    
    We decided that the transition matrix should be determined by the normalized inverse-distance to other stations
    
    i.e. if A is closer to C than it is to B, then P(C|A) > P(B|A)
    """
    matrix_list = [normalize(distanceDic[station]) for station in distanceDic] #Normalize each row of the transition matrix so that they sum to 1
    return np.matrix(matrix_list)    # return the probability transition matrix
    

def normalize (values_list):
    """Divide a list of numbers by their sum in order to make list sum to 1    
    """
    total = sum(values_list)
    newList = []
    return [round(x/total, 5) for x in values_list]

def computeInitialDistribution(ue):       
    closestD = sorted([(i, euclideanD(STATIONS[i].location, ue.location)) for i in range(len(STATIONS))], key = lambda value: value[1])# return sorted list by distance
    
    finalUEparam = []
    
    scalar = 10000000# closest towers get higher scalar values
    dictScalar = {}
    for index, distance in closestD:
        dictScalar[index] = scalar
        scalar /=3
    
    
    for i in range(len(STATIONS)):
        total = abs(STATIONS[i].SNR)*1000
        if ue.speed != 0:
            time_to_destination = euclideanD(ue.location, ue.final_location)/ue.speed
            total += (1/time_to_destination)*1000*ue.speed
        total += dictScalar[i]
        finalUEparam.append(total)
    
    return normalize(finalUEparam)


def manhattanD(location_1, location_2):
    return abs(location_1[0]-location_2[0])+abs(location_1[1]-location_2[1])
    
def euclideanD (location_1, location_2):
    return math.sqrt(math.pow((location_1[0]-location_2[0]),2)+math.pow((location_1[1]-location_2[1]),2))

if __name__ == '__main__':        
    location_ue = Location(random.choice(LOCATION_X), random.choice(LOCATION_Y))
    
    speed = random.choice(SPEED_RANGE)
    final_location = Location(location_ue[0]+speed, location_ue[1]+speed)
    
    ue = UE(location_ue, final_location, speed)# creating the user
    print ('UE INFO: ',ue)
    print(' ' )
    print(' ' )
    probabilityMatrix = computeProbabilityMatrix(computeInverseDistances())
    initialDistribution = computeInitialDistribution(ue)

    ind = np.argmax(initialDistribution)
    
    print('Closest cellular eNB: ' +str(ind)+'  ' , STATIONS[ind])#print out closest compatiable station
    
    print(' ' )
    print(' ' )
    print('Initial Distribution', initialDistribution )
    print(' ' )
    print(' ' )
    print('Transition Probabilities', probabilityMatrix)
    print(' ' )
    
    
    
    for i in range (20):
        c =  initialDistribution*probabilityMatrix
        initialDistribution = c
        ind = np.argmax(c)
        
        print('Closest cellular eNB after ' +str(i+1)+' time steps: '+ str(ind), STATIONS[ind])#print out closest compatiable station
    
    
    
    print(' ' )
    print('Steady Distribution', initialDistribution )
