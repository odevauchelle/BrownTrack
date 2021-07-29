
import sys
sys.path.append('./../')

figure_path = '../figures/'

import BrownTrack as BT

traj = BT.trajectory( X = ( 0, 0 ) )

from pylab import *

for _ in range(5) :
    traj.addPoint( rand(2) )

figure()
plot( traj.x, traj.y, 'o-' )
axis('scaled')
savefig( figure_path + 'simple_trajectory.svg', bbox_inches = 'tight')


show()
