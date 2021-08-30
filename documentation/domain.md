# Domain

A domain is a portion of a two-dimensional space, defined by a closed boundary---a disk, for instance.

## Disk

Let us define a domain bounded by a disk:
```python
import BrownTrack as BT
domain = BT.domain( 'Circle', { 'xy' : ( 0, 0 ), 'radius' : 1  } )
```
To show it, we turn it into a `matplotlib.patches` object:
```python
from pylab import *
gca().add_patch( domain.get_patch() )
```

![Disk](../figures/domain.svg)

## Polygon

A domain can also be bounded by a polygon:
```python
domain = BT.domain( 'Polygon', { 'xy' : array( [ cos(theta), sin(theta) ] ).T  } )
```
![Polygon](../figures/domain_2.svg)
