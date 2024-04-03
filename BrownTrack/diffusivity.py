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


def dispersion( trajectories, with_velocities = False, cutoff = None, dim = 'xy' ) :
    '''
    Transforms a list of trajectories into a cloud of points, in the coordinates (time, r**2), where r is the distance to the starting point of each trajectory.
    The first point, of coordinate (0,0), is omitted from the output.

    time, r2 = dispersion( trajectories, with_velocities = False, cutoff = None, dim = 'xy' )
    time, r2, u, v = dispersion( trajectories, with_velocities = True, cutoff = None, dim = 'xy' )

    Arguments :
    trajectories : A list of trajectories.
    with_velocities (boolean) : Whether to calculate velocities as well
    cutoff (float): whether to slice the data, and the size of slices.
    dim : 'x', 'y' or 'xy' (the default), the dimension of interest

    Output :
    time : A time list. Time is set to zero at the beginning of each trajectory.
    r2 : A list of r**2, where r is the distance to the starting point of each trajectory.
    u, v (optional) : Two lists of velocities.
    '''

    dim =  list(dim)

    output = []

    for traj in trajectories :

        if not cutoff is None :
            number_of_slices = int( round( len( traj.x )/cutoff ) )

        else :
            number_of_slices = 0

        position = {}

        if number_of_slices > 0 :
            for d in dim :
                position[d] = np.array_split( traj.__dict__[d], number_of_slices )

        else :
            for d in dim :
                position[d] = [ traj.__dict__[d] ]

        for i in range( len( position[ dim[0] ] ) ) :

            time = np.arange( len( position[ dim[0] ][i] ) )
            
            if with_velocities :
                dt = np.diff(time)

            for i_d,d in enumerate( dim ) :

                x = position[d][i]

                
                if i_d == 0 :        
                    r2 = ( np.array( x ) - x[0] )**2

                else :
                    r2 += ( np.array( x ) - x[0] )**2

                if with_velocities :

                    additional_ouput += [ np.diff( x )/dt ]
            
            
            additional_ouput = [ time[1:], r2[1:] ]

            output += list( np.array( additional_ouput ).T )

    if output == [] :

        if with_velocities :
            return [ np.array([]) ]*len(dim)*2
        
        else :
            return [ np.array([]) ]*len(dim)
    
    else :
        return np.array( output ).T


def dispersion_2( trajectories, cutoff = None, dim = 'xy' ) :

    '''
    dispersion_2( trajectories, cutoff = None, dim = 'xy' )
    '''

    output = dict( time = [] )

    for d in dim :
        output[d] = []

    for traj in trajectories :
        
        N = len( traj.x )
        
        if cutoff is None :
            cutoff = N
            
        nb_full_slices = N//cutoff
        
        output['time'] += ( np.arange( cutoff ).tolist()*( nb_full_slices + 1 ) )[:N]

        for d in dim :

            x = np.array( traj.__dict__[d] )
            x0 = []

            for i in range( nb_full_slices + 1 ) :
                try :
                    x0 += [ x[ i*cutoff ] ]*cutoff
                except : # in case N == cutoff
                    pass

            x0 = np.array( x0 )[:N]
            output[d] += list( x - x0 )
        
    return output


def diffusivity_CVE( x = None, dx = None, dt = 1., estimator = 'Frishman' ) :

    '''
    D = get_diffusivity( x, dt = 1. )

    Covariance-based estimator for diffusivity.

    Arguments:
        x : one-dimensional series of positions
        dt : time step (defaults to 1.)
        estimator : "Frishman" or "Vestergaard"

    Output:
        D : estimate of diffusivity

    Vestergaard, C. L., Blainey, P. C., & Flyvbjerg, H. (2014). Optimal estimation of diffusion coefficients from single-particle trajectories. Physical Review E, 89(2), 022726.
    Frishman, A., & Ronceray, P. (2020). Learning force fields from stochastic trajectories. Physical Review X, 10(2), 021009.
    '''

    if dx is None :
        dx = np.diff( x )

    else :
        dx = np.array(dx)

    if estimator == 'Vestergaard' :
        return ( np.mean( dx**2 )/2 + np.mean( dx[1:]*dx[:-1] ) )/dt
    
    elif estimator == 'Frishman' :
        return ( np.mean( ( dx[1:] + dx[:-1] )**2 )/4 + np.mean( dx[1:]*dx[:-1] )/2 )/dt





def diffusivity_2D( trajectories, bootstrap = None, downsampling = None, **kwargs ) :

    '''
    Dx, Dy = diffusivity_2D( trajectories, bootstrap = None, dt = 1. )

    Covariance-based estimator for diffusivity.

    Arguments:
        trajectories : a list of two-dimensional trajectories
        bootstrap : if an integer, repeats the procedure on bootsrap slices of the data, and outputs the dispersion (defaults to None)
        dt : time step (defaults to 1.)

    Output:
        Dx, Dy : estimates of diffusivity along x and y
        Dx, Dy, std_Dx, std_Dy : diffusivity along x and y, and dispersion (if bootstratp isn't None)

    '''

    dx = []
    dy = []

    if downsampling is None :
        downsampling = 1

    for trajectory in trajectories :
        dx += np.diff( trajectory.x[::downsampling] ).tolist()
        dy += np.diff( trajectory.y[::downsampling] ).tolist()

    if bootstrap is None :
        return diffusivity_CVE( dx = dx, **kwargs )/downsampling, diffusivity_CVE( dx = dy, **kwargs )/downsampling
    
    else :

        Dx = [ diffusivity_CVE( dx = dx, **kwargs ) for dx in np.array_split( dx, bootstrap ) ]
        Dy = [ diffusivity_CVE( dx = dy, **kwargs ) for dy in np.array_split( dy, bootstrap ) ]

        std_Dx = np.std( Dx )/downsampling
        std_Dy = np.std( Dy )/downsampling

        Dx = np.mean( Dx )/downsampling
        Dy = np.mean( Dy )/downsampling

        return Dx, Dy, std_Dx, std_Dy


if __name__ == '__main__' :

    from numpy.random import normal

    print( 'Should be 0.5:', diffusivity_CVE( np.cumsum( normal( size = 1000 ) ) )  )
