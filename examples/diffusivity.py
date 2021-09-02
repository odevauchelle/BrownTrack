
import sys
sys.path.append( './../')
sys.path.append( './../../bindata/' )

import BrownTrack as BT
from pylab import *
from bindata import bindata

figure_path = '../figures/'
save_figs = False

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
epsilon = 0.03 # step size of the random walk


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

for t in range(150) :

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

fig_phy = figure('phy')
ax_phy = gca()

fig_std = figure('std')
ax_std = gca()

ax_phy.add_patch( box.get_patch( linestyle = '-' ) )

traj_plots = []

for trajectory in trajectories.live_trajectories :
    traj_plots += [ ax_phy.plot( trajectory.x, trajectory.y )[0] ]

for ax in (ax_phy,) :

    ax.axis('scaled')
    ax.axis('off')
    ax.set_xticks([])
    ax.set_yticks([])

if save_figs :
    fig_phy.savefig(figure_path + 'diffusivity_phy.svg', bbox_inches = 'tight' )

########################
#
# Small box
#
########################

# small box for safety

small_box = box.deepcopy()
small_box.boundary['radius'] -= 5*epsilon

ax_phy.add_patch( small_box.get_patch( edgecolor = 'grey' ) )

for traj_plot in traj_plots :
    traj_plot.remove()

ax_phy.set_prop_cycle(None) # reset color cycle

inside, outside = small_box.cookie_cutter( trajectories.live_trajectories )

traj_std_plots = []

for traj in inside :

    ax_phy.plot( traj.x, traj.y )
    x, y = traj.x - traj.x[0], traj.y - traj.y[0]
    traj_std_plots += [ ax_std.plot( x**2 + y**2 )[0] ]

for traj in outside :
    ax_phy.plot( traj.x, traj.y, color = 'gray', alpha = .25 )

ax_std.set_xscale('log')
ax_std.set_yscale('log')
ax_std.set_xlabel('Time')
ax_std.set_ylabel(r'Dispersion  $\langle ( {\bf x - x_0 } )^2 \rangle$')

if save_figs :
    fig_std.savefig(figure_path + 'diffusivity_std.svg', bbox_inches = 'tight' )
    fig_phy.savefig(figure_path + 'diffusivity_phy_small_box.svg', bbox_inches = 'tight' )


for traj_std_plot in traj_std_plots :
    traj_std_plot.set_alpha(.3)

########################
#
# Diffusivity plot
#
########################

time, r2 = BT.dispersion( inside )

data = bindata( time, r2, bins = 'log', nbins = 6 )

time, r2 = data.apply( mean )
sigma_time, sigma_r2 = data.apply( std )
nb = data.nb

error_time, error_r2 = sigma_time/sqrt( nb ), sigma_r2/sqrt( nb )

std_color = 'k'

ax_std.errorbar( time, r2, sigma_r2, sigma_time, 'o', color = std_color, label = 'Binned data' )
#
# time_th = logspace( log10( nanmin( time ) ), log10( nanmax( time ) ), 10 )
# r2_th = epsilon**2*time_th

ax_std.plot( time, epsilon**2*time, '--', color = std_color, label = 'Theory' )
# plot( time_th, 10**polyval( fit, log10( time_th ) ), '--',color = 'gray' )
ax_std.legend()


if save_figs :
    fig_std.savefig(figure_path + 'diffusivity_std_th.svg', bbox_inches = 'tight' )

show()
