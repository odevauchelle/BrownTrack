
import sys
sys.path.append('./../')

figure_path = '../figures/'

import BrownTrack as BT
from pylab import *
from random import shuffle

##################
#
# functions
#
##################

def geomean( x ) :
    return exp( nanmean( log(x) ) )

def geostd( x ) :
    return exp( nanstd( log(x) ) )

##################
#
# parameters
#
##################

box = BT.domain( patch_type = 'Circle', boundary = { 'xy': ( 0, 0 ), 'radius' : 1 } )
epsilon = 0.05 # step size of the random walk


##################
#
# random walk
#
##################

trajectories = BT.bunch()

for _ in range(10) :
    z = box.boundary['radius']*rand()*exp( 1j*2*pi*rand() )
    trajectories.addTrajectory( BT.trajectory( ( real(z), imag(z) ) ) )


# time loop

for t in range(100) :

    ########### trajectories Brownian motion

    for traj in trajectories.live_trajectories :

        dz = epsilon*exp( 1j*2*pi*rand() )
        x, y = array( traj.getEnd() ) + array( [ real(dz), imag(dz) ] )

        ########### boundaries

        z = x + 1j*y
        r = abs(z)

        if r > box.boundary['radius'] :
            z = z*( 2*box.boundary['radius'] - r )/r
            x, y = real(z), imag(z)

        traj.addPoint( [ x, y ] )

#######################
#
# plots
#
#######################

# trajectories

figure()

gca().add_patch( box.get_patch( linestyle = '-' ) )
axis('scaled'); axis('off')

xticks([])
yticks([])


traj_plots = []

for trajectory in trajectories.live_trajectories :
    traj_plots += [ plot( trajectory.x, trajectory.y )[0] ]


# savefig( figure_path + 'diffusivity_1.svg', bbox_inches = 'tight' )

########################
#
# Small box
#
########################

# small box for safety

small_box = box.deepcopy()
small_box.boundary['radius'] -= 2*epsilon

gca().add_patch( small_box.get_patch( edgecolor = 'grey' ) )

for traj_plot in traj_plots :
    traj_plot.remove()

gca().set_prop_cycle(None) # reset color cycle
# trajectories = []
#
# for theta in linspace(0,pi,5)[1:] :
#     z = 2*exp( 1j*theta )*linspace(-1,1,30)
#     trajectories += [ BT.trajectory( points = array( [ real(z), imag(z) ] ).T ) ]

inside, outside = small_box.cookie_cutter( trajectories.live_trajectories )

for traj in inside :
    plot( traj.x, traj.y )

for traj in outside :
    plot( traj.x, traj.y, color = 'gray', alpha = .25 )

# savefig( figure_path + 'diffusivity_2.svg', bbox_inches = 'tight' )

########################
#
# Diffusivity plot
#
########################

figure()

time, r2 = BT.spread( inside )

time_mean, r2_mean = BT.bin_data( time, r2 )['mean']

plot( time_mean, r2_mean, 'o', color = 'k' )

time_th = logspace( 0, log10( max( time_mean ) ), 10 )
r2_th = epsilon**2*time_th

plot( time_th, r2_th, '--', color = 'k' )
# plot( time_th, 10**polyval( fit, log10( time_th ) ), '--',color = 'gray' )

xscale('log')
yscale('log')

show()
