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

def dispersion( trajectories ) :
    '''
    Transforms a list of trajectories into a cloud of points, in the coordinates (time, r**2), where r is the distance to the starting point of each trajectory.
    The first point, of coordinate (0,0), is omitted from the output.

    time, r2 = dispersion( trajectories )

    Arguments :
    trajectories : A list of trajectories.

    Output :
    time : A time list. Time is set to zero at the beginning of each trajectory.
    r2 : A list of r**2, where r is the distance to the starting point of each trajectory.
    '''

    time_r2 = []

    for traj in trajectories :

        time = np.arange( len( traj.x ) )
        r2 = ( np.array( traj.x ) - traj.x[0] )**2 + ( np.array( traj.y ) - traj.y[0] )**2

        time = time[1:]
        r2 = r2[1:]

        time_r2 += list( np.array( [ time, r2 ] ).T )

    if time_r2 == [] :
        return [ np.array([]) ]*2
    else :
        return np.array( time_r2 ).T
