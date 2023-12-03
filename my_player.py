from player_abalone import PlayerAbalone
from seahorse.game.action import Action
from seahorse.game.game_state import GameState
from seahorse.utils.custom_exceptions import MethodNotImplementedError
import random
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
        # [print(*x) for x in current_state.get_rep().get_grid()]
        # [print(a, b.__dict__) for a, b in current_state.get_rep().env.items()]
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
        heuristic_tree, hash_table = self.heuristic(current_state= current_state,my_player_id= my_player_id)
        arbre_scorer = heuristic_tree.get_tree() # on obtient un arbre de la forme HeuristicTree avec le score de chaque état décidé par notre heuristic
        # on appelle minimax

        v,m = heuristic_tree.minimax(game_state_parent= current_state, game_state = current_state, maximizingPlayer= True,heuristic_tree= heuristic_tree,hash_table= hash_table)


        possible_actions = current_state.get_possible_actions()
        random.seed("seahorse")
        if kwargs:
            pass
        return random.choice(list(possible_actions))




    def heuristic(self, current_state : GameState, my_player_id : int):
        #création d une table de hashage hash : state et d un arbre heuristique associant hash : score
        #but premier maximiser le score à deux pas
        # but deuxième minimiser la moyenne des distances au centre du plateau des billes
        hash_table = {}
        heuristicTree = HeuristicTree()
        A1 = list(current_state.get_possible_actions())
        for a1 in A1:
            etat1 = a1.get_next_game_state()
            a1_hash = etat1.__hash__() # On génère le hash des états
            A2 = list(etat1.generate_possible_actions()) # action possible à partir de état1
            hash_table[a1_hash] = etat1
            for a2 in A2 :
                etat2 = a2.get_next_game_state()
                a2_hash = etat2.__hash__()
                score = etat2.get_scores()[my_player_id]
                heuristicTree[a1_hash][a2_hash] = score # on store le score et le chemin pour y arriver
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

    def get_children(self, path_to_node: list):  # path = [a,b,c,d,e,f....] -> list[hash] or int
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

    def find_path_to_state(self, state, path=None):  # trouver path_to_action -> list[hash]
        if path is None:
            path = []
        for key, value in self.items():
            current_path = path + [key]

            if key == state:
                return current_path
            elif isinstance(value, dict):
                result = value.find_path_to_state(state, current_path)
                if result:
                    return result
        return None

    def find_path_to_hash(self, hash : int , path=None):  # trouver path_to_action -> list[hash]
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







# jusqu'a la sur à 100%






    def minimax(self, game_state_parent : GameState, game_state: GameState, maximizingPlayer: bool, heuristic_tree: dict, hash_table: dict, depth=2):
        # renvoie à partir d'un état la meilleure action (m) et sa valeur (v)
        # le premier appel on aura path = None
        path = []
        # Check for terminal conditions
        if game_state.is_done() or depth == 0: # on atteint les feuilles terminales
            # probleme je n'arrive pas a obtenir le score de game_state
            # pourquoi ? pb de type ?
            hash_table_list = list(hash_table.values())
            idx = hash_table_list.index(game_state)
            idx_parent = hash_table_list.index(game_state_parent)
            idx_key_parent = list(hash_table.keys())[idx_parent]
            idx_key = list(hash_table.keys())[idx]

            if idx == 0 :
                print(idx, idx_parent)
                print(idx_key, '  ',idx_key_parent)
                print('self_parent', self[idx_key])
                print('fptg',self.find_path_to_state(game_state_parent))
                print((heuristic_tree)[idx_parent])
                print(heuristic_tree.keys())
                print('-')

            return -1, path  # Assuming you have an evaluate_state function

        if maximizingPlayer:
            value = float('-inf')
            best_movement = None
            for child_hash in self.get_children(path):  # For move in possible moves
                child_node = hash_table[child_hash]
                child_value, _ = self.minimax( game_state_parent= game_state,
                    game_state=child_node, maximizingPlayer=False, hash_table=hash_table, heuristic_tree=heuristic_tree,
                    depth=depth - 1
                )
                if child_value > value:
                    value = child_value
                    best_movement = child_hash
        else:
            value = float('inf')
            best_movement = None
            for child_hash in self.get_children(path):
                child_node = hash_table[child_hash]
                child_value, _ = self.minimax( game_state_parent= game_state,
                    game_state=child_node, maximizingPlayer=True, hash_table=hash_table, heuristic_tree=heuristic_tree,
                    depth=depth - 1
                )
                if child_value < value:
                    value = child_value
                    best_movement = child_hash
        return value, best_movement

    """La fonction minimax doit donc renvoyer le score associé à l'état du jeu actuel.
     Si c'est un nœud de maximisation, vous renvoyez le score maximal parmi les enfants.
    Si c'est un nœud de minimisation, vous renvoyez le score minimal."""





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


