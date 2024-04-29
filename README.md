# Abalone_projet

Créer un agent intelligent capable de jouer au jeu Abalone. Abalone est un jeu de stratégie au tour par tour, en un contre un, dont le principe est simple : expulser un maximum de billes de l’adversaire hors
du plateau. Ce plateau sur lequel le jeu se déroule est percé de 61 cercles supportant les billes. Chaque joueur possède 14 billes disposées d’une manière bien définie au départ. Le joueur blanc commence. À chaque tour,
chaque joueur doit effectuer un et un seul déplacement dans n’importe quelle direction (horizontale, verticale, diagonale) sur une case adjacente. Ce mouvement revient à déplacer une ou plusieurs de ses billes (au
maximum 3) dans le même sens.

Ces mouvements doivent cependant respecter quelques règles :
• On doit toujours déplacer des billes adjacentes.
• Si l’on déplace plusieurs billes, cela doit uniquement se faire dans l’une des deux directions parallèles à la ligne formée par ces dernières. Les mouvements en flèche ne sont donc pas autorisés dans le cadre du projet!
• On peut pousser les billes adverses seulement si l’on est en supériorité numérique stricte et qu’il y a un espace vide (ou le bord du plateau) derrière la ligne formée par ces dernières.

La fin de partie est déclarée lorsque six billes d’une même équipe sont expulsées hors du plateau ou lorsque les 2 joueurs ont effectué 50 tours en tout (25 coups chacun). Le gagnant est décidé en comptant le nombre de billes perdues par chaque joueur. La majorité l’emporte. En cas d’égalité, c’est l’équipe ayant la plus petite somme des distances entre ses billes et le centre du plateau qui gagne. Dans le cas improbable ou il y a encore une égalité, alors il y a une égalité entre les deux agents.

![Texte alternatif](GUI/'Rapport annuel professionnel entreprise simple.png')

