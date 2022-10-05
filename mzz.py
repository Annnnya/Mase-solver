from maze import Maze, build_maze

maze = build_maze('./mazefile.txt')
maze.find_path()
print(maze)
print()
maze.reset()
print(maze)
