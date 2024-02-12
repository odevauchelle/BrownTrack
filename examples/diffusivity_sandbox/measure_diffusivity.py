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


for name, trajectories_ in trajectories.items() :

    D[name] = dict( x = [], y = [] )
    sigma_2[name] = []
    t[name] = []

    for trajectory in trajectories_ :

        if len( trajectory.x ) > 2 :
            
            sigma_2[name] += ( ( array( trajectory.x ) - trajectory.x[0] )**2 + ( array( trajectory.y ) - trajectory.y[0] )**2 ).tolist()
            t[name] += arange( len( trajectory.x ) ).tolist()
            
            D[name]['x'] += [ BT.diffusivity_CVE( trajectory.x ) ]
            D[name]['y'] += [ BT.diffusivity_CVE( trajectory.y ) ]

        ax_phys.plot( trajectory.x, trajectory.y, color = colors[name], lw = 1, alpha = .2, label = name )
    
    print(D)

    time, sigma_2[name] = bindata( t[name], sigma_2[name], nbins = 20 ).apply()

    ax_D.plot( time, sigma_2[name], 'o', color = colors[name] )

    for dim in ['x', 'y' ] :
        D[name][dim] = mean( D[name][dim] )
        ax_D.plot( time, 4*D[name][dim]*time, '--', color = colors[name] )


print( 'measured', D)
print( 'theory', array(p['dxs'])**2/array(p['dts'])/2 )





#####################
#
# Save & show
#
#######################

show()