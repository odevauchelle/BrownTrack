from pylab import *

sys.path.append('../../../BrownTrack/')
import BrownTrack as BT
sys.path.append('../../../bindata/')
from bindata import bindata
# create random walkers

L = 3
tau = 10
u0 = .2
N = 1000
# box = BT.domain( 'Polygon', { 'xy' : ( array( [ [-1,-1], [1,-1], [1,1], [-1,1] ] )*L/2 ) } )

trajectories = BT.bunch()

for _ in range(N) :
    trajectories.addTrajectory( BT.trajectory( ( rand(2)-.5 )*L ) )

ux, uy = normal( scale = u0, size = ( 2, N ) )

for _ in range(100) :

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

# ax.add_patch( box.get_patch() )

ax.axis('equal'); ax.axis('off')


###################################
#
# Dispersion
#
###################################

figure()
ax_sig = gca()
dim = 'x'

disp = BT.dispersion_2( trajectories.getAllTrajectories(), dim = dim )

binned_data = bindata( disp['time'], disp[dim], nbins = 100 )
t, _ = binned_data.apply(mean)
_, sigma = binned_data.apply(var)

ax_sig.plot( t, sigma, '.', color = 'grey', label = 'Data' )

###################################
#
# Autocorrelation
#
###################################
#
# box.resize(.9)
# ax.add_patch( box.get_patch() )
#
# cut_trajs, _ = box.cookie_cutter( trajectories.live_trajectories )

figure()
ax_ac = gca()

trajs = trajectories.live_trajectories

for traj in trajs[::10] :
    ax.plot( traj.x[:30*tau], traj.y[:30*tau], '.', ms = 1, color = 'tab:blue', alpha = .3 )

alpha = BT.veloctiy_correlation( trajs, max_length = int(tau) )
ax_ac.plot( alpha['y'] )

t = linspace(0, ax_ac.get_xlim()[1], 30 )
ax_ac.plot( t, u0**2*(1-t/tau), '--', color = 'grey', alpha = .6 )
ax_ac.plot( t, u0**2*(1-t/tau-2*t*u0/L), ':', color = 'grey', alpha = .6 )

ax_ac.set_xlabel('Time')
ax_ac.set_ylabel('Velocity auto-correlation')

# ax_ac.axvline( tau, color = 'grey', linestyle = '--', linewidth = rcParams['axes.linewidth'] )

D_tau = BT.autocorrelation_diffusivity( alpha )
print(D_tau)

t_th = linspace( min(t), max(t), 5)

Dx, Dy = BT.diffusivity_2D( trajs )
ax_sig.plot( t_th, 2*Dy*t_th, '--', label = 'CVE' )

Dx, Dy = BT.diffusivity_2D( trajs, downsampling = int(3*tau) )
ax_sig.plot( t_th, 2*Dy*t_th, '--', label = 'Decimated CVE' )

ax_sig.plot( t_th, 2*u0**2*tau*t_th, '-', color = 'grey', zorder = -1, label = 'Exact' )
ax_sig.legend()

ax_sig.set_xscale('log')
ax_sig.set_yscale('log')
# ax_sig.axhline( L**2, linestyle = ':', color = 'k' )
ax_sig.set_xlabel('Time')
ax_sig.set_ylabel('Position variance')


# ax.figure.savefig('trajectory_tau.svg', bbox_inches = 'tight')
# ax_sig.figure.savefig('dispersion_tau.svg', bbox_inches = 'tight')
# ax_ac.figure.savefig('autocorrelation_tau.svg', bbox_inches = 'tight')

ax_sig.plot( t_th, 2*D_tau['D'][dim]*t_th, '--', label = 'Autocorrelation' )
ax_sig.legend()
# ax_sig.figure.savefig('dispersion_tau_autocorr.svg', bbox_inches = 'tight')
ax_ac.axhline(0, color = 'k', linestyle = '--', linewidth = rcParams['axes.linewidth'])


show()
