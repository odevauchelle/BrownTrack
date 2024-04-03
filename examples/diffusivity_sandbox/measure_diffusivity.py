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
    slow = BT.domain( 'Circle', { 'xy' : ( 0, 0 ), 'radius' : 1  } ),
    quick = BT.domain( 'Circle', { 'xy' : ( 0, 0 ), 'radius' : p['inner_radius']  } ),
)

####################
#
# figures
#
####################

fig, (ax_phys, ax_D) = subplots( ncols = 2, figsize = (8,4) )

ax_phys.axis('scaled')
ax_phys.axis('off')
ax_phys.set_xlim( array([-1,1])*domains['slow'].boundary['radius']*1.01 )
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

trajectories['quick'], trajectories['slow'] = domains['quick'].cookie_cutter( b.getAllTrajectories() )

cutoff = 10
downsampling = 1
bootstrap = 10
dim = 'x'

for name, trajectories_ in trajectories.items() :
    
    disp = BT.dispersion_2( trajectories_, cutoff = cutoff, dim = dim )
    binned_data = bindata( disp['time'], disp[dim[-1]], nbins = cutoff + 1 )

    _, sigma_2= binned_data.apply( var )
    t, _ = binned_data.apply( mean )

    D['x'], D['y'], D['std_x'], D['std_y'] = BT.diffusivity_2D( trajectories_, downsampling = downsampling, bootstrap = bootstrap )
    
    ax_D.plot( t, sigma_2, 'o', color = colors[name] )

    for trajectory in trajectories_ :
        ax_phys.plot( trajectory.x, trajectory.y, color = colors[name], lw = 1, alpha = .2, label = name )

    for local_dim in dim :
        ax_D.plot( t, 2*len(dim)*D[local_dim]*t, '--', color = colors[name] )

    ax_D.axhline( domains[name].get_area()/pi, color = colors[name], alpha = .1 )

print( 'measured', D)
print( 'theory', array(p['dxs'])**2/array(p['dts'])/2 )

#####################
#
# Save & show
#
#######################

show()
