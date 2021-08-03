from pylab import *
from munkres import Munkres

def build_cost_matrix( X1, X2, appaearance_prob_length, disappaearance_prob_length ) :

    N1 = len(X1)
    N2 = len(X2)

    cost_matrix = zeros( ( N1 + N2, N1 + N2 ) )

    for n1 in range(N1) :
        for n2 in range(N2) :
            dx = array( X2[n2] ) - array( X1[n1] )
            cost_matrix[ n1, n2 ] = dot( dx, dx )

    cost_matrix[ N1:, :N2 ] = zeros( ( N2, N2 ) ) + appaearance_prob_length**2
    cost_matrix[ :N1, N2: ] = zeros( ( N1, N1 ) ) + disappaearance_prob_length**2

    return cost_matrix

def find_proper_links( links, N1, N2 ) :

    proper_links = []

    for link in links :
        if link[0] < N1 and link[1] < N2 :
            proper_links += [ link ]

    return proper_links


def assign( X1, X2, mismatch_length ) :

    '''
    Pairs points from two list, trying to minimize the total distance, using the Kuhn-Munkres algorithm as implementend in the munkres library (https://pypi.org/project/munkres/).

    links = assign( X1, X2, appearance_prob_length, disappearance_prob_length )

    Arguments:
    X1: Set of points.
    X2: Set of points.
    mismatch_length: Length beyond which it's likely that X2 contains a point that doesn't match any point in X1, and vice versa. If mismatch_length is a couple of lenghts, they correspond to a disconnected point in X1 and X2, respectively.
    '''

    try :
        mismatch_length[1]
    except :
        mismatch_length = [mismatch_length]*2


    N1 = len(X1)
    N2 = len(X2)

    cost_matrix = build_cost_matrix( X1, X2, *mismatch_length )

    links = Munkres().compute( cost_matrix )

    links = find_proper_links( links, N1, N2 )

    return links


# def assign_to_bunch( points, bunch, mismatch_length, t ) :
#     '''
#     Convenience method that assigns new points to the trajectories of a bunch, create new trajectories when necessary, and kills the disconnected trajectories.
#
#     bunch = assign_to_bunch( points, bunch, mismatch_length, t )
#
#     Returns:
#     bunch: The bunch after assignement.
#     '''
#
#     try :
#         links = assign( bunch.getEnds(), points, mismatch_length )
#         new_point_indices =  list( set( range( len(points) ) ) - set ( [ link[1] for link in links ] ) )
#     except :
#         print( 'Link error at time ' + str(t) )
#
#     try :
#         bunch.grow( links, points )
#     except :
#         print( 'bunch.grow error at time ' + str(t) )
#
#     try :
#         disconnected_trajectories = list( set( range( len( bunch.live_trajectories ) ) ) - set ( [ link[0] for link in links ] ) )
#         bunch.kill( disconnected_trajectories )
#     except :
#         print( 'bunch.kill error at time ' + str(t) )
#
#     try :
#         for point in points[ new_point_indices ] :
#              bunch.addTrajectory( Trajectory( t, point ) )
#
#     except :
#         print( 'bunch.addTrajectory error at time ' + str(t) )
#
#     return bunch


if __name__ == '__main__' :

    X1 = rand( 20, 2 )
    X2 = X1 + .2*( rand( *shape( X1 ) ) - .5 )

    plot( *X1.T, 'o' )
    plot( *X2.T, 'o' )

    for link in assign( X1, X2, 1 ) :

        if link[0] == link[1] : # then the pairing is correct
            linestyle = '-'
        else :
            linestyle = ':'

        plot( *array( [ X1[ link[0] ], X2[ link[1] ] ] ).T, color = 'grey', linestyle = linestyle, zorder = -1 )

    axis('scaled')
    xticks([])
    yticks([])
    show()
