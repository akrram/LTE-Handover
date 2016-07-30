# LTE-Handover and Mobility Prediction 

We have two main classes [class eNB, class UE] that store the information related to both the cellular tower
and user equipment. The next step involved is creating a reasonable probability transition matrix within a grid
of a NxN dimensions. In our implementation, N = 500 miles. The probabilities were chosen based on their
distances to each other, giving the closest stations to one node a higher probability. The dimensions of the
matrix is simply MxM, where M = number of stations within the grid. The initial distribution of each station is
instantiated with respect to each user that is in the grid. The values are also chosen with respect to the
location of the user to the other stations, the speed of the user, and the Signal-to-Noise ratio of the channel
also with respect to the user and a certain eNB station.
After the transition matrix and the initial distribution have been created, the simulation is run using the
Markov transition property for each time step [one hour] into the future, generating a newer distribution for
each station as time passes. The predicted station is simply the maximum probability value of the distribution. 
