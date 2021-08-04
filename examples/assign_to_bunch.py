
import sys
sys.path.append('./../')

figure_path = '../figures/'

import BrownTrack as BT
from pylab import *

bunch = BT.bunch() # empty bunch

bunch.assign( [ [0,0] ] )
print(bunch.live_trajectories)

bunch.assign( [ [.1,0] ] )

for traj in bunch.live_trajectories :
    print( traj.x, traj.y )

bunch.assign( [ [.2,.1] ] )

print( len( bunch.live_trajectories ), len( bunch.dead_trajectories ) )

bunch.assign( [ [.2,.2] ], mismatch_length = .01 )


# for t in range(40) :
#     bunch.assign( rand( 20, 2 ), mismatch_length = .3, t = t )

for trajectory in bunch.dead_trajectories :
    plot( trajectory.x, trajectory.y, '-o', color = 'grey' )

for trajectory in bunch.live_trajectories :
    plot( trajectory.x, trajectory.y, '-o', color = 'tab:blue' )

axis('scaled')
yticks([]), xticks([])

savefig(figure_path + 'assign_to_bunch.svg', bbox_inches = 'tight' )

# figure( figsize = (6,3) )
# h = 0
#
# for traj in bunch.dead_trajectories :
#     plot( [ traj.birth_time, traj.end_time ], [h]*2, color = 'grey' )
#     h += 1
#
# for traj in bunch.live_trajectories :
#     plot( [ traj.birth_time, traj.end_time ], [h]*2, color = 'tab:blue' )
#     h += 1
#
# xlim(0,t)




show()
