import sys
sys.path.append('./../')

figure_path = '../figures/'

import BrownTrack as BT

from pylab import *

X1 = rand( 3, 2 )
X2 = X1 + .2*( rand( *shape( X1 ) ) - .5 )

plot( *X1.T, 'o' )
plot( *X2.T, 'o' )

links = BT.assign( X1, X2, 1 )
print(links)

for link in links :

    if link[0] == link[1] : # then the pairing is correct
        linestyle = '-'
    else :
        linestyle = ':'

    plot( *array( [ X1[ link[0] ], X2[ link[1] ] ] ).T, color = 'grey', linestyle = linestyle, zorder = -1 )

axis('scaled')
xticks([])
yticks([])

savefig(figure_path + 'assignment.svg', bbox_inches = 'tight' )


show()
