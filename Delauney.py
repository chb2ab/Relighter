import numpy as np
from scipy.spatial import Delaunay

def interpolate(paneldata, x, y):
    cord = np.array([x,y])
    n = len(paneldata)
    tri = Delaunay(paneldata)
    triangleindex = tri.find_simplex(cord)
    intercords = tri.simplices[triangleindex]
    index1 = np.empty(2)
    index2 = np.empty(2)
    index3 = np.empty(2)
    if triangleindex >= 0:
        index1[0] = intercords[0]
        index2[0] = intercords[1]
        index3[0] = intercords[2]
        x1 = tri.points[intercords[0]][0]
        y1 = tri.points[intercords[0]][1]
        x2 = tri.points[intercords[1]][0]
        y2 = tri.points[intercords[1]][1]
        x3 = tri.points[intercords[2]][0]
        y3 = tri.points[intercords[2]][1]
        
        index1[1] = ((y2 - y3) * (x - x3) + (x3 - x2) * (y - y3)) / ((y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3))
        index2[1] = ((y3 - y1) * (x - x3) + (x1 - x3) * (y - y3)) / ((y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3))
        index3[1] = 1 - index1[1] - index2[1]
    else:
        index1[0] = -1
        index1[1] = 10000000
        index2[0] = -1
        index2[1] = 10000000
        index3[0] = -1
        index3[1] = 0
        distance = np.empty(n)
        for i in range(n):
            distance[i] = np.linalg.norm(np.subtract(cord, paneldata[i]))
            if distance[i] < index1[1]:
                index2[0] = index1[0]
                index2[1] = index1[1]
                index1[0] = i
                index1[1] = distance[i]
            elif distance[i] < index2[1]:
                index2[0] = i
                index2[1] = distance[i]
        base = index1[1] + index2[1]
        index1[1] /= base
        index2[1] /= base
    ans = np.array([index1, index2, index3])        
    return ans
