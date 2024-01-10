$ python3 -m venv env
$ . env/bin/activate
$ pip install -r requirements.txt
$ python3 main.py

Without a heuristic, A* is Dijkstra. Here is a shortest path:
####################
#                  #
#                  #
#                  #
#       S+++++     #
#            +     #
#    ########+     #
#          E++     #
####################

Dijkstra explores the world from start outward (. = visited)
####################
#...............   #
#................  #
#................. #
#.......S+++++.....#
#............+.... #
#....########+...  #
# .....    E++..   #
####################

With a heuristic, A* searches "best first"
####################
#                  #
#       ....       #
#      ......      #
#     ..S+++..     #
#     .....+++     #
#    ########+     #
#          E++     #
####################
