

import numpy as np

def spread( trajectories ) :
    '''
    Transforms a list of trajectories into a cloud of points, in the coordinates (time, r**2), where r is the distance to the starting point of each trajectory.
    The first point, of coordinate (0,0), is omitted from the output.

    time, r2 = radial_spread( trajectories )

    Arguments :
    trajectories : A list of trajectories.

    Output :
    time : A time list. Time is set to zero at the beginning of each trajectory.
    r2 : A list of r**2, where r is the distance to the starting point of each trajectory.
    '''

    time_r2 = []

    for traj in trajectories :

        time = np.arange( len( traj.x ) )
        r2 = ( traj.x - traj.x[0] )**2 + ( traj.y - traj.y[0] )**2

        time = time[1:]
        r2 = r2[1:]

        time_r2 += list( np.array( [ time, r2 ] ).T )

    return np.array( time_r2 ).T


def bin_data( x, y, bins = None, nb_bins = 10, **statistics ) :

    if statistics == {} :
        statistics = { 'mean' : np.mean }

    if bins is None :
        bins = 'log'

    if bins == 'log' :
        bins = np.logspace( 0, np.log10( max(x) ), nb_bins )

    elif bins == 'lin' :
        bins = np.linspace( 1, max(x), nb_bins )

    output = { 'bins' : bins, 'nb_points' : [] }

    for key in statistics.keys() :

        output[key] = [ [], [] ]

    print(bins)

    indices = np.digitize( x, bins )

    for index in set( indices ) :

        selection = indices == index

        output['nb_points'] += [ sum(selection) ]

        for key in statistics.keys() :

            output[key][0] += [ statistics[key]( x[ selection ] ) ]
            output[key][1] += [ statistics[key]( y[ selection ] ) ]

    return output
