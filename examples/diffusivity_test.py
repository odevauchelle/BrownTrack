
import sys
sys.path.append('./../')

figure_path = '../figures/'

import BrownTrack as BT
from pylab import *
from random import shuffle

small_box = BT.domain( patch_type = 'Circle', boundary = { 'xy': ( 0.5, 0.5 ), 'radius' : .3 } )

points = rand(50,2)
is_inside = small_box.contains( points )



gca().add_patch( small_box.get_patch( edgecolor = 'grey' ) )

plot( *points[is_inside].T, '.' )
plot( *points[~is_inside].T, '.' )

axis('scaled')
show()
