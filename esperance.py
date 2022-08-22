from random import randint, choice


def play_game_randomly(
    verbose: bool = True,
    nb_trees: int = 4,
    nb_fruits_per_tree: int = 10,
    puzzle_size: int = 9,
    fruits_if_panier: int = 2,
) -> tuple[int]:
    """Simulates one game of `Le verger` with random play

    Args:
        verbose (bool, optional): whether to comment the game. Defaults to True.
        nb_trees (int, optional): number of trees from which to get fruits. Defaults to 4.
        nb_fruits_per_tree (int, optional): number of fruits on each tree. Defaults to 10.
        puzzle_size (int, optional): number of pieces that make up the raven's puzzle. Defaults to 9.
        fruits_if_panier (int, optional): in case the dice yields the 'panier', you are allowed to pick that many fruits. Defaults to 2.

    Returns:
        tuple[int]: winner (0: raven, 1:player), number of turns played before the game ended
    """
    puzzle = 0
    fruits = 0
    nb_turns = 0
    total_fruits = nb_trees * nb_fruits_per_tree
    fruits_dict = {i: nb_fruits_per_tree for i in range(1, nb_trees + 1)}
    if verbose:
        print(f"Fruits_dict: {fruits_dict}\n")
    while fruits < total_fruits and puzzle < puzzle_size:
        # draw dice
        dice = randint(1, 6)
        if verbose:
            print(f"\nDice: {dice}")
        if dice == nb_trees + 2:  # raven: add one piece to the puzzle
            puzzle += 1
            if verbose:
                print(f"Puzzle has {puzzle} piece(s)\n")
        if dice in range(1, nb_trees + 1):  # 1 to 4 included
            if fruits_dict[dice]:  # there are fruits on this tree
                fruits_dict[dice] -= 1
                fruits += 1
            if verbose:
                print(f"Fruits_dict: {fruits_dict}, fruits picked: {fruits}\n")
        if dice == nb_trees + 1:  # panier: pick randomly any 2 fruits, if available
            if verbose:
                print("Panier!")
            for _ in range(fruits_if_panier):
                available_trees = [
                    tree for tree in range(1, nb_trees + 1) if fruits_dict[tree]
                ]
                if available_trees:
                    tree_random = choice(available_trees)
                    if verbose:
                        print(f"Picked {tree_random}")
                    fruits_dict[tree_random] -= 1
                    fruits += 1
            if verbose:
                print(f"Fruits_dict: {fruits_dict}, fruits picked: {fruits}\n")
        nb_turns += 1
    if puzzle == puzzle_size:
        if verbose:
            print(f"Raven wins in {nb_turns} turns")
        return 0, nb_turns
    if verbose:
        print(f"I win in {nb_turns} turns")
    return 1, nb_turns


def play_game_optimized(
    verbose: bool = True,
    nb_trees: int = 4,
    nb_fruits_per_tree: int = 10,
    puzzle_size: int = 9,
    fruits_if_panier: int = 2,
) -> tuple[int]:
    """Simulates one game of `Le verger` with optimized play: when drawing 'panier', pick the `fruits_if_panier` fruits
    from the trees that have the largest number of fruits available.

    Args:
        verbose (bool, optional): whether to comment the game. Defaults to True.
        nb_trees (int, optional): number of trees from which to get fruits. Defaults to 4.
        nb_fruits_per_tree (int, optional): number of fruits on each tree. Defaults to 10.
        puzzle_size (int, optional): number of pieces that make up the raven's puzzle. Defaults to 9.
        fruits_if_panier (int, optional): in case the dice yields the 'panier', you are allowed to pick that many fruits. Defaults to 2.

    Returns:
        tuple[int]: winner (0: raven, 1:player), number of turns played before the game ended
    """
    puzzle = 0
    fruits = 0
    nb_turns = 0
    total_fruits = nb_trees * nb_fruits_per_tree
    fruits_dict = {i: nb_fruits_per_tree for i in range(1, nb_trees + 1)}
    if verbose:
        print(f"Fruits_dict: {fruits_dict}\n")
    while fruits < total_fruits and puzzle < puzzle_size:
        # draw dice
        dice = randint(1, 6)
        if verbose:
            print(f"\nDice: {dice}")
        if dice == nb_trees + 2:  # raven: add one piece to the puzzle
            puzzle += 1
            if verbose:
                print(f"Puzzle has {puzzle} piece(s)\n")
        if dice in range(1, nb_trees + 1):  # 1 to 4 included
            if fruits_dict[dice]:  # there are fruits on this tree
                fruits_dict[dice] -= 1
                fruits += 1
            if verbose:
                print(f"Fruits_dict: {fruits_dict}, fruits picked: {fruits}\n")
        if dice == nb_trees + 1:  # a smarter way to pick the 2 fruits
            if verbose:
                print("Panier!")
            for _ in range(fruits_if_panier):
                available_trees = [
                    tree for tree in range(1, nb_trees + 1) if fruits_dict[tree]
                ]
                if available_trees:
                    tree_best = max(
                        available_trees, key=fruits_dict.get
                    )  # pick the tree with the most fruits so as to preserve rarer fruits
                    if verbose:
                        print(f"Picked {tree_best}")
                    fruits_dict[tree_best] -= 1
                    fruits += 1
            if verbose:
                print(f"Fruits_dict: {fruits_dict}, fruits picked: {fruits}\n")
        nb_turns += 1
    if puzzle == puzzle_size:
        if verbose:
            print(f"Raven wins in {nb_turns} turns")
        return 0, nb_turns
    if verbose:
        print(f"I win in {nb_turns} turns")
    return 1, nb_turns


nb_games_experiment = 100_000
games = [play_game_randomly(verbose=False) for _ in range(nb_games_experiment)]
turns = [game[1] for game in games]
winners = [game[0] for game in games]
print(
    f"""En moyenne après {nb_games_experiment} parties jouées randomly, la partie se décide en {round(sum(turns)/len(turns),2)} tours\n
Stats: {round(sum(winners)*100/len(winners),2)}% de victoires"""
)

games = [play_game_optimized(verbose=False) for _ in range(nb_games_experiment)]
turns = [game[1] for game in games]
winners = [game[0] for game in games]
print(
    f"""En moyenne après {nb_games_experiment} parties jouées mieux, la partie se décide en {round(sum(turns)/len(turns),2)} tours\n
Stats: {round(sum(winners)*100/len(winners),2)}% de victoires"""
)
