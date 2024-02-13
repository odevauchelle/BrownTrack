figure_path = '../figures/'

import sys
sys.path.append('./../')

import BrownTrack as BT
from pylab import *

# domain = BT.domain( 'Circle', { 'xy' : ( 0, 0 ), 'radius' : 1  } )
#
theta = linspace(0,2*pi, 18 )
box = BT.domain( 'Polygon', { 'xy' : array( [ 1 + cos(theta), sin(theta) ] ).T  } )
# box = BT.domain('Circle', {'xy' : (0,1), 'radius': 30})
for expansion_factor in [1., .5, 1.2] :

    box.resize( expansion_factor )

    print('area:', box.get_area()/expansion_factor**2 )
    gca().add_patch( box.get_patch() )

    box.resize( 1/expansion_factor )

axis('scaled')
xticks([]); yticks([])

# savefig(figure_path + 'domain_2.svg', bbox_inches = 'tight')

show()
