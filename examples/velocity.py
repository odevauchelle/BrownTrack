
import sys
sys.path.append('./../')

figure_path = '../figures/'

import BrownTrack as BT

traj = BT.trajectory( X = ( 1, 0 ) )

from pylab import *

for t in linspace(0,1,15)[1:]**2 :
    point = exp(1j*t*2*pi)
    # plot( *point, 'o' )
    traj.addPoint( ( real(point), imag(point) ) )


traj_u = traj.diff()


figure()
ax_phys = gca()
ax_phys.plot( traj.x, traj.y, '.-', label = 'Original' )
ax_phys.set_xlabel('$x$'); ax_phys.set_ylabel('$y$')
ax_phys.axis('scaled')
ax_phys.set_title('Position')

traj = traj.diff_companion()
ax_phys.plot( traj.x, traj.y, '.-', color = 'tab:orange', label = 'Midpoint' )

ax_phys.legend()

# savefig( figure_path + 'circle.svg', bbox_inches = 'tight')

figure()
ax_u = gca()
ax_u.plot( traj_u.x, traj_u.y, '.-', color = 'tab:orange' )
ax_u.set_xlabel(r'$\mathrm{d}x/\mathrm{d}t$'); ax_u.set_ylabel('$\mathrm{d}y/\mathrm{d}t$')
ax_u.axis('scaled')
ax_u.set_title('Velocity')

# savefig( figure_path + 'velocity_circle.svg', bbox_inches = 'tight')

angular_momentum = traj.x*traj_u.y - traj.y*traj_u.x

figure()
ax_m = gca()
ax_m.plot( traj.get_time_list(), angular_momentum, 'm.-')
ax_m.set_title('Angular momentum')
ax_m.set_xlabel(r'Time'); ax_m.set_ylabel('Angular momentum')

# savefig( figure_path + 'circle_momentum.svg', bbox_inches = 'tight')


show()
