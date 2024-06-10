from typing import List, Tuple


# List of scheduled opperation, used as a STACK
scheduled_operations: List[str] = []

MOVE = {
    "H": (0, -1),
    "B": (0, 1),
    "D": (1, 0),
    "G": (-1, 0)
}
DIRECTION = (
    ("H", (0, -1)),
    ("B", (0, 1)),
    ("D", (1, 0)),
    ("G", (-1, 0))
)

# The idea here is to stalk the opponent
def main(maze: List[List[str]], pos_self: Tuple[int, int], pos_enemy: Tuple[int, int]) -> str:

    # If any opperation are scheduled, do them
    if scheduled_operations != []:
        return scheduled_operations.pop()

    # If the opponent's position is not the same as ours, we go back to them
    if pos_enemy != pos_self:
        delta = (pos_enemy[0]-pos_self[0], pos_enemy[1]-pos_self[1])
        match delta:
            case (0, -1):  return "H"  # Move UP
            case (0, 1):   return "B"  # Move DOWN
            case (-1, 0):  return "G"  # Move LEFT
            case (1, 0):   return "D"  # Move RIGHT
            case _:  # If the opponent isn't nearby
                # Dijkstra algorithm to go back to the opponent or the nearest cheese
                list_pos = (pos_self,)
                maze[pos_self[1]][pos_self[0]] = "."
                while True:
                    next_list_pos = []
                    for pos in list_pos:
                        for move, delta in DIRECTION:
                            new_pos = (pos[0] + delta[0], pos[1] + delta[1])
                            if maze[new_pos[1]][new_pos[0]] == "$" or (new_pos[0], new_pos[1]) == pos_enemy:
                                scheduled_operations.append(move)
                                pos = (new_pos[0] - MOVE[move][0], new_pos[1] - MOVE[move][1])
                                while pos != pos_self:
                                    move = maze[pos[1]][pos[0]]
                                    scheduled_operations.append(move)
                                    pos = (pos[0] - MOVE[move][0], pos[1] - MOVE[move][1])
                                return scheduled_operations.pop()
                            elif maze[new_pos[1]][new_pos[0]] == " ":
                                maze[new_pos[1]][new_pos[0]] = move
                                next_list_pos.append(new_pos)
                    list_pos = tuple(next_list_pos)

    # Else we try to get to a cheese if there is one nearby
    if maze[pos_self[1]-1][pos_self[0]] == "$":
        scheduled_operations.append("B")
        return "H"
    if maze[pos_self[1]+1][pos_self[0]] == "$":
        scheduled_operations.append("H")
        return "B"
    if maze[pos_self[1]][pos_self[0]-1] == "$":
        scheduled_operations.append("D")
        return "G"
    if maze[pos_self[1]][pos_self[0]+1] == "$":
        scheduled_operations.append("G")
        return "D"