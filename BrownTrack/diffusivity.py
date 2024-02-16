#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# Olivier Devauchelle, 2021
#
# Based on a library initially developped by O.~Devauchelle, A.~Abramian & E.~Lajeunesse with the help of J.~Heyman


import numpy as np

def dispersion( trajectories, with_velocities = False, cutoff = None ) :
    '''
    Transforms a list of trajectories into a cloud of points, in the coordinates (time, r**2), where r is the distance to the starting point of each trajectory.
    The first point, of coordinate (0,0), is omitted from the output.

    time, r2 = dispersion( trajectories, with_velocities = False, cutoff = None )
    time, r2, u, v = dispersion( trajectories, with_velocities = True, cutoff = None )

    Arguments :
    trajectories : A list of trajectories.
    with_velocities (boolean) : Whether to calculate velocities as well
    cutoff (float): whether to slice the data, and the size of slices.

    Output :
    time : A time list. Time is set to zero at the beginning of each trajectory.
    r2 : A list of r**2, where r is the distance to the starting point of each trajectory.
    u, v (optional) : Two lists of velocities.
    '''

    output = []

    for traj in trajectories :

        if not cutoff is None :
            number_of_slices = int( round( len(traj.x)/cutoff ) )

        else :
            number_of_slices = 0

        if number_of_slices > 0 :
            x_list = np.array_split( traj.x, number_of_slices )
            y_list = np.array_split( traj.y, number_of_slices )

        else :
            x_list = [traj.x]
            y_list = [traj.y]

        for i in range(len(x_list)) :

            x = x_list[i]
            y = y_list[i]
            
            time = np.arange( len( x ) )
            r2 = ( np.array( x ) - x[0] )**2 + ( np.array( y ) - y[0] )**2

            additional_ouput = [ time[1:], r2[1:] ]

            if with_velocities :
                dt = np.diff(time)
                additional_ouput += [ np.diff( x )/dt, np.diff( y )/dt ]

            output += list( np.array( additional_ouput ).T )

    if output == [] :

        if with_velocities :
            return [ np.array([]) ]*4
        
        else :
            return [ np.array([]) ]*2
    
    else :
        return np.array( output ).T


def diffusivity_CVE( x = None, dx = None, dt = 1. ) :

    '''
    D = get_diffusivity( x, dt = 1. )

    Covariance-based estimator for diffusivity.

    Arguments:
        x : one-dimensional series of positions
        dt : time step (defaults to 1.)

    Output:
        D : estimate of diffusivity

    Vestergaard, C. L., Blainey, P. C., & Flyvbjerg, H. (2014). Optimal estimation of diffusion coefficients from single-particle trajectories. Physical Review E, 89(2), 022726.
    '''

    if dx is None :
        dx = np.diff( x )

    else :
        dx = np.array(dx)

    return ( np.mean( dx**2 )/2 + np.mean( dx[1:]*dx[:-1] ) )/dt

def diffusivity_2D( trajectories, bootstrap = None, **kwargs ) :

    '''
    Dx, Dy = diffusivity_2D( trajectories, bootstrap = None, dt = 1. )

    Covariance-based estimator for diffusivity.

    Arguments:
        trajectories : a list of two-dimensional trajectories
        bootstrap : if an integer, repeats the procedure on bootsrap slices of the data, and outputs the estimated error (defaults to None)
        dt : time step (defaults to 1.)

    Output:
        Dx, Dy : estimates of diffusivity along x and y
        Dx, Dy, std_Dx, std_Dy : diffusivity along x and y, and estimated error (if bootstratp isn't None)

    '''

    dx = []
    dy = []

    for trajectory in trajectories :
        dx += np.diff( trajectory.x ).tolist()
        dy += np.diff( trajectory.y ).tolist()

    Dx, Dy = diffusivity_CVE( dx = dx, **kwargs ), diffusivity_CVE( dx = dy, **kwargs )

    if bootstrap is None :
        return Dx, Dy
    
    else :

        std_Dx = np.std( [ diffusivity_CVE( dx = dx, **kwargs ) for dx in np.array_split( dx, bootstrap ) ] )/bootstrap
        std_Dy = np.std( [ diffusivity_CVE( dx = dy, **kwargs ) for dy in np.array_split( dy, bootstrap ) ] )/bootstrap

        return Dx, Dy, std_Dx, std_Dy


if __name__ == '__main__' :

    from numpy.random import normal

    print( 'Should be 0.5:', diffusivity_CVE( np.cumsum( normal( size = 1000 ) ) )  )
