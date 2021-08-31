from matplotlib.patches import Circle

patch = Circle( xy = (0,0), radius = .8 )

print(patch)
print(patch.contains_points([(0,0), (0,.7), (0,0.9)]))
