import numpy as np
import cv2 as cv
from shapely.geometry import Polygon

def find_adj_mat_old(vertices, lines_centroids):
    adj_mat = np.zeros([len(vertices), len(vertices)])
    for i,v1 in enumerate(vertices):
        diff1 = vertices-v1
        dv = np.abs(diff1[:,0])+np.abs(diff1[:,1])#np.linalg.norm(vertices-v1,axis=1)
        idx = np.argsort(dv)
        
        for j, v2 in enumerate(vertices[idx[:5]]):
            if i!=idx[j]:
                midpt = (v1+v2)/2
               
                diff2 = lines_centroids - midpt
                d = np.linalg.norm(diff2, axis=1)
               
                nearest_neighbor = np.argmin(d)
               
                if d[nearest_neighbor]<=20:
                    adj_mat[i,idx[j]] = 1
                    adj_mat[idx[j],i] = 1
    return adj_mat

def box_intersect(box1, box2):
    a = min(box1[1],box2[1]) - max(box1[0], box2[0])
    b = min(box1[3],box2[3]) - max(box1[2], box2[2])
    return a>=0 and b>=0

def find_adj_mat(vertex_boxes, line_boxes):
    adj_mat = np.zeros([len(vertex_boxes), len(vertex_boxes)])
    for i,lb in enumerate(line_boxes):
        box1 = [lb[0], lb[0]+lb[2], lb[1], lb[1]+lb[3]]
        touched_vertices = []
        for j,vb in enumerate(vertex_boxes):
            box2 = [vb[0], vb[0]+vb[2], vb[1], vb[1]+vb[3]]
            if box_intersect(box1, box2):
                touched_vertices.append(j)
        
        if len(touched_vertices)!=2:
            continue
        adj_mat[touched_vertices[0],touched_vertices[1]] = 1
        adj_mat[touched_vertices[1],touched_vertices[0]] = 1
    return adj_mat

def cross_product(A):    
    # Stores coefficient of X
    # direction of vector A[1]A[0]
    X1 = (A[1][0] - A[0][0])
    # Stores coefficient of Y
    # direction of vector A[1]A[0]
    Y1 = (A[1][1] - A[0][1])
    # Stores coefficient of X
    # direction of vector A[2]A[0]
    X2 = (A[2][0] - A[0][0])
    # Stores coefficient of Y
    # direction of vector A[2]A[0]
    Y2 = (A[2][1] - A[0][1])
    # Return cross product
    return (X1 * Y2 - Y1 * X2)

def is_convex(points):
    # Stores count of
    # edges in polygon
    N = len(points)
    # Stores direction of cross product
    # of previous traversed edges
    prev = 0
    # Stores direction of cross product
    # of current traversed edges
    curr = 0
    # Traverse the array
    for i in range(N):  
        # Stores three adjacent edges
        # of the polygon
        temp = [points[i], points[(i + 1) % N],
                           points[(i + 2) % N]]
        # Update curr
        curr = cross_product(temp)
        # If curr is not equal to 0
        if (curr != 0):            
            # If direction of cross product of
            # all adjacent edges are not same
            if (curr * prev < 0):
                return False
            else:                
                # Update curr
                prev = curr

    return True

def AOI(vertices):
    polygon = Polygon(vertices)
   
    minx = np.min(vertices[:,0])
    maxx = np.max(vertices[:,0])
    miny = np.min(vertices[:,1])
    maxy = np.max(vertices[:,1])
    return polygon.area/(maxx-minx)/(maxy-miny)

def DFS_new(graph, marked, n, vert, start, count, path, cycles, vert_coords):
    # mark the vertex vert as visited
    marked[vert] = True
    # if the path of length (n-1) is found
    if n == 0:
        # mark vert as un-visited to make
        # it usable again.
        marked[vert] = False
        
        box = []
        for k in range(len(path)):
            box.append(vert_coords[path[k]])
        box = np.array(box)
        if AOI(box) >= 0.55:
            new_path = path + [start]
           
            s = set(new_path)
            duplicated = False
            for e in cycles:
                if s == set(e):
                    duplicated = True
            if not duplicated:
                cycles.append(new_path)
                count += 1 
            return count
        else:
            return count
  
    # For searching every possible path of
    # length (n-1)
    for i in range(len(graph)):
        if marked[i] == False and graph[vert][i] == 1:
 
            # DFS for searching path by decreasing
            # length by 1
            path = path + [i]
            
            count = DFS_new(graph, marked, n-1, i, start, count, path, cycles, vert_coords)
            path = path[:-1]
  
    # marking vert as unvisited to make it
    # usable again.
    marked[vert] = False
    return count

def DFS(graph, marked, n, vert, start, count, path, cycles):
 
    # mark the vertex vert as visited
    marked[vert] = True
    # if the path of length (n-1) is found
    if n == 0:
        # mark vert as un-visited to make
        # it usable again.
        marked[vert] = False
        # Check if vertex vert can end with
        # vertex start
        if graph[vert][start] == 1:
            new_path = path + [start]
            
            s = set(new_path)
            duplicated = False
            for e in cycles:
                if s == set(e):
                    duplicated = True
            if not duplicated:
                cycles.append(new_path)
                count += 1 
            return count
        else:
            return count
  
    # For searching every possible path of
    # length (n-1)
    for i in range(len(graph)):
        if marked[i] == False and graph[vert][i] == 1:
 
            # DFS for searching path by decreasing
            # length by 1
            path = path + [i]
            
            count = DFS(graph, marked, n-1, i, start, count, path, cycles)
            path = path[:-1]
  
    # marking vert as unvisited to make it
    # usable again.
    marked[vert] = False
    return count

def findCycles(graph, n, vert_coords):
 
    # all vertex are marked un-visited initially.
    V = len(graph)
    marked = [False] * V
  
    # Searching for cycle by using v-n+1 vertices
    count = 0
    cycles = []
    for i in range(V): #range(V-(n-1)):
        path = [i]
        marked[i] = True
        # count = DFS(graph, marked, n-1, i, i, count, path, cycles)
        count = DFS_new(graph, marked, n-1, i, i, count, path, cycles, vert_coords)
        # ith vertex is marked as visited and
        # will not be visited again.
        marked[i] = False
     
    return int(count), cycles    


def sortRow(points, iterations):
    z,x,y=points.shape
    for p in range(iterations):
        for k in range(z-1):
                if points[k,0,0]>=points[k+1,0,0]:
                    temp=points[k].copy()
                    points[k]=points[k+1].copy()
                    points[k+1]=temp.copy()
    return points




def sortPts(pts):
    ptsCopy=pts.copy()
    originalOrder=[i for i in range(len(pts))]
    for i in range(len(pts)):
        for j in range(len(pts)):
            if j==len(pts)-1:
                continue
            if ptsCopy[j][1]>ptsCopy[j+1][1]:
                temp=ptsCopy[j].copy()
                ptsCopy[j]=ptsCopy[j+1].copy()
                ptsCopy[j+1]=temp.copy()
                temp=originalOrder[j]
                originalOrder[j]=originalOrder[j+1]
                originalOrder[j]=temp
    if ptsCopy[0][0]>ptsCopy[1][0]:
        temp=ptsCopy[0].copy()
        ptsCopy[0]=ptsCopy[1].copy()
        ptsCopy[1]=temp.copy()
    
    if ptsCopy[2][0]<ptsCopy[3][0]:
        temp=ptsCopy[2].copy()
        ptsCopy[2]=ptsCopy[3].copy()
        ptsCopy[3]=temp.copy()
    
    return ptsCopy
    


