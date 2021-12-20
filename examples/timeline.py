
import sys
sys.path.append('./../')

figure_path = './'

import BrownTrack as BT
from pylab import *

population = BT.bunch( live_trajectories = [BT.trajectory( X = [0.5,0.5] ) ], dead_trajectories = [] )

for t in range(150) :

    ########### Brownian motion

    for traj in population.live_trajectories :

        x, y = array( traj.getEnd() ) + 0.1*( rand(2) - array( [ .5, .5 ] ) )

        ########### boundaries

        if x < 0 :
            x = - x
        if x > 1 :
            x = 2 - x
        if y < 0 :
            y = - y
        if y > 1 :
            y = 2 - y

        traj.addPoint( [x, y ] )


        ########### splitting

        if rand() < .03 :

            population.addTrajectory( BT.trajectory( X = traj.getEnd(), birth_time = t ) )

    ########## Death
    population.kill( where( rand( len( population.live_trajectories ) ) < .01 )[0] )

live_color = 'tab:blue'
dead_color = 'tab:grey'

figure()

for trajectory in population.dead_trajectories :
    plot( trajectory.x, trajectory.y, dead_color, alpha = .5 )

for trajectory in population.live_trajectories :
    plot( trajectory.x, trajectory.y, live_color, alpha = .5 )

axis('scaled')
xlim([0,1])
ylim([0,1])
xticks([])
yticks([])

savefig( figure_path + 'bugs.svg', bbox_inches = 'tight' )

figure( figsize = (6,3) )
h = 0

for traj in population.dead_trajectories :
    plot( [ traj.birth_time, traj.getEndTime() ], [h]*2, dead_color )
    h += 1

for traj in population.live_trajectories :
    plot( [ traj.birth_time, traj.getEndTime() ], [h]*2, live_color )
    h += 1

yticks([])
xlim(0,t)

xlabel('Time')
ylabel('Trajectory label')

savefig( figure_path + 'timeline.svg', bbox_inches = 'tight' )

show()
