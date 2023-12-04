from player_abalone import PlayerAbalone
from seahorse.game.action import Action
from seahorse.game.game_state import GameState
from seahorse.utils.custom_exceptions import MethodNotImplementedError
import random
from time import sleep
#algorithme de type minimax
# on explore que 2 niveaux. Current_state -> Action_adverser -> Prochain_state
# on suppose que forcement, a partir d un état on a au moins deux actions possibles
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
        players = [player for player in current_state.players]
        my_player_id = None
        place = 0
        for player in players:
            if player.name.startswith("my_player"):
                my_player_id = player.get_id()
                break
            place += 1 #if place = 0 : white, else : black
        if place == 1 : place_adverse = 0
        else : place_adverse = 1
        grid = [x for x in current_state.get_rep().get_grid()]
        distance = self.distance_moyenne(grid, place)


        heuristic_tree, hash_table = self.heuristic(current_state= current_state,my_player_id= my_player_id, place= place, place_adverse= place_adverse)

        # on appelle minimax

        v,m_hash = heuristic_tree.minimax()
        next_state = hash_table[m_hash]
        best_action = Action(current_state, next_state)

        return best_action


    def distance_moyenne(self, board: list[list], piece: int, x_m=4, y_m=4) -> float:
        distance = 0
        nbr_piece = 0
        piece_char = 'W' if piece == 0 else 'B'

        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == piece_char:
                    distance += self.distance_euclidienne(j, x_m, i, y_m)
                    nbr_piece += 1

        return distance / max(1, nbr_piece)  # Avoid division by zero, assuming nbr_piece is always non-negative

    def distance_euclidienne(self, x_elmt, x_m, y_elmt, y_m):
        return ((y_m - y_elmt) ** 2 + (x_m - x_elmt) ** 2) ** 0.5

    def heuristic(self, current_state : GameState, my_player_id : int, place : int, place_adverse : int, W_score =.9, W_distance = .5):
        #création d une table de hashage hash : state et d un arbre heuristique associant hash : score
        #but premier maximiser le score à deux pas
        #but deuxième minimiser la moyenne des distances au centre du plateau des billes
        #Fonction du score attribué aux déplacements favorisant l’éjection de billes, on veut que le score de l'adv soit plus faible qu'au début
        x_m,y_m = 4,4 # coordonnée du centre du board
        hash_table = {}
        heuristicTree = HeuristicTree()
        A1 = list(current_state.get_possible_actions())
        score0 = list(current_state.scores.values())[place_adverse]
        for a1 in A1:
            etat1 = a1.get_next_game_state()
            a1_hash = etat1.__hash__() # On génère le hash des états
            A2 = list(etat1.generate_possible_actions()) # action possible à partir de état1
            score1 = list(etat1.scores.values())[place_adverse]
            epsilon = 0
            if score1 < score0:
                epsilon +=100000
            hash_table[a1_hash] = etat1
            for a2 in A2 :
                etat2 = a2.get_next_game_state()
                grid = [x for x in etat2.get_rep().get_grid()]
                distance = self.distance_moyenne(grid,place)
                score2 = list(etat2.scores.values())[place_adverse]
                if score2 < score1:
                    epsilon +=50000
                a2_hash = etat2.__hash__()
                score = round(W_score * etat2.get_scores()[my_player_id] - W_distance *distance - 100000*epsilon,4)*10000
                heuristicTree[a1_hash][a2_hash] = int(score) # pb : le score ne peut pas etre au chose qu'un int ...
                hash_table[a2_hash] = etat2
        return heuristicTree, hash_table







class HeuristicTree(dict): # tout transformer en hash
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

    def get_children(self, path_to_node: list) -> list[int] or int: # return list si noeud non final, int = score sinon
        if path_to_node == []:
            x = list(self.keys())
            return x
        x = self[path_to_node[0]]
        for i in range(1, len(path_to_node)):
            x = x[path_to_node[i]]
        if isinstance(x, int):
            return x
        elif isinstance(x, dict):
            return list(x.keys())
        #return list hash or valeur node = function evaluate

    def find_path_to_hash(self, hash : int , path=None) -> list[int]:  # trouver path_to_action
        if path is None:
            path = []

        for key, value in self.items():
            current_path = path + [key]

            if key == hash:
                return current_path
            elif isinstance(value, dict):
                result = value.find_path_to_hash(hash, current_path)
                if result:
                    return result
        return None


    def minimax(self, maximizingPlayer = True, game_state_hash = 0000000000, depth = 2):

        if game_state_hash == 0000000000 :
            path_to_hash = [] # ie on est la racine
        else :
            path_to_hash = self.find_path_to_hash(game_state_hash)

        children = self.get_children(path_to_hash)

        if depth == 0: # ie get children = int
            score = self.get_children(path_to_node= path_to_hash)
            return score, path_to_hash

        if maximizingPlayer :
            value = float('-inf')
            for child in children : # child is hash
                tmp= float(self.minimax(game_state_hash= child,maximizingPlayer= False, depth= depth - 1)[0])
                if type(tmp) == list:
                    tmp = tmp[0]
                if tmp > value:
                    value = tmp
                    best_movement = child
        else :
            value = float('inf')
            for child in children: # child is hash
                tmp= self.minimax(game_state_hash=child, maximizingPlayer= True, depth=depth - 1)[0]
                if type(tmp) == list :
                    tmp = tmp[0]
                if tmp < value:
                    value = tmp
                    best_movement = child

        return value, best_movement











"""
Exemple : 
# remarque, conception supposant qu'on a que deux niveau racine -> a-b-c-> i
heursiticTree = HeuristicTree()

heursiticTree['a']['1']  = 0
heursiticTree['a']['1']  = 1
heursiticTree['a']['2']  = 4
heursiticTree['a']['3']  = 3
heursiticTree['b']["1"]  = -6 # arbre respectant nos assumptions : 1) au moins deux actions possibles a chaque etat ; 2) que deux niveaux d'actions dans le futur
heursiticTree['b']["2"]  = -6
heursiticTree['c']['1']  = -1
heursiticTree['c']['2']  = -1
heursiticTree['c']['3']  = -1
heursiticTree['c']['4']  = -1 #les clefs des nodes sont des hash !! 

heursiticTree.get_tree()

action adverser -> current_state 
de ce current_state je peux faire l'action a,b ou c. 1,2,3,4 action adverse, je peux de nouveau faire une action 

->> {'hash1': {hash4: 1, hash5 : 4, hash6: 3},'hash2': {hash7:  -6, hash8: -6},'hash3': {hash9: -1, hash10: -1, hash11: -1, hash12 : -1}}
 
->> {
    hash1: {
        hash4: 1,
        hash5: 4, 
        hash6: 3
    },
    hash2: {
        hash7: -6,
        hash8: -6
    },
    hash3: {
        hash9: -1,
        hash10: -1,
        hash11: -1,
        hash12: -1}
    }
"""


