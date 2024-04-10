from pylab import *

sys.path.append('../../../BrownTrack/')
import BrownTrack as BT
sys.path.append('../../../bindata/')
from bindata import bindata
# create random walkers

L = 50
tau = 10
u0 = .1
N = 100
box = BT.domain( 'Polygon', { 'xy' : ( array( [ [-1,-1], [1,-1], [1,1], [-1,1] ] )*L/2 ) } )

trajectories = BT.bunch()

for _ in range(N) :
    trajectories.addTrajectory( BT.trajectory( L*( rand( 2 ) - .5 ) ) )

ux, uy = normal( scale = u0, size = ( 2, N ) )


for _ in range(300) :

    updated = rand(N) < 1/tau
    ux[updated], uy[updated] = normal( scale = u0, size = ( 2, sum(updated) ) )

    x, y = array( trajectories.getEnds() ).T
    x += ux
    y += uy

    sel = x > L/2
    x[ sel ] = L/2 - ( x[ sel ] - L/2 )
    ux[ sel ] = -ux[ sel ]

    sel = x < - L/2
    x[ sel ] = - L/2 + ( - x[ sel ] - L/2 )
    ux[ sel ] = -ux[ sel ]

    sel = y > L/2
    y[ sel ] = L/2 - ( y[ sel ] - L/2 )
    uy[ sel ] = -uy[ sel ]

    sel = y < - L/2
    y[ sel ] = - L/2 + ( - y[ sel ] - L/2 )
    uy[ sel ] = -uy[ sel ]

    trajectories.grow( new_points = array((x,y)).T )

###################################
#
# plot
#
###################################

ax = gca()



ax.add_patch( box.get_patch() )

ax.axis('equal'); ax.axis('off')


###################################
#
# Dispersion
#
###################################

figure()
ax_sig = gca()

disp = BT.dispersion_2( trajectories.getAllTrajectories(), cutoff = 100*tau, dim = 'xy' )

for dim in 'y' :

    binned_data = bindata( disp['time'], disp[dim], nbins = 100 )
    t, _ = binned_data.apply(mean)
    _, sigma = binned_data.apply(var)

    ax_sig.plot( t, sigma, '.', color = 'grey' )

###################################
#
# Autocorrelation
#
###################################

box.resize(.9)
ax.add_patch( box.get_patch() )

cut_trajs, _ = box.cookie_cutter( trajectories.live_trajectories )

figure()
ax_ac = gca()

print(t)
for trajs in [trajectories.live_trajectories, cut_trajs] :

    for traj in trajs[::10] :
        ax.plot( traj.x, traj.y, color = 'tab:blue', alpha = .3 )

    alpha = BT.veloctiy_correlation( trajs, max_length = 5*tau )
    ax_ac.plot( alpha['y'] )

    D_tau = BT.autocorrelation_diffusivity( alpha )
    print(D_tau)

    t_th = linspace( min(t), max(t), 5)

    ax_sig.plot( t_th, 2*D_tau['D']['y']*t_th, '--'  )

print(t_th)



ax_sig.plot( t_th, 2*u0**2*tau*t_th, '-k', zorder = -1 )


ax_sig.set_xscale('log')
ax_sig.set_yscale('log')
ax_sig.axhline( L**2, linestyle = ':', color = 'k' )

show()
