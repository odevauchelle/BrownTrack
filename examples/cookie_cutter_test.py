figure_path = '../figures/'


import sys
sys.path.append('./../')

import BrownTrack as BT
from pylab import *

theta = linspace( 0, 2*pi, 8 )

#domain = BT.domain( 'Circle', { 'xy' : ( 0, 0 ), 'radius' : 1  } )
domain = BT.domain( 'Polygon', { 'xy' : array( [ cos(theta), sin(theta) ] ).T  } )


theta = linspace( 0, pi, 61 )[1:-1]

trajectories = []

for k in range(3,9) :
    r = 1.2*cos(k*theta)
    x = r*cos(theta)
    y = r*sin(theta)

    traj = BT.trajectory( points = array( [x, y ] ).T  )

    plot( traj.x, traj.y, color = 'grey' )

    trajectories += [traj]


# savefig(figure_path + 'trifolium.svg', bbox_inches = 'tight')


inside, outside = domain.cookie_cutter( trajectories )
print( len( inside ), len( outside ) )


for traj in inside :
    print( len( traj.x ) )
    plot( traj.x, traj.y, marker = '.', color = 'tab:blue' )

print('----------------')

for traj in outside :
    print(len(traj.x))
    plot( traj.x, traj.y, marker = '.', color = 'tab:orange' )


gca().add_patch( domain.get_patch() )

axis('scaled')
xticks([]); yticks([])

# savefig(figure_path + 'trifolium_2.svg', bbox_inches = 'tight')


show()
