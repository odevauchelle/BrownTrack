

import numpy as np

def dispersion( trajectories ) :
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
