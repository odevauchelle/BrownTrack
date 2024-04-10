from pylab import *

sys.path.append('../../../BrownTrack/')
import BrownTrack as BT
sys.path.append('../../../bindata/')
from bindata import bindata
# create random walkers

# L = 50
u0 = .1
N = 10
# box = BT.domain( 'Polygon', { 'xy' : ( array( [ [-1,-1], [1,-1], [1,1], [-1,1] ] )*L/2 ) } )

trajectories = BT.bunch()
for _ in range(N) :
    trajectories.addTrajectory( BT.trajectory( normal( scale = 1, size = 2 ) ) )
ux, uy = normal( scale = u0, size = ( 2, N ) )


for _ in range(10) :
    trajectories.grow( new_points = trajectories.getEnds() + normal( scale = u0, size = ( N, 2 ) ) )

###################################
#
# plot
#
###################################
fig_phys = figure()
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

binned_data = bindata( disp['time'], disp[dim], nbins = 10 )
t, sigma = binned_data.apply(mean)
_, sigma = binned_data.apply(var)

ax_sig.plot( t, sigma, 'o', color = 'grey', label = 'Data' )

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



for traj in trajectories.live_trajectories :
    ax.plot( traj.x, traj.y, color = 'tab:blue', alpha = .5 )


fig_phys.savefig('trajectories_autocorrelation_fails.svg', bbox_inches = 'tight')

figure()
ax_ac = gca()

alpha = BT.veloctiy_correlation( trajectories.live_trajectories, max_length = 10 )
ax_ac.plot( alpha['y'] )

D_tau = BT.autocorrelation_diffusivity( alpha )
print(D_tau)

t_th = linspace( min(t), max(t), 5)

# ax_sig.plot( t_th, 2*D_tau['D'][dim]*t_th, '--', label = 'Autocorrelation' )

Dx, Dy = BT.diffusivity_2D( trajectories.live_trajectories )
ax_sig.plot( t_th, 2*Dy*t_th, '--', label = 'CVE' )

# Dx, Dy = BT.diffusivity_2D( trajs, downsampling = int(3*tau) )
# ax_sig.plot( t_th, 2*Dy*t_th, '--', label = 'Decimated CVE' )

ax_sig.plot( t_th, u0**2*t_th, '-', color = 'grey', zorder = -1, label = 'Exact' )
ax_sig.legend()


ax_sig.set_xscale('log')
ax_sig.set_yscale('log')
# ax_sig.axhline( L**2, linestyle = ':', color = 'k' )
ax_sig.set_xlabel('Time')
ax_sig.set_ylabel('Position variance')

ax_sig.get_figure().savefig('CVE_estimator.svg',bbox_inches = 'tight')


show()
