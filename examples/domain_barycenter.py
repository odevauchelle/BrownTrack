figure_path = '../figures/'


import sys
sys.path.append('./../')

import BrownTrack as BT
from pylab import *

# domain = BT.domain( 'Circle', { 'xy' : ( 0, 0 ), 'radius' : 1  } )
#
theta = linspace(0,2*pi, 100 )[::-1]
domain = BT.domain( 'Polygon', { 'xy' : array( [ 0.5*cos(theta), ( 1 - 0.8*cos(3*theta) )*sin(theta) ] ).T  } )

print('area:', domain.get_area() )

gca().add_patch( domain.get_patch() )
plot(*domain.get_barycenter(),'+')


axis('scaled')
xticks([]); yticks([])

# savefig(figure_path + 'domain_2.svg', bbox_inches = 'tight')

show()
