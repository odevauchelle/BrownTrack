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

def dispersion( trajectories, with_velocities = False ) :
    '''
    Transforms a list of trajectories into a cloud of points, in the coordinates (time, r**2), where r is the distance to the starting point of each trajectory.
    The first point, of coordinate (0,0), is omitted from the output.

    time, r2 = dispersion( trajectories, with_velocities = False )
    time, r2, u, v = dispersion( trajectories, with_velocities = True )

    Arguments :
    trajectories : A list of trajectories.
    with_velocities (boolean) : Whether to calculate velocities as well

    Output :
    time : A time list. Time is set to zero at the beginning of each trajectory.
    r2 : A list of r**2, where r is the distance to the starting point of each trajectory.
    u, v (optional) : Two lists of velocities.
    '''

    output = []

    for traj in trajectories :

        time = np.arange( len( traj.x ) )
        r2 = ( np.array( traj.x ) - traj.x[0] )**2 + ( np.array( traj.y ) - traj.y[0] )**2

        additional_ouput = [ time[1:], r2[1:] ]

        if with_velocities :
            dt = np.diff(time)
            additional_ouput += [ np.diff( traj.x )/dt, np.diff( traj.y )/dt ]

        output += list( np.array( additional_ouput ).T )

    if output == [] :
        if with_velocities :
            return [ np.array([]) ]*4
        else :
            return [ np.array([]) ]*2
    else :
        return np.array( output ).T


def diffusivity_CVE( x, dt = 1. ) :

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

    dx = np.diff( x )

    return ( np.mean( dx**2 )/2 + np.mean( dx[1:]*dx[:-1] ) )/dt

def diffusivity_2D( trajectories, **kwargs ) :

    '''
    Dx, Dy = diffusivity_2D( trajectories, dt = 1. )

    Covariance-based estimator for diffusivity.

    Arguments:
        trajectories : a list of two-dimensional trajectories
        dt : time step (defaults to 1.)

    Output:
        Dx, Dy : estimates of diffusivity along x and y
    '''

    Dx = []
    Dy = []

    for trajectory in trajectories :
        Dx += [ diffusivity_CVE( trajectory.x, **kwargs ) ]
        Dy += [ diffusivity_CVE( trajectory.y, **kwargs ) ]

    return Dx, Dy


if __name__ == '__main__' :

    from numpy.random import normal

    print( diffusivity_CVE( np.cumsum( normal( size = 1000 ) ) )  )
