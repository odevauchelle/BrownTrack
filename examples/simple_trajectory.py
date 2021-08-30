
import sys
sys.path.append('./../')

figure_path = '../figures/'

import BrownTrack as BT

traj = BT.trajectory( X = ( 0, 0 ) )

print( isinstance( traj, BT.trajectory ) )

from pylab import *

for _ in range(5) :
    point = rand(2)
    # plot( *point, 'o' )
    traj.addPoint( point )


plot( traj.x, traj.y, '.-' )
axis('scaled')
# savefig( figure_path + 'simple_trajectory.svg', bbox_inches = 'tight')

print( traj.x )
print(type(traj.x[3]))

show()
