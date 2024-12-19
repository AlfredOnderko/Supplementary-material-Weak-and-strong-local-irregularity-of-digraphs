import networkx
import itertools

def blue_red_balanced_degrees(G,coloring,orientation):

    blue_red_sums = [[] for i in range(networkx.number_of_nodes(G))]

    for v in G.nodes():
        blue_sum = 0
        red_sum = 0
        for u in networkx.neighbors(G, v):
            # the edge is stored as (min(u,v),max(u,v))

            # sgn denotes wheter v is the start or the end of e
            sgn = 1
            if u < v:
                sgn = -1

            e = (min(u, v), max(u, v))
            if coloring[e] == "b":
                blue_sum = blue_sum + sgn * orientation[e]
            else:
                red_sum = red_sum + sgn * orientation[e]

        blue_red_sums[v] = [blue_sum, red_sum]

    return blue_red_sums

def is_conflict_in_the_middle(G,coloring,orientation):
    blue_red_sums = blue_red_balanced_degrees(G,coloring,orientation)

    for i in range(1, len(edgelist) - 1):  # first and last edges are the ones precolored
        e = edgelist[i]
        if (coloring[e] == "b" and blue_red_sums[e[0]][0] == blue_red_sums[e[1]][0]) or \
                (coloring[e] == "r" and blue_red_sums[e[0]][1] == blue_red_sums[e[1]][1]):
            return True, blue_red_sums

    return False, blue_red_sums

def solve_for_middle(edgelist,orientations):
    G = networkx.from_edgelist(edgelist)

    for or_first,or_last in itertools.product([1,-1],repeat=2):
        col_first = "b"
        for col_last in ["b","r"]:



            for orientation_array in orientations:

                obtained_degrees = []

                for col_middle in itertools.product(["b","r"],repeat=len(edgelist)-2):
                    orientation = dict(zip(edgelist, [or_first] + orientation_array + [or_last]))
                    coloring = dict(zip(edgelist, [col_first] + list(col_middle) + [col_last]))
                    #print(col_middle)
                    #print([col_first] + list(col_middle) + [col_last])
                    #print(coloring)

                    conflict, blue_red_sums = is_conflict_in_the_middle(G,coloring,orientation)
                    if not conflict:
                        # col_first is always "b"
                        if col_last == "b":
                            obtained_degrees = obtained_degrees + [[blue_red_sums[1][0], blue_red_sums[networkx.number_of_nodes(G)-2][0]]]
                        else:
                            obtained_degrees = obtained_degrees + [[blue_red_sums[1][0], blue_red_sums[networkx.number_of_nodes(G)-2][1]]]


                # here we test all possible degrees of vertices 0 and (n-1)
                # rough estimates are that these degrees are between -4 and 4
                for sigma_first, sigma_last in itertools.product(range(-4,5),range(-4,5)):
                    # there are some cases that we consider but in reality they are impossible to obtain
                    # e.g. 0->1 and sigma_first = -1
                    # we skip these cases
                    if (sigma_first == -1 and orientation[(0,1)]==1) \
                            or (sigma_first== 1 and orientation[(0,1)]==-1) \
                            or (sigma_last == 1 and orientation[(networkx.number_of_nodes(G)-2, networkx.number_of_nodes(G)-1)] == 1) \
                            or (sigma_last == -1 and orientation[(networkx.number_of_nodes(G)-2, networkx.number_of_nodes(G)-1)] == -1):
                        continue

                    can_finish_coloring = False
                    for degree_pair in obtained_degrees:
                        if sigma_first != degree_pair[0] and sigma_last != degree_pair[1]:
                            can_finish_coloring = True
                            break

                    if not can_finish_coloring:
                        print("I could not find a coloring for this situation:")
                        print("Edges: " + str(edgelist))
                        print("Orientation: " + str(orientation))
                        print("Partial coloring (left, right): " + col_first + ", " + col_last)
                        print("Sigma (left, right):" + str(sigma_first) + ", " + str(sigma_last))
                        print()
                        #return

if __name__ == '__main__':
    edgelist = [(0,1),(1,2),(1,3),(1,4),(4,5)]
    orientations = [[-1,1,1],[-1,1,-1]]
    solve_for_middle(edgelist,orientations)

    edgelist = [(0,1),(1,2),(1,4),(3,4),(4,5)]
    orientations = [[-1,1,1],[-1,1,-1],[1,1,1],[1,1,-1]]
    solve_for_middle(edgelist,orientations)

    edgelist = [(0,1),(1,2),(1,3),(1,5),(4,5),(5,6)]
    orientations = [[-1,1,1,1],[-1,1,1,-1],[-1,1,-1,1],[-1,1,-1,-1]]
    solve_for_middle(edgelist,orientations)

    edgelist = [(0,1),(1,2),(1,3),(1,6),(4,6),(5,6),(6,7)]
    orientations = [[1,-1,1,-1,1]]
    solve_for_middle(edgelist,orientations)

    edgelist = [(0,1),(1,2),(1,3),(3,4),(4,5)]
    orientations = [list(x) for x in itertools.product([1,-1],repeat=3)]
    solve_for_middle(edgelist,orientations)

    edgelist = [(0,1),(1,2),(1,3),(3,5),(4,5),(5,6)]
    orientations = [list(x) for x in itertools.product([1,-1],repeat=4)]
    solve_for_middle(edgelist,orientations)

    #edgelist = [(0, 1), (1, 2), (1, 3), (3, 4)]
    #orientations = [list(x) for x in itertools.product([1, -1], repeat=2)]
    #solve_for_middle(edgelist, orientations)


    #G = networkx.from_edgelist(edgelist)
    """col_middle = ["r","b","b"]

    col_first = "b"
    col_last = "r"
    or_first = 1
    or_last = -1

    # how to count color degrees
    orientation = dict(zip(edgelist, [or_first]+orientations[0]+[or_last]))
    coloring = dict(zip(edgelist, [col_first]+col_middle+[col_last]))

    conflict_in_the_middle = is_conflict_in_the_middle(G,coloring,orientation)
    print(conflict_in_the_middle)

    print(G)"""
