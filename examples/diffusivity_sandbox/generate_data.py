from pylab import *
from numpy.random import normal
from matplotlib.patches import Circle
import json

dxs = .05, .03 # space step
dts = 1., 1.
inner_radius = .5
# dts = 1., ( dxs[0]/dxs[1] )**2 # time step

def time_step( z ):
    return dts[0] + ( dts[1] - dts[0] )*( abs(z) > inner_radius )

# def time_step( z ):
#     return dts[0] + ( dts[1] - dts[0] )*( abs(z) )

def space_step( z ) :
    return dxs[0] + ( dxs[1] - dxs[0] )*( abs(z) > inner_radius )

nb_walkers = 10
walkers = [ array([0. + 0j]*nb_walkers ) ]

#################
#
# Random walk loop
#
#################

min_diff_coef = 4*min( dxs )**2/max( dts )
measurement_time = int( 1/min_diff_coef )

nb_iterations = 500

print(measurement_time, nb_iterations)

for _ in range( nb_iterations ) :

    z = walkers[-1].copy()

    # steps
    step_size = space_step( z )
    dz = normal( scale = step_size ) + 1j*normal( scale = step_size )
    z += dz

    # boundary condition
    r = abs(z)
    outside = where( r > 1 )
    z[outside] -= 2*( r[outside] - 1 )*exp(1j*angle(z[outside]) )

    # save
    walkers += [z]

#####################
#
# Time
#
#####################

walkers = array( walkers )
dt = time_step( walkers )

t = cumsum( dt, axis = 0 )


#####################
#
# plot in physical space
#
#####################

fig, (ax_phys, ax_hist) = subplots( ncols = 2, figsize = (8,4))
ax_hist.yaxis.tick_right()
ax_hist.yaxis.set_label_position("right")

ax_phys.add_patch( Circle( [0,0], 1 , facecolor = 'none', edgecolor = 'k' ) )
ax_phys.add_patch( Circle( [0,0], .5 , facecolor = 'none', edgecolor = 'k', linestyle = '--', alpha = .5 ) )

for z in array(walkers).T[:3] :
    ax_phys.plot( real(z), imag(z), lw = .7, color = 'tab:blue', alpha = .3 )


# ax_t.axvline( measurement_time, color = 'k', linestyle = '--')

ax_phys.axis('scaled')
ax_phys.axis('off')
ax_phys.set_xticks([])
ax_phys.set_yticks([])

#####################
#
# histogram
#
#####################

r_bin = linspace(0,1,9)
r_area = pi*( r_bin[1:]**2 - r_bin[:-1]**2 )

print(shape(walkers))
z = walkers[measurement_time:,:].flatten()
print(shape(z))

n_bin, _ = histogram( abs( z ), bins = r_bin )
rho_bin = n_bin/r_area/len(z)

r = []
rho = []

for i in range( len( rho_bin ) ) :
    r += [ r_bin[i], r_bin[i+1] ]
    rho += [ rho_bin[i] ]*2


color = ax_hist.plot( r, rho )[0].get_color()
ax_hist.fill_between( r, rho, alpha = .2, color = color )

ax_hist.set_xlim(0,1)
ax_hist.set_ylim(0, ax_hist.get_ylim()[-1])
ax_hist.set_xlabel(r'Radius')
ax_hist.set_ylabel(r'Density $\rho$')


show(block = False)


###########################
#
# export data
#
###########################

data_file = './data/walker_' + str(rand()).split('.')[1] + '.json'

p = dict(
    inner_radius = inner_radius,
    dxs = dxs,
    dts = dts,
    walkers = [ [ real(z).tolist(), imag(z).tolist() ] for z in walkers.T ]
)

if input('Save?') in ('','y') :

    with open( data_file, 'w' ) as the_file :
        json.dump( p, the_file )
    
    print('Saved.')

else :
    print('Not saved.')

# savefig('varying_time_step.pdf', bbox_inches = 'tight')
