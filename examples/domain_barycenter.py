figure_path = '../figures/'


import sys
sys.path.append('./../')

import BrownTrack as BT
from pylab import *

# domain = BT.domain( 'Circle', { 'xy' : ( 0, 0 ), 'radius' : 1  } )
#
theta = linspace(0,2*pi, 15 )[::-1]
domain = BT.domain( 'Polygon', { 'xy' : ( array( [ cos(theta)*(cos(theta)>=0), sin(theta)] ) ).T  } )

print('area:', domain.get_area() )

patch = domain.get_patch()
patch.set( facecolor = 'tab:blue', alpha = .5 )
gca().add_patch( patch )
plot(0,0,'+', color = 'k')
print( domain.get_barycenter() )
plot( *domain.get_barycenter(),'+', color = 'tab:red')


axis('scaled')
xticks([]); yticks([])

# savefig(figure_path + 'domain_2.svg', bbox_inches = 'tight')

show()
