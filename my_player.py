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
        #TODO
        possible_actions = current_state.get_possible_actions()
        if kwargs:
            pass
        # attribution du joueur se fait par rapport a l'odre de la ligne de commande
        players =  [ player  for player in current_state.players]
        my_player_id = None
        place = 0
        for player in players :
            if player.name.startswith("my_player"):
                my_player_id = player.get_id()
                break
            place += 1
        print('player',type(list(list(current_state.get_possible_actions())[0].get_next_game_state().generate_possible_actions())[0].get_next_game_state().get_scores()[my_player_id]))
        print(current_state.get_scores()[my_player_id])
        max_action = self.heuristic(current_state,my_player_id,place)
        print('######',max_action)
        #print('action',my_actions)
        # [print(*x) for x in current_state.get_rep().get_grid()]
        # [print(a, b.__dict__) for a, b in current_state.get_rep().env.items()]
        possible_actions = current_state.get_possible_actions()
        random.seed("seahorse")
        if kwargs:
            pass
        #print(list(possible_actions))
        return max_action


    def heuristic(self, current_state : GameState, my_player_id : int, place : int): #vision a deux pas dans le future, why not rajouter un para
        #but premier maximiser le score à deux pas
        A1 = list(current_state.get_possible_actions())
        score2 = {} #min score  -6, nbr pice = 14
        score1 = {}
        #on initialise le score par chaque premier choix et le choix menant a ce score
        a1_idx = -1
        for a1 in A1 : #pour chaque état parent
            a1_idx += 1
            A2 = list(a1.get_next_game_state().generate_possible_actions()) #j obtient une nouvelle liste d action possible
            a2_idx = -1
            score2_1 = {}
            i=0
            for a2 in A2 :
                a2_idx += 1
                score = a2.get_next_game_state().get_scores()[my_player_id]
                score2_1[str(i)]= score
            score2[]
                i+=1
            # Calculer la distance au centre, avec une moyenne, de nos billes
        return A1[a1_idx]
    # def minimax(state, depth, maximizing_player):
    #     if depth == 0 or game_over(state):
    #         return evaluate(state)
    #
    #     if maximizing_player:
    #         max_eval = float('-inf')
    #         for child_state in get_possible_moves(state):
    #             eval = minimax(child_state, depth - 1, False)
    #             max_eval = max(max_eval, eval)
    #         return max_eval
    #     else:
    #         min_eval = float('inf')
    #         for child_state in get_possible_moves(state):
    #             eval = minimax(child_state, depth - 1, True)
    #             min_eval = min(min_eval, eval)
    #         return min_eval
    #
    # def get_best_move(state):
    #     best_move = None
    #     max_eval = float('-inf')
    #
    #     for child_state in get_possible_moves(state):
    #         eval = minimax(child_state, depth=2, maximizing_player=False)
    #         if eval > max_eval:
    #             max_eval = eval
    #             best_move = child_state
    #
    #     return best_move

