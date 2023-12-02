from player_abalone import PlayerAbalone
from seahorse.game.action import Action
from seahorse.game.game_state import GameState
from seahorse.utils.custom_exceptions import MethodNotImplementedError
import random
#algorithme de type minimax
class MyPlayer(PlayerAbalone):
    """
    Player class for Abalone game.

    Attributes:
        piece_type (str): piece type of the player
    """

    def __init__(self, piece_type: str, name: str = "bob", time_limit: float=60*15,*args) -> None:
        """
        Initialize the PlayerAbalone instance.

        Args:
            piece_type (str): Type of the player's game piece
            name (str, optional): Name of the player (default is "bob")
            time_limit (float, optional): the time limit in (s)
        """
        super().__init__(piece_type,name,time_limit,*args)


    def compute_action(self, current_state: GameState, **kwargs) -> Action:
        """
        Function to implement the logic of the player.

        Args:
            current_state (GameState): Current game state representation
            **kwargs: Additional keyword arguments

        Returns:
            Action: selected feasible action
        """
        # en moyenne on a ~ 50 actions possibles par état
        # [print(*x) for x in current_state.get_rep().get_grid()]
        # [print(a, b.__dict__) for a, b in current_state.get_rep().env.items()]
        possible_actions = current_state.get_possible_actions()
        if kwargs:
            pass
        # attribution du joueur se fait par rapport a l'odre de la ligne de commande
        players = [player for player in current_state.players]
        my_player_id = None
        place = 0
        for player in players:
            if player.name.startswith("my_player"):
                my_player_id = player.get_id()
                break
            place += 1

        arbre = self.heuristic(current_state= current_state,my_player_id= my_player_id)
        arbre_scorer = arbre.get_tree() # on obtient un arbre de la forme HeuristicTree avec le score de chaque état décidé par notre heuristic
        keys = list(arbre_scorer.keys())



        possible_actions = current_state.get_possible_actions()
        random.seed("seahorse")
        if kwargs:
            pass
        return random.choice(list(possible_actions))




    def heuristic(self, current_state : GameState, my_player_id : int): #vision a deux pas dans le future, why not rajouter un para
        #but premier maximiser le score à deux pas
        # but deuxième minimiser la moyenne des distances au centre du plateau des billes
        heuristicTree = HeuristicTree()
        A1 = list(current_state.get_possible_actions())
        for a1 in A1:
            A2 = list(a1.get_next_game_state().generate_possible_actions())
            for a2 in A2  :
                score = a2.get_next_game_state().get_scores()[my_player_id]
                heuristicTree[a1][a2] = score

        return heuristicTree





class HeuristicTree(dict):
    """Create tree with the use of dictionnaire """

    def __missing__(self, key):
        value = self[key] = type(self)()
        return value

    # cast a (nested) dict to a (nested) Tree class
    def __init__(self, data={}):
        for k, data in data.items():
            if isinstance(data, dict):
                self[k] = type(self)(data)
            else:
                self[k] = data

    def get_tree(self):
        return self

    # def evaluate(self):
    # def minimax(self, depth = 2, maximizing_player): # depth = pas, on est le joueur pour lequel on veut maximiser le socre = MyPlayer = maximizing_player (au début)
    #     if depth == 0 :
    #         return self.evaluate(node, my_player_id)



"""
Exemple : 

heursiticTree = HeuristicTree()

heursiticTree['a']['1']['x']  = '@'
heursiticTree['a']['1']['y']  = '#'
heursiticTree['a']['2']['x']  = '$'
heursiticTree['a']['3']       = '%'
heursiticTree['b']            = '*'

heursiticTree.get_tree()

--> {'a': {'1': {'x': '@', 'y': '#'}, '2': {'x': '$'}, '3': '%'}, 'b': '*'}
"""


# def find_best_move(self, depth):
#     maximizing_player = True  # Adjust as needed
#     best_score = float('-inf') if maximizing_player else float('inf')
#     best_move = None
#
#     for move, child in self.items():
#         score = self.minimax(child, depth, not maximizing_player)
#         if (maximizing_player and score > best_score) or (not maximizing_player and score < best_score):
#             best_score = score
#             best_move = move
#
#     return best_move
#
#
# """Definition of the decision algorithm -> minimax"""
#
#
# def minimax(self, node, maximizing_player, depth=2):
#     if depth == 0 or not node:
#         return self.evaluate(node)  # Implement your own evaluation function
#
#     if maximizing_player:
#         max_eval = float('-inf')
#         for child in node.values():
#             eval = self.minimax(child, False, depth - 1)
#             max_eval = max(max_eval, eval)
#         return max_eval
#     else:
#         min_eval = float('inf')
#         for child in node.values():
#             eval = self.minimax(child, True, depth - 1)
#             min_eval = min(min_eval, eval)
#         return min_eval
#
#
# def evaluate(self, node):
#     # Implement your own scoring/evaluation function based on the GameState
#     # This function should return a score for the given node
#     # You might want to use the GameState associated with the node for scoring
#     pass
#
#
# def find_best_move(self, depth):
#     maximizing_player = True  # Adjust as needed
#     best_score = float('-inf') if maximizing_player else float('inf')
#     best_move = None
#
#     for move, child in self.items():
#         score = self.minimax(child, depth, not maximizing_player)
#         if (maximizing_player and score > best_score) or (not maximizing_player and score < best_score):
#             best_score = score
#             best_move = move
#
#     return best_move