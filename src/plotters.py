import matplotlib.pyplot as plt

from .simulation import Simulation
from .journal import message

def plotOptimizationResults( initialParams, optParams ):

    for sim in Simulation.all_simulations:
        
        initialX, initialY = sim.run( initialParams )
        optX, optY = sim.run( optParams )
        
        plt.figure()
        plt.plot( sim.data[:,0], sim.data[:,1], "x", 
                label= "given data",
                markersize=5) 
        plt.plot( initialX, initialY, label="initial params" )
        plt.plot( optX, optY, label="optimal params" )
        plt.legend()
        plt.grid()
        plt.savefig(sim.name + ".pdf" )
        message( " --> " + sim.name +".pdf" )

