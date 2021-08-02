
import sys
sys.path.append('./../')

figure_path = '../figures/'

import BrownTrack as BT
from pylab import *

aggregate = BT.bunch( live_trajectories = [], dead_trajectories = [] )

for theta in linspace(0,2*pi,15)[:-1] :

    new_trajectory = BT.trajectory( X = [ 0, 0 ] )
    new_trajectory.addPoint( [ cos(theta), sin(theta) ] )
    aggregate.addTrajectory( new_trajectory )

for _ in range(500) :

    radii = [ norm( point ) for point in aggregate.getEnds() ]
    new_radii = max(radii) + rand()
    new_angle = 2*pi*rand()
    new_point = array( [ new_radii*cos(new_angle), new_radii*sin(new_angle) ] )

    distances = [ norm( array( point ) -  new_point ) for point in aggregate.getEnds() ]

    aggregate.live_trajectories[ argmin(distances) ].addPoint( new_point )


for trajectory in aggregate.live_trajectories :
    plot( trajectory.x, trajectory.y )

axis('equal')
show()
