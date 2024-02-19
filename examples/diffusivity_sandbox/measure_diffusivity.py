from pylab import *
import json
from glob import glob
import sys

sys.path.append('/home/olivier/git/BrownTrack')
import BrownTrack as BT

sys.path.append('/home/olivier/git/bindata')
from bindata import bindata

##################
#
# load data
#
##################

data_path = './data/'

tilt = []
m = []

data_file = glob(data_path + 'walker_*.json')[0]

with open( data_file ) as the_file :
    p = json.load( the_file )

b = BT.bunch()

for trajectory in p['walkers'] :
    b.addTrajectory( BT.trajectory( points = array( trajectory ).T ) )

print( b.getAllTrajectories()[0].x )

domains = dict(
    main = BT.domain( 'Circle', { 'xy' : ( 0, 0 ), 'radius' : 1  } ),
    inner = BT.domain( 'Circle', { 'xy' : ( 0, 0 ), 'radius' : p['inner_radius']  } ),
)

####################
#
# figures
#
####################

fig, (ax_phys, ax_D) = subplots( ncols = 2, figsize = (8,4) )

ax_phys.axis('scaled')
ax_phys.axis('off')
ax_phys.set_xlim( array([-1,1])*domains['main'].boundary['radius']*1.01 )
ax_phys.set_ylim(ax_phys.get_xlim())

for name, domain in domains.items():
    ax_phys.add_patch( domain.get_patch() )
    # ax_phys.plot( *domain.get_barycenter(), '+k' )


################
#
# extract and plot trajectories
#
#################

trajectories = {}
sigma_2 = {}
D = {}
t = {}

colors = dict(quick = 'tab:orange', slow = 'tab:blue')

domains['main'].boundary['radius'] -= 2*min(p['dxs'])
all_trajectories, _ = domains['main'].cookie_cutter( b.getAllTrajectories() )

#all_trajectories = b.getAllTrajectories()


domains['inner'].boundary['radius'] -= 2*max(p['dxs'])

trajectories['quick'], trajectories['slow'] = domains['inner'].cookie_cutter( all_trajectories )

domains['inner'].boundary['radius'] += 2*max(p['dxs']) + 2*min(p['dxs'])
_, trajectories['slow'] = domains['inner'].cookie_cutter( trajectories['slow'] )

cutoff = 10

for name, trajectories_ in trajectories.items() :

   
    t[name], sigma_2[name] = bindata( *BT.dispersion( trajectories_, cutoff = cutoff ), nbins = cutoff+1 ).apply()

    D[name] = {}
    
    D[name]['x'], D[name]['y'] = BT.diffusivity_2D( trajectories_, downsampling=50 )
    
    ax_D.plot( t[name], sigma_2[name], 'o', color = colors[name] )

    for trajectory in trajectories_ :
        ax_phys.plot( trajectory.x, trajectory.y, color = colors[name], lw = 1, alpha = .2, label = name )


    for dim in ['x', 'y' ] :
        # D[name][dim] = nanmean( D[name][dim] )
        ax_D.plot( t[name], 4*D[name][dim]*t[name], '--', color = colors[name] )


print( 'measured', D)
print( 'theory', array(p['dxs'])**2/array(p['dts'])/2 )

#####################
#
# Save & show
#
#######################

show()
