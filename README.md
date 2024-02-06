# rrt_project - MSR Hackathon RRT Project 

### Overview
The Rapidly-Exploring Random Tree (RRT) is a widely used algorithm in the field of robotics and motion planning. Introduced by Steven M. LaValle in 1998, RRT is designed to efficiently explore and navigate high-dimensional spaces, making it particularly suited for complex environments. The algorithm incrementally builds a tree structure by randomly sampling configuration points and connecting them to the existing tree through locally optimal paths. This approach allows RRT to quickly explore the configuration space, making it well-suited for real-time applications. RRT has been utilized in robotics for tasks such as motion and path planning, contributing to the improvement of autonomous robots' ability to navigate and make decisions in complex environments.

### Usage and Output
The start and goal locations can either be randomly generated or specified by the user. Similarly, circular obstacles can either be randomly generated or manually placed by entering coordinates for the center point and a radius of the obstacle. Below is an example of the algorithm being used on randomly generated obstacles. The start position is marked with an orange dot, the goal is marked with a blue dot, and the blue path indicates the path found from the start to the goal.

<img src="scferro.github.io/assets/rrt_2.png"/>


Obstacles can also be specified using a binary image file. Black pixels are considered to be occupied by obstacles, while white pixels are considered empty. Circular obstacles are created to occupy any black pixels in the image, with a higher density of smaller obstacles used for any pixels that are border an empty white pixel. Below is the RRT navigating around the Northwestern "N". 

<img src="scferro.github.io/assets/rrt_4.png"/>

<br>

### RRT Algorithm
For this project, the following RRT algorithm was used to navigate from a start point to a goal point while avoiding obstacles.

Input:

    q_start: The start point

    q_goal: The point that the tree is attempting to reach

    K: Current number of vertices in RRT

    K_max: Maximum allowed number of vertices in RRT

    Δ: Incremental distance

    D: The planning domain

Output:

    G: the RRT

Algorithm:

    Initialize G with q_start

    WHILE K < K_max AND path to q_goal is not found:

        - q_rand ← RANDOM_POINT(D)

        - q_near ← NEAREST_VERTEX(q_rand, G)

        - q_new ← NEW_VERTEX(q_near, q_rand, Δ)

        - IF q_new is NOT located within an obstacle:

            - Add vertex q_new to G

            - Add an line segment between q_near and q_new in G

            - Check if straight line path from q_new to q_goal is obstacle free
            
            - K = K + 1

    return G

RANDOM_POINT randomly selects a point within the domain D.

NEAREST_VERTEX selects the vertex in G that is closest to the random point q_rand

NEW_VERTEX generates a new vertex in the tree by moving a distance Δ from one vertex towards another.

