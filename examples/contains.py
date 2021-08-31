
import sys
sys.path.append('./../')

figure_path = '../figures/'

import BrownTrack as BT
from pylab import *
from random import shuffle

center = ( 0.5, 0.5 )
radius = .3

# box = BT.domain( patch_type = 'Circle', boundary = { 'xy': center, 'radius' : radius } )
theta = linspace(0, 2*pi, 6)[1:]
box = BT.domain( patch_type = 'Polygon', boundary = { 'xy': array( [ center[0] + radius*cos(theta), center[1] + radius*sin(theta) ] ).T } )



gca().add_patch( box.get_patch( edgecolor = 'grey' ) )

points = rand( 100, 2 )
is_inside = box.contains( points )

plot( *points[is_inside].T, '.' )
plot( *points[~is_inside].T, '.' )

axis('scaled')
show()
