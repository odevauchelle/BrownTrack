from pylab import *
import json

from .assignment import assign

##########################
#
# miscellaneous functions
#
##########################

def none_to_zero( x ) :
    if x is None :
        return 0
    else :
        return x

################### TRAJECTORIES ###################

class trajectory :
    '''
    Two-dimensionnal trajectory with a starting time.

    Attributes:
    x: List of coordinates.
    y: List of coordinates.
    birth_time : Starting time of the trajectory.
    '''

    def __init__( self, X = None, birth_time = 0, mummy = None, points = None ) :

        '''
        Create a trajectory.

        trajectory( self, X = None, birth_time = 0, mummy = None, points = None )

        Arguments:
        birth_time: Starting time of the trajectory.
        X: Starting point of the trajectory.
        mummy: Mummified trajectory.
        points: List of points.

        '''

        try :
            self.birth_time = birth_time
            self.x = [ X[0] ]
            self.y = [ X[1] ]

        except :

            try :
                self.birth_time = mummy[0]
                self.x = mummy[1]
                self.y = mummy[2]

            except :
                self.birth_time = birth_time
                self.x = array( points )[:,0]
                self.y = array( points )[:,1]

    def getEndTime( self ) :
        return self.birth_time + len( self.x )

    def getPoints( self ) :
        return list( array( [ self.x, self.y ] ).T )

    def __getitem__( self, key ) : #  slicing

        time = range( len( self.x ) )[key]

        if type(key) == int : # returns only a point
            return ( self.x[key], self.y[key]), self.birth_time + time

        else :
            return trajectory( points = self.getPoints()[key], birth_time = self.birth_time + time[0] )

    def addPoint( self, X ) :
        '''
        Add a new point to a trajectory.

        addPoint( X )

        Arguments:
        X: The new point to be added.
        '''

        self.x += [ X[0] ]
        self.y += [ X[1] ]

    def getEnd( self ) :
        return [ self.x[-1], self.y[-1] ]

    def mummify( self, json_serializable = True ):

        '''
        Converts trajectory to list for storage in file.

        mummify()

        '''
        if json_serializable :
            return [ self.birth_time, array( self.x ).tolist(), array( self.y ).tolist() ]
        else :
            return [ self.birth_time, self.x, self.y ]

def load_trajectories( traj_file, max_number_of_trajectories = inf, theta = None ) :

    trajectories = []

    for line in traj_file.readlines() :

        if len( trajectories ) >= max_number_of_trajectories :
            break

        try :

            traj = trajectory( mummy = json.loads( line ) )

            if theta != None : # rotation
                y = array(traj.y); x = array(traj.x)
                traj.x = list( cos(theta)*y + sin(theta)*x )
                traj.y = list( cos(theta)*x - sin(theta)*y )

            trajectories += [ traj ]

        except :
            print( 'Could not read line:', line )
            pass

    return trajectories




################### BUNCH (i.e. bunch of trajectories) ###################

class bunch :
    '''Collection of trajectories.'''

    def __init__( self, live_trajectories = None, dead_trajectories = None ) :
        '''
        Create a bunch of trajectories.

        bunch( live_trajectories = None, dead_trajectories = None )

        Parameters:
        live_trajectories: A list of trajectories which end at present time.
        dead_trajectories: A list of trajectories which have ended.

        '''

        if live_trajectories is None :
            live_trajectories = []

        if dead_trajectories is None :
            dead_trajectories = []

        self.live_trajectories = live_trajectories
        self.dead_trajectories = dead_trajectories

    def getAllTrajectories( self ) :
        return self.live_trajectories + self.dead_trajectories

    def addTrajectory( self, trajectories ) :

        if type(trajectories) == list :
            self.live_trajectories += trajectories

        elif isinstance(trajectories, trajectory) :
            self.live_trajectories += [ trajectories ]

        else :
            print('This is not a trajectory or a list of trajectories.')

    def getEnds( self ) :

        end_points = []

        for trajectory in self.live_trajectories :
            end_points += [ [ trajectory.x[-1], trajectory.y[-1] ] ]

        return end_points

    def kill( self, kill_list ) :

        killed_trajectories = []
        surviving_trajectories = []

        for n in range( len(self.live_trajectories) ) :
            if n in kill_list :
                killed_trajectories += [self.live_trajectories[n]]
            else :
                surviving_trajectories += [self.live_trajectories[n]]

        self.live_trajectories = surviving_trajectories
        self.dead_trajectories += killed_trajectories

    def undertake( self ) :
        self.dead_trajectories = []


    def bury( self, traj_file, traj_filter = lambda trajectory: True ) :
        '''
        Save trajectories in a text file.
        A user defined filter traj_filter may be used to filter trajectories before saving them.
        '''

        for traj in self.dead_trajectories :

            if traj_filter( traj ):
                json.dump( traj.mummify(), traj_file, separators = ( ',', ':' ) )
                traj_file.write( '\n' )

    def killAllTrajectories( self ) :
        self.dead_trajectories += self.live_trajectories
        self.live_trajectories = []

    def grow( self, tracks, new_points ) :

        '''
        grow( tracks, new_points )

        Parameters:
        tracks: A list of tuples. Each tuple contains two indices. The first index is that of the trajectory to be grown. The second is that of the new point.
        new_points: The points to be added to the trajectories.
        '''

        for track in tracks :
            self.live_trajectories[ track[0] ].addPoint( new_points[ track[1] ] )

    def getTrajectoriesTime( self, t ) :

        x = []
        y = []

        for trajectory in self.getAllTrajectories() :
            if trajectory.birth_time < t < trajectory.getEndTime() :
                x += [ nan ] + trajectory.x[:(t-trajectory.birth_time)]
                y += [ nan ] + trajectory.y[:(t-trajectory.birth_time)]

        return x,y

    def getCurrentTime( self ) :
        try :
            return max( [ traj.getEndTime() for traj in self.getAllTrajectories() ] )
        except :
            return 0

    def assign( self, points, mismatch_length = 1, t = None ) :
        '''
        Convenience method that assigns new points to the trajectories of a bunch, create new trajectories when necessary, and kills the disconnected trajectories.

        assign_to_bunch( points, mismatch_length = 1, t = None )

        Returns:
        points: Set of points to be added to the bunch's trajectories.
        mismatch_length: Length beyond which it's likely that points contains a point that doesn't match any end point.
        t: Time of the assignement. If None, find the most recent point among all trajectories.
        '''

        if t is None :
            t = self.getCurrentTime()

        try :
            links = assign( X1 = self.getEnds(), X2 = points, mismatch_length = mismatch_length )
            new_point_indices =  list( set( range( len(points) ) ) - set ( [ link[1] for link in links ] ) )
        except :
            print( 'Link error at time ' + str(t) )

        try :
            self.grow( links, points )
        except :
             print( 'bunch.grow error at time ' + str(t) )

        try :
            disconnected_trajectories = list( set( range( len( self.live_trajectories ) ) ) - set ( [ link[0] for link in links ] ) )
            self.kill( disconnected_trajectories )
        except :
            print( 'bunch.kill error at time ' + str(t) )

        # print(points[new_point_indices])

        try :
            for point in array(points)[ new_point_indices ] :
                self.addTrajectory( trajectory( point, t ) )
        except :
            print( 'bunch.addTrajectory error at time ' + str(t) )
