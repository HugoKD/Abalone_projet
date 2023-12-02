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
        print('######', max_action)
        print(current_state.is_done())

        #print('action',my_actions)
        # [print(*x) for x in current_state.get_rep().get_grid()]
        # [print(a, b.__dict__) for a, b in current_state.get_rep().env.items()]
        possible_actions = current_state.get_possible_actions()
        random.seed("seahorse")
        if kwargs:
            pass
        #print(list(possible_actions))
        print(type(random.choice(list(possible_actions))))
        return random.choice(list(possible_actions))


    def heuristic(self, current_state : GameState, my_player_id : int, place : int): #vision a deux pas dans le future, why not rajouter un para
        #but premier maximiser le score à deux pas
        arbre_heuristic = ArbreHeuristic(current_state)
        A1 = list(current_state.get_possible_actions())
        score_niv_2 = {} # Enregistrer les scores des noeuds au niv 2
        score_niv_1 = {} #  Enregistrer les scores des noeuds au niv 1
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
                score2_1[str(i)]= (score,a2) #on store le score et l'action pour y parvenir
                i += 1
            score_niv_2[str(a1_idx)] = score2_1
        #on calcule maintenant score niv 1 en faisant un moyenne des scores de ces enfants pour ensuite choisir la meilleur action
        for key in score_niv_2.keys():
            score_niv_1[str(key)] = sum([x[0] for x in score_niv_2[key].values()])/(len(score_niv_2[key]))
        return score_niv_2# pas très pratique deux dictio
            # Calculer la distance au centre, avec une moyenne, de nos billes



class NoeudNonBinaire:
    def __init__(self, etat : GameState , action : Action, score : int ): # action : Action pour faire parent -> enfant
        self.etat = etat
        self.action = action
        self.enfants = [] # est ce que enfant = liste ?

    def ajouter_enfant(self, etat,action):
        nouvel_enfant = NoeudNonBinaire(etat,action)
        self.enfants.append(nouvel_enfant)

    def get_enfants(self):
        return self.enfants

class ArbreHeuristic:
    def __init__(self, etat : GameState):
        self.racine = NoeudNonBinaire(etat,action=None, score=0) # On commence avec toutes nos pièces

    def ajouter_enfant(self, parent, etat, action):
        # Recherche du parent dans l'arbre
        file = [self.racine]
        while file:
            noeud_courant = file.pop(0)
            if noeud_courant.etat == parent:
                # Ajout du nouvel enfant au parent trouvé
                noeud_courant.ajouter_enfant(etat)
                return
            else:
                file.extend(noeud_courant.get_enfants())

    def parcours_largeur(self):
        file = [self.racine]
        while file:
            noeud_courant = file.pop(0)
            print(noeud_courant.etat)
            file.extend(noeud_courant.get_enfants())

    def parcours_profondeur(self):  # A tester
        file = [self.racine]
        print(file)
        while file:
            noeud_courant = file.pop()
            print(noeud_courant.etat)
            file.extend(noeud_courant.get_enfants())