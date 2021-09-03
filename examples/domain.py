figure_path = '../figures/'


import sys
sys.path.append('./../')

import BrownTrack as BT
from pylab import *

# domain = BT.domain( 'Circle', { 'xy' : ( 0, 0 ), 'radius' : 1  } )
#
theta = linspace(0,2*pi, 8 )
domain = BT.domain( 'Polygon', { 'xy' : array( [ cos(theta), sin(theta) ] ).T  } )

print('area:', domain.get_area() )

gca().add_patch( domain.get_patch() )

axis('scaled')
xticks([]); yticks([])

# savefig(figure_path + 'domain_2.svg', bbox_inches = 'tight')

show()
