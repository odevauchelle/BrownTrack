
import sys
sys.path.append('./../')

figure_path = '../figures/'

import BrownTrack as BT
from pylab import *

traj = BT.trajectory( points = array( [ rand(5), rand(5) ] ).T )

for item, value in traj.__dict__.items() :
  print( item, ':', value )

print('####################')

print(traj[1])

print('####################')

for item, value in traj[2:].__dict__.items() :
  print( item, value )

print('####################')

print(traj[-1])

print('####################')
