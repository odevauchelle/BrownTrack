
import sys
sys.path.append('./../')

figure_path = '../figures/'

import BrownTrack as BT
from pylab import *
from random import shuffle

# create random walkers

actual = BT.bunch()

for _ in range(3) :
    actual.addTrajectory( BT.trajectory( rand(2) ) )

# prepare tracker

tracker = BT.bunch()
tracker.assign( actual.getEnds(), mismatch_length = .2 )



# time loop

for t in range(20) :

    ########### Actual Brownian motion

    for traj in actual.live_trajectories :

        x, y = array( traj.getEnd() ) + 0.2*( rand(2) - array( [ .5, .5 ] ) )

        ########### boundaries

        if x < 0 :
            x = - x
        if x > 1 :
            x = 2 - x
        if y < 0 :
            y = - y
        if y > 1 :
            y = 2 - y

        traj.addPoint( [ x, y ] )

    # Let the tracker track

    new_points = actual.getEnds()

    if rand() < 0. :
        shuffle( new_points )
        new_points = new_points[:-1]

    tracker.assign( new_points, mismatch_length = .2 )

#######################
#
# plots
#
#######################

# trajectories

figure()

for trajectory in actual.live_trajectories :
    plot( trajectory.x, trajectory.y )

for trajectory in tracker.getAllTrajectories() :
    plot( trajectory.x, trajectory.y, ':k' )
    plot( array(trajectory.x)[[0,-1]], array(trajectory.y)[[0,-1]], '.k' )

# for trajectory in tracker.dead_trajectories :
#     plot( trajectory.x, trajectory.y, ':', color = 'grey' )

axis('scaled')
xlim([0,1])
ylim([0,1])
xticks([])
yticks([])

# savefig( figure_path + 'tracks_with_holes.svg', bbox_inches = 'tight' )



# timelines

figure( figsize = (6,3) )


h = 0

for traj in actual.live_trajectories :
    plot( [ traj.birth_time, traj.getEndTime() ], [h]*2 )
    h += 1


for traj in tracker.live_trajectories :
    plot( [ traj.birth_time, traj.getEndTime() ], [h]*2, ':k' )
    h += 1

for traj in tracker.dead_trajectories :
    plot( [ traj.birth_time, traj.getEndTime() ], [h]*2, ':', color = 'grey' )
    h += 1

yticks([])
xlim(0,t)

xlabel('Time')
ylabel('Trajectory label')



show()