#outline functionc called in the parking lot system that accepts a photo name
def outline(selected_img):
    img = cv.imread('./ParkingLotManager/Samples/{}'.format(selected_img)) # read the image
    threshold = 135
    mask = (img[:,:,0]>threshold) & (img[:,:,1]>threshold) & (img[:,:,2]>threshold) # generate a mask of the white lines
    cp_out = cv.connectedComponentsWithStats(mask.astype(np.int8), 4, cv.CV_16U) # do connected component labelling on the mask
    (numLabels1, labels1, stats1, centroids1) = cp_out # retrieve the statistics of the found connected components
    print(stats1) # print the statistics of the found connected components
    candidate_cp = [] # prepare an empty list for keeping the IDs of larger connected components formed by connected white lines
    new_mask = np.zeros_like(mask) # prepare a new mask for keeping all pixels of larger white lines
    for i in range(1,numLabels1):
        if (stats1[i,3]*stats1[i,4])>(0.65*img.shape[0]*img.shape[1]): # keep the white-line component if its bounding box size>0.65 parking lot area)
            new_mask = new_mask | (labels1==i) # add all pixels of this white-line connected component
            candidate_cp.append(i) # add the component ID into the list
    # Since there might be some very small white holes inside the white-line components, we need to fill them to avoid the false detection of corners
    kernel = np.ones((5,5),np.uint8) # we use the morphological closing operation to do the hole filling
    res = cv.morphologyEx(new_mask.astype(np.float32),cv.MORPH_CLOSE,kernel) # result of the hole filling

    #res = cv.erode(res,None,1) # result of the hole filling

    cv.imwrite('mask.jpg', (255*(1-res)).astype(np.uint8)) # write the result to a jpg file
    # cv2_imshow(res*255) # show the result (with no holes inside the white lines)

    #Corner detection can now begin
    gray = np.float32(1-res) # convert to gray image
    dst = cv.cornerHarris(gray,2,3,0.1) # detect corners
    dst = cv.dilate(dst,None,iterations=10) # dilate the corners so that neighboring corners can be merged into one
    img[dst>0.05*dst.max()]=[0,0,255] # plot the corners over the input image for visualization
    corners = (dst>0.05*dst.max()).astype(np.int8)
    
    cv.imshow("img",img) # show the result of the corner detection


    output1 = cv.connectedComponentsWithStats(corners, 4, cv.CV_16U)
    (numLabels1, labels1, stats1, centroids1) = output1
    centroids1, stats1 = centroids1[1:], stats1[1:]
    img_copy = img.copy()
    for i in range(len(centroids1)):
        txt = '%d'%i
        cv.putText(img_copy, txt, (int(centroids1[i][0]),int(centroids1[i][1])), cv.FONT_HERSHEY_PLAIN, 1, (200, 0, 0), 1, cv.LINE_AA)
   

    edges = gray.copy()
    for i in range(1, numLabels1):
        comp = labels1==i
        edges[:,:][comp] = 255 #np.random.randint(0,255)
    cv.imshow("edges",edges)

    e = (edges[:,:]==0).astype(np.int8)
    output2 = cv.connectedComponentsWithStats(e, 4, cv.CV_16U)
    (numLabels2, labels2, stats2, centroids2) = output2
    centroids2, stats2 = centroids2[1:], stats2[1:]
    
    for i in range(len(centroids2)):
        txt = '%d'%i
        cv.putText(img_copy, txt, (int(centroids2[i][0]),int(centroids2[i][1])), cv.FONT_HERSHEY_PLAIN, 1, (0, 200, 0), 1, cv.LINE_AA)
    cv.imshow("copy",img_copy)
    lines = edges.copy()
    for i in range(1, numLabels2):
        comp = labels2==i
        lines[:,:][comp] = np.random.randint(0,255)
        
    cv.imshow("line",lines)

    adjmat = find_adj_mat(stats1, stats2)
    

    n = 4
    num_cycles, cycles = findCycles(adjmat, n, centroids1)
    original_cycles=cycles
    out_img = img.copy()
    out_img2=img.copy()
    point_arr=[]
    doAgain=True
    rowCount=1
    parkingLot=dict()
    lots_per_row=0
    cv.destroyAllWindows()
    alreadyAdded=[False for c in cycles]
    while doAgain:#loop to ensure every box can be dealt with
        done=True
        out_img=img.copy()
        for i,c in enumerate(cycles):
            pts = []
            if alreadyAdded[i]==False:
                for j in range(4):
                    pts.append([np.round(centroids1[c[j]][0]), np.round(centroids1[c[j]][1])])
                pts=sortPts(pts)
                pts = np.array(pts, np.int32)
                cv.polylines(out_img,[pts],True,(0,255,255),5)
                cv.imshow("Point Selection",out_img)
                cv.imshow("Confirmation", out_img2)
                k=cv.waitKey(0)
                if k==ord('y'):
                    point_arr.append(pts)
                    alreadyAdded[i]=True
                    cv.polylines(out_img2,[pts],True,(0,255,0),5)
                elif k==ord('n'):
                    continue
                elif k==ord('c'):
                    lots_per_row=len(point_arr)
                    point_arr=np.array(point_arr, dtype=np.int32)
                    parkingLot['row_{}'.format(rowCount)]=point_arr
                    point_arr=[]
                    point_arr.append(pts)
                    cv.polylines(out_img2,[pts],True,(0,255,0),5)
                    alreadyAdded[i]=True
                    rowCount+=1
                elif k==ord('d'):
                    alreadyAdded[i]=True
            else:
                for v in alreadyAdded:
                    if v ==False:
                        done=False
                        break
                if done==True:
                    point_arr=np.array(point_arr, dtype=np.int32)
                    parkingLot['row_{}'.format(rowCount)]=point_arr
                    doAgain=False
    cv.destroyAllWindows()
    for row in parkingLot.keys():
        parkingLot[row]=sortRow(parkingLot[row], lots_per_row)


    return parkingLot, lots_per_row