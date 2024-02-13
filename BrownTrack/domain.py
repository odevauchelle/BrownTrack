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
from matplotlib.patches import Circle, Polygon
import matplotlib.pyplot as plt
from copy import deepcopy
# from shapely.geometry import Point, Polygon
import matplotlib.path as mplPath
from shapely.geometry import Polygon as shapely_Polygon

# from .trajectory import trajectory

############
#
#   Functions
#
############

def CircumscribedCircle( points ):
    '''
    From https://stackoverflow.com/questions/44231281/circumscribed-circle-of-a-triangle-in-2d

    center, radius = CircumscribedCircle( points )
    '''
    (x1, y1), (x2, y2), (x3, y3) = points

    A = np.array([[x3-x1,y3-y1],[x3-x2,y3-y2]])
    Y = np.array([(x3**2 + y3**2 - x1**2 - y1**2),(x3**2+y3**2 - x2**2-y2**2)])

    if np.linalg.det(A) == 0:
        return None

    Ainv = np.linalg.inv(A)
    X = 0.5*np.dot(Ainv,Y)
    x,y = X[0],X[1]
    r = np.sqrt((x-x1)**2+(y-y1)**2)

    return (x,y), r

############
#
#   Parameters
#
############

default_patch_style = dict( facecolor = 'none', edgecolor = 'k', linestyle = '--' )

############
#
#   Classes
#
############


class domain :
    '''
    A two-dimensionnal domain.
    '''

    def __init__( self, patch_type = None, boundary = None ) :
        '''
        A two-dimensionnal domain.

        omega = domain( boundary, patch_type = None, boundary = None )

        Parameters:
        patch_type (str): The type of patch that represents the domain. 'Polygon' or 'Circle'.
        boundary (dict): Parameters defining the domain's shape, such as a list of points for a polygon, or center and radius for a circle.
        '''

        if patch_type is None :
            patch_type = 'Polygon'

        if boundary is None :
            boundary = {}

        self.patch_type = patch_type
        self.boundary = boundary

    def deepcopy( self ) :
        return deepcopy( self )

    def as_dict( self, json_serialize = True ) :
        '''
        Creates a dictionary. Almost synonymous with domain.asdict().

        output = domain.as_dict( json_serialize = True ) :

        Parameters:
        json_serialize (Boolean): Wheter lists are converted to json serializable format.

        '''

        if json_serialize :
            output = self.__dict__
            output['boundary'] = np.array( self.boundary ).tolist()
            return output

        else :
            return self.__dict__


    def get_patch( self, **kwargs ) :
        '''
        Creates a patch that corresponds to the domain.

        is_kept = get_patch( self, **kwargs )

        Parameters:
        kwargs : Keyword arguments for matplotlib.patch.
        '''

        style = default_patch_style.copy()
        style.update( kwargs )

        if self.patch_type == 'Polygon' :
            patch = Polygon( **self.boundary, **style )

        elif self.patch_type == 'Circle' :
            patch = Circle( **self.boundary, **style )

        return patch

    def ginput( self, ax = None, timeout = -1 ) :
        '''
        Uses matplotlib ginput function to define the boundary of the domain.

        is_kept = domain.ginput( ax = None, timeout = -1 )

        Arguments:
        ax : Axis to which ginput applies.
        timeout : ginput timemout.
        '''

        ginput_style = default_patch_style.copy()
        ginput_style['edgecolor'] = 'red'

        if ax is None :
            ax = plt.gca()

        initial_title = ax.get_title()

        ax.set_title( initial_title + ' [' + self.patch_type + ']' )

        old_boundary = self.boundary.copy()

        if self.patch_type == 'Polygon' :
            self.boundary = dict( xy = plt.ginput( -1, timeout = timeout ) )

        elif self.patch_type == 'Circle' :
            center, radius = CircumscribedCircle( plt.ginput( -1, timeout = timeout ) )
            self.boundary = dict( xy = center, radius = radius )

        boundary_patch = self.get_patch( **ginput_style )

        ax.add_patch( boundary_patch )

        plt.show( block = False )

        is_kept = input( 'Keep? (Y/n) ' ) in ( '', 'Y', 'y' )
        boundary_patch.remove()
        ax.set_title( initial_title )

        if is_kept :
            return True

        else :
            self.boundary = old_boundary
            return False

    def get_area( self ) :
        if self.patch_type == 'Circle' :
            return np.pi*self.boundary['radius']**2

        elif self.patch_type == 'Polygon' :
            return shapely_Polygon( self.boundary['xy'] ).area

    def get_barycenter( self ) :
        '''
        Get the surface barycenter of a domain (centroid). Uses Shapely.

        xb, yb = domain.get_barycenter()
        '''

        if self.patch_type == 'Circle' :
            return self.boundary['xy'] # just the center

        elif self.patch_type == 'Polygon' :

            return list( shapely_Polygon( self.boundary['xy'] ).centroid.coords[0] )


    def contains( self, points ) :
        '''
        Whether points are inside domain.

        is_inside = domain.contains( points )

        Parameters:
        points : A list of points.

        Output:
        is_inside : A list of Booleans (True if inside).
        '''

        if self.patch_type == 'Circle' :
            x, y = np.array( points ).T
            xc, yc = self.boundary['xy']
            return abs( ( x - xc ) + 1j*( y - yc ) ) < self.boundary['radius']

        elif self.patch_type == 'Polygon' :
            path = mplPath.Path( self.boundary['xy'] )
            return path.contains_points( points )

    def resize( self, expansion_factor ) :
        '''
        Resize domain homotetically, with respect to the barycenter.

        domain.resize( expansion_factor )

        Parameters:
            expansion_factor (float) : scaling factor for the domain
        '''

        if self.patch_type == 'Circle' :
            self.boundary['radius'] *= expansion_factor

        elif self.patch_type == 'Polygon' :
            xy_center = self.get_barycenter()
            self.boundary['xy'] = list( np.array( xy_center ) + expansion_factor*( np.array( self.boundary['xy'] ) - np.array( xy_center ) ) )

    def cookie_cutter( self, trajectory ) :
        '''
        Split trajectories into inside and outside pieces. The resulting pieces are themselves trajectories.

        inside, outside = cookie_cutter( trajectories = None )

        Parameters:
        trajectory: A trajectory or a list of trajectories.

        Output:
        inside : A list of trajectories inside the domain.
        inside : A list of trajectories outside the domain.
        '''

        inside = []
        outside = []

        try : # argument is a single trajectory

            is_inside = self.contains( trajectory.getPoints() )

            is_inside = list( is_inside ) + [ not( is_inside[-1] ) ]

            while True :

                try :
                    cut = is_inside.index( not( is_inside[0] ) )

                    if is_inside[0] :
                        inside += [ trajectory[:cut] ]
                    else :
                        outside += [ trajectory[:cut] ]

                    is_inside = is_inside[cut:]
                    trajectory = trajectory[cut:]

                except :
                    return inside, outside

        except : # argument is a list of trajectories

            for trajectory in trajectory :

                new_inside, new_outside = self.cookie_cutter( trajectory )

                inside += new_inside
                outside += new_outside

            return inside, outside
