
import sys
sys.path.append('./../')

figure_path = '../figures/'

import BrownTrack as BT
from pylab import *

swarm = BT.bunch( live_trajectories = [], dead_trajectories = [] )

for _ in range(5) :

    new_trajectory = BT.trajectory( X = rand( 2 ) )
    swarm.addTrajectory( new_trajectory )

print( swarm.live_trajectories )
print( swarm.dead_trajectories )

for _ in range(10):

    tracks = []
    new_points = []

    for traj_index in range( len( swarm.live_trajectories ) ) :

        new_points += [ array( swarm.live_trajectories[traj_index].getEnd() ) + 0.2*( rand( 2 ) - .5 ) ]
        tracks += [ [ traj_index ]*2 ]

    swarm.grow( tracks = tracks, new_points = new_points )

for trajectory in swarm.live_trajectories :
    plot( trajectory.x, trajectory.y )

axis('equal')

# savefig(figure_path + 'bunch.svg', bbox_inches = 'tight' )

show()
