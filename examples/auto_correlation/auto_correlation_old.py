from pylab import *
from numpy.random import normal
from numpy import correlate
sys.path.append('/home/olivier/git/BrownTrack/')
import BrownTrack as BT

t = arange( 1000)
N = 100
size =  ( len(t), N )
tau = 10
traj_len = 50

L = 100

u = [ array( [0]*N ).T ]
x = [ array( [0]*N ).T ]

while len(u) < len(t) :
    
    new_u = u[-1]*0.
    updated = rand(N) < 1/tau

    new_u[updated] = normal( size = sum(updated) )
    new_u[~updated] = u[-1][~updated]

    new_x = x[-1] + new_u
    
    bounce = new_x > L
    new_x[bounce] -= 2*( new_x[bounce] - L )

    bounce = new_x < - L
    new_x[bounce] += 2*( - new_x[bounce] - L )

    u += [ new_u ]
    x += [ new_x ]

u = array( u )
x = array(x)

fig_disp, (ax_u, ax_x) = subplots(nrows = 2, sharex = True)

figure()
ax_sig = gca()


ax_u.set_ylabel('$u$')
ax_x.set_ylabel('$x$')
ax_x.set_xlabel('$t$')


ax_sig.set_xlabel('$t$')
ax_sig.set_ylabel(r'$\sigma^2$')


# ax_u.imshow(u.T)


for xx in x.T[::10] :
    ax_x.plot( t[::10], xx[::10], color = 'tab:blue', alpha = .3 )
 

sigma_2 = var( x, axis = 1 )

ax_sig.plot( t, sigma_2 )


figure()
ax_corr = gca()
alpha = []
D_CVE = []

correlate_kwargs = dict( mode = 'full' )


for xx in x.T :
    
    xx = xx[:traj_len]
    uu = diff(xx)

    alpha += [ BT.autocorrelation( uu, **correlate_kwargs )  ]
    D_CVE += [ BT.diffusivity_CVE( x = xx ) ]

alpha = mean( array(alpha), axis = 0 )

D = {
    'CVE' : mean( D_CVE ),
    'Green-Kubo' : sum( alpha )/2,
    'exact' : tau/2
    }

print(D)

for name, D_value in D.items() :
    
    ax_sig.plot( t, 2*D_value*t, '--', alpha = .5, label = name )

t = arange(len(alpha))
t_mean = sum( t*alpha )/sum(alpha)
tau_alpha = sqrt( sum( ( t-t_mean )**2*alpha )/sum(alpha) )

bound_style = dict( linestyle = '--', color = 'k', alpha = .3 )

for tau in [tau, tau_alpha] :
    ax_sig.axvline( tau, **bound_style )

ax_sig.axhline( L**2, **bound_style )

ax_sig.legend()

ax_corr.plot( alpha )

ax_sig.set_xscale('log')
ax_sig.set_yscale('log')

show()
