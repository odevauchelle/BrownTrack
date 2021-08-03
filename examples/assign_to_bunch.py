
import sys
sys.path.append('./../')

figure_path = '../figures/'

import BrownTrack as BT
from pylab import *

bunch = BT.bunch( live_trajectories = [], dead_trajectories = [] )

for t in range(40) :
    bunch.assign( rand( 20, 2 ), mismatch_length = .3, t = t )

for trajectory in bunch.dead_trajectories :
    plot( trajectory.x, trajectory.y, color = 'grey' )

for trajectory in bunch.live_trajectories :
    plot( trajectory.x, trajectory.y, color = 'tab:blue' )

axis('scaled')


figure( figsize = (6,3) )
h = 0

for traj in bunch.dead_trajectories :
    plot( [ traj.birth_time, traj.end_time ], [h]*2, color = 'grey' )
    h += 1

for traj in bunch.live_trajectories :
    plot( [ traj.birth_time, traj.end_time ], [h]*2, color = 'tab:blue' )
    h += 1

yticks([])
xlim(0,t)




show()
