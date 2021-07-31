from pylab import *
import json

################### TRAJECTORIES ###################

class trajectory :
    '''
    Two-dimensionnal trajectory with a starting time.

    Attributes:
    x: List of coordinates.
    y: List of coordinates.
    birth_time : Starting time of the trajectory.
    end_time : Time of the last point of the trajectory.
    '''

    def __init__( self, birth_time = 0, X = None, mummy = None ) :

        '''
        Create a trajectory.

        trajectory( self, birth_time = 0, X = None, mummy = None )

        Arguments:
        birth_time: Starting time of the trajectory.
        X: Starting point of the trajectory.
        mummy: Mummified trajectory.

        '''

        try :
            self.birth_time = birth_time
            self.x = [ X[0] ]
            self.y = [ X[1] ]
            self.end_time = birth_time + len(self.x)

        except :
            self.birth_time = mummy[0]
            self.x = mummy[1]
            self.y = mummy[2]

    def addPoint( self, X ) :
        '''
        Add a new point to a trajectory.

        addPoint( X )

        Arguments:
        X: The new point to be added.
        '''

        self.x += [ X[0] ]
        self.y += [ X[1] ]
        self.end_time += 1

    def getEnd( self ) :
        return [ self.x[-1], self.y[-1] ]

    def mummify( self ):

        '''
        Converts trajectory to dictionnary for storage.

        mummify()

        '''

        return [
            self.birth_time,
            self.x,
            self.y
            ]

def load_trajectories( traj_file, max_number_of_trajectories = inf, theta = None ) :

    trajectories = []

    for line in traj_file :

        if len( trajectories ) >= max_number_of_trajectories :
            break

        try :

            trajectory = trajectory( mummy = json.loads( line ) )

            if theta != None : # rotation
                y = array(trajectory.y); x = array(trajectory.x)
                trajectory.x = list( cos(theta)*y + sin(theta)*x )
                trajectory.y = list( cos(theta)*x - sin(theta)*y )

            trajectories += [ trajectory ]

        except :
            pass

    return trajectories




################### BUNCH (i.e. bunch of trajectories) ###################

class bunch :
    '''Collection of trajectories.'''

    def __init__( self, live_trajectories, dead_trajectories ) :
        '''
        Create a bunch of trajectories.

        bunch( live_trajectories, dead_trajectories )

        Parameters:
        live_trajectories: A list of trajectories which end at present time.
        dead_trajectories: A list of trajectories which have ended.

        '''

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
                traj_file.write('\n')

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
            if trajectory.birth_time < t < trajectory.end_time :
                x += [ nan ] + trajectory.x[:(t-trajectory.birth_time)]
                y += [ nan ] + trajectory.y[:(t-trajectory.birth_time)]

        return x,y
