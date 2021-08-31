import numpy as np
from matplotlib.patches import *
import matplotlib.pyplot as plt

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
            center, radius = CircumscribedCircle( plt.ginput( 3, timeout = timeout ) )
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


    def cookie_cutter( self, trajectories = None ) :
        '''
        Split trajectories into inside and outside pieces. The resulting pieces are themselves trajectories.

        inside, outside = cookie_cutter( trajectories = None )

        Parameters:
        trajectories: A trajectory or a list of trajectories.

        Output:
        inside : A list of trajectories inside the domain.
        inside : A list of trajectories outside the domain.
        '''

        if trajectories is None :
            trajectories = []

        try :
            trajectories.x
            trajectories = [ trajectories ]

        except :
            pass

        inside = []
        outside = []

        for traj in trajectories :

            is_inside = self.get_patch().get_path().contains_points( traj.getPoints() )

            is_inside = list( is_inside ) + [ not( is_inside[-1] ) ]

            while True :

                try :
                    cut = is_inside.index( not( is_inside[0] ) )

                    if is_inside[0] :
                        inside += [ traj[:cut] ]
                    else :
                        outside += [ traj[:cut] ]

                    is_inside = is_inside[cut:]
                    traj = traj[cut:]

                except :
                    return inside, outside
