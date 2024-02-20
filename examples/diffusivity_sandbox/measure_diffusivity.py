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
D = {}

colors = dict(quick = 'tab:orange', slow = 'tab:blue')

domains['main'].boundary['radius'] -= 2*min(p['dxs'])
all_trajectories, _ = domains['main'].cookie_cutter( b.getAllTrajectories() )

#all_trajectories = b.getAllTrajectories()


domains['inner'].boundary['radius'] -= 2*max(p['dxs'])

trajectories['quick'], trajectories['slow'] = domains['inner'].cookie_cutter( all_trajectories )

domains['inner'].boundary['radius'] += 2*max(p['dxs']) + 2*min(p['dxs'])
_, trajectories['slow'] = domains['inner'].cookie_cutter( trajectories['slow'] )

cutoff = 10
downsampling = 1
dim = 'xy'

for name, trajectories_ in trajectories.items() :
   
    t, sigma_2 = bindata( *BT.dispersion( trajectories_, cutoff = cutoff, dim = dim ), nbins = cutoff+1 ).apply()

    D['x'], D['y'] = BT.diffusivity_2D( trajectories_, downsampling = downsampling )
    
    ax_D.plot( t, sigma_2, 'o', color = colors[name] )

    for trajectory in trajectories_ :
        ax_phys.plot( trajectory.x, trajectory.y, color = colors[name], lw = 1, alpha = .2, label = name )

    for local_dim in dim :
        ax_D.plot( t, 2*len(dim)*D[local_dim]*t, '--', color = colors[name] )


print( 'measured', D)
print( 'theory', array(p['dxs'])**2/array(p['dts'])/2 )

#####################
#
# Save & show
#
#######################

show()
