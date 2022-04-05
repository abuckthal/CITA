from itertools import count
import ghhops_server as hs
from flask import Flask
import rhino3dm as r


app = Flask(__name__)
hops = hs.Hops(app)


def get_cross_product(p1, p2, p3):
	return ((p2[0] - p1[0])*(p3[1] - p1[1])) - ((p2[1] - p1[1])*(p3[0] - p1[0]))


def get_slope(p1, p2):
	if p1[0] == p2[0]:
		return 999999
	else:
		return 1.0*(p1[1]-p2[1])/(p1[0]-p2[0])


@hops.component(
    "/convexhull",
    name="Convex Hull",
    description="Test a Set of Points",
    inputs=[
        hs.HopsPoint("P", "P", "Points", hs.HopsParamAccess.LIST  )
    ],

    outputs = [
        hs.HopsLine("E", "P", "Hull", hs.HopsParamAccess.LIST)       
    ]
)





def ConvexHull(points):
    

    #turns rhino points into tuple of coordinates (X, Y)
    points_coords = []
    for i in range(len(points)):
        points_coords.append((points[i].X, points[i].Y))


    #creates convex hull

    #finds starting point
    a = sorted(points_coords, key=lambda x: [x[0],x[1]])[0]
    start = a

    hull = []
    hull.append(start)

    #sort points counter-clockwise
    ccw_p = sorted(points_coords, key= lambda p: (get_slope(p, start)))
    
    #check for concavity
    for pt in ccw_p:
        hull.append(pt)
        while len(hull) > 2 and get_cross_product(hull[-3], hull[-2], hull[-1]) < 0:
            hull.pop(-2)

        
    #make a list of points to draw a polyline from
    for pt in hull:
        hull_rhino = []
        hull_rhino.append(r.Point3d(pt[0], pt[1], 0))

    #draw polyline
    return r.Polyline(hull_rhino)
    
    


#test print command
#print(ConvexHull([r.Point3d(20,5,0), r.Point3d(25,8,0), r.Point3d(15,3,0), r.Point3d(10,10,0), r.Point3d(9,14,0)]))

if __name__ == "__main__":
    app.run()
