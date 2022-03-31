import numpy as np

roi = np.array([[0, 250], [520, 90], [640, 90],
                [640, 719], [0, 719]], dtype=np.uint32)


min_x = min(point[0] for point in roi)
min_y = min(point[1] for point in roi)
roi_offset = (min_x, min_y)
roi_region = ([point[0] - roi_offset[0], point[1] - roi_offset[1]]
              for point in roi)
roi_region_array = np.array([*([point[0] - roi_offset[0], point[1] - roi_offset[1]]
                               for point in roi)])
array_gen = np.array([*roi_region])

bounding_rect = [0, 0, 1081, 1920]
tup = [*bounding_rect[2:], 3]
array = np.array(tup, dtype=np.uint16)

print(array)
print(array_gen)
print(roi_region_array)
