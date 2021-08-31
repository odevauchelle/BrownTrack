import sys
sys.path.append('./../')

figure_path = '../figures/'

import BrownTrack as BT

from pylab import *

X1 = rand( 5, 2 )
X2 = X1 + .2*( rand( *shape( X1 ) ) - .5 )
X2[0] += 0.5

fig, axs = subplots( ncols = 2, figsize = (8,6) )

for ax in axs :
    ax.plot( *X1.T, 'o' )
    ax.plot( *X2.T, 'o' )

for i, length in enumerate( [ 1, 0.2 ] ) :

    for link in BT.assign( X1, X2, length ) :

        if link[0] == link[1] : # then the pairing is correct
            linestyle = '-'
        else :
            linestyle = ':'

        axs[i].plot( *array( [ X1[ link[0] ], X2[ link[1] ] ] ).T, color = 'grey', linestyle = linestyle, zorder = -1 )
        axs[i].set_title( 'length=' + str(length) )


for ax in axs :
    ax.axis('scaled')
    ax.set_xticks([])
    ax.set_yticks([])

# savefig(figure_path + 'assignment_too_far.svg', bbox_inches = 'tight' )


show()
