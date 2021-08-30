# Slicing

A trajectory can be sliced, just like a list. Let us first create a trajectory:
```python
import BrownTrack as BT
traj = BT.trajectory( points = array( [ rand(5), rand(5) ] ).T )

for item, value in traj.__dict__.items() :
  print( item, ':', value )
```
```console
birth_time : 0
x : [0.14651764 0.44768981 0.28279086 0.11232581 0.88370136]
y : [0.30874002 0.04255391 0.61682148 0.67096416 0.32654818]
```

A single trajectory element is a time and a point:
```python
print(traj[1])
```
```console
(1, (0.44768980925722535, 0.04255391250420393))
```

A slice with more than one element is also a trajectory:
```python
for item, value in traj[2:].__dict__.items() :
  print( item, value )
```
```console
birth_time 2
x [0.28279086 0.11232581 0.88370136]
y [0.61682148 0.67096416 0.32654818]
```
