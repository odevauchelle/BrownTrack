figure_path = '../figures/'


import sys
sys.path.append('./../')

import BrownTrack as BT
from pylab import *

theta = linspace( 0, 2*pi, 7 )

domain = BT.domain( 'Circle', { 'xy' : ( 0, 0 ), 'radius' : 1  } )
gca().add_patch( domain.get_patch() )

theta = linspace( 0, pi, 30 )
r = 1.2*cos(3*theta)
x = r*cos(theta)
y = r*sin(theta)

traj = BT.trajectory( points = array( [x, y ] ).T  )



plot( traj.x, traj.y, color = 'grey' )

inside, outside = domain.cookie_cutter( traj )


for traj in inside :
    plot( traj.x, traj.y, marker = '.', color = 'tab:blue' )

for traj in outside :
    plot( traj.x, traj.y, marker = '.', color = 'tab:orange' )

axis('scaled')
xticks([]); yticks([])
show()
