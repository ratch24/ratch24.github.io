import itertools

ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]
suits = ["♥", "♦", "♣", "♠"]

deck = []
for rank in ranks:
    for suit in suits:
        deck.append(f"{rank} of {suit}")


num_players = int(input("How many players? "))


players = {}
for i in range(1, num_players + 1):
    players[f"Player {i}"] = {"chips": 100, "hand": [], "folded": False}


for player in players:
    players[player]["hand"].append(deck.pop())
    players[player]["hand"].append(deck.pop())


print("\n--- Pre-Flop Betting Stage ---")

for player in players:
    if not players[player]["folded"]:
        print(f"{player}, you have {players[player]['chips']} chips.")
        bet = int(input(f"{player}, how much would you like to bet? (0 to check, -1 to fold) "))
        if bet == -1:
            players[player]["folded"] = True
            print(f"{player} folds!")
        elif bet > players[player]["chips"]:
            print("You can't bet more than you have!")
            bet = players[player]["chips"]
        players[player]["chips"] -= bet
        pot += bet


community_cards = [deck.pop() for _ in range(3)]
print("\nCommunity Cards (Flop):")
for card in community_cards:
    print(card)


print("\n--- Post-Flop Betting Stage ---")
for player in players:
    if not players[player]["folded"]:
        print(f"{player}, you have {players[player]['chips']} chips.")
        bet = int(input(f"{player}, how much would you like to bet? (0 to check, -1 to fold) "))
        if bet == -1:
            players[player]["folded"] = True
            print(f"{player} folds!")
        elif bet > players[player]["chips"]:
            print("You can't bet more than you have!")
            bet = players[player]["chips"]
        players[player]["chips"] -= bet
        pot += bet


turn_card = deck.pop()
community_cards.append(turn_card)
print(f"\nCommunity Card (Turn): {turn_card}")


print("\n--- Turn Betting Stage ---")
for player in players:
    if not players[player]["folded"]:
        print(f"{player}, you have {players[player]['chips']} chips.")
        bet = int(input(f"{player}, how much would you like to bet? (0 to check, -1 to fold) "))
        if bet == -1:
            players[player]["folded"] = True
            print(f"{player} folds!")
        elif bet > players[player]["chips"]:
            print("You can't bet more than you have!")
            bet = players[player]["chips"]
        players[player]["chips"] -= bet
        pot += bet


river_card = deck.pop()
community_cards.append(river_card)
print(f"\nCommunity Card (River): {river_card}")


print("\n--- River Betting Stage ---")
for player in players:
    if not players[player]["folded"]:
        print(f"{player}, you have {players[player]['chips']} chips.")
        bet = int(input(f"{player}, how much would you like to bet? (0 to check, -1 to fold) "))
        if bet == -1:
            players[player]["folded"] = True
            print(f"{player} folds!")
        elif bet > players[player]["chips"]:
            print("You can't bet more than you have!")
            bet = players[player]["chips"]
        players[player]["chips"] -= bet
        pot += bet


print("\n--- Determining the Winner ---")

def evaluate_hand(cards):
    ranks_order = {rank: i for i, rank in enumerate(ranks)}
    suits_count = {suit: 0 for suit in suits}
    rank_count = {rank: 0 for rank in ranks}

    for card in cards:
        rank, suit = card.split(" of ")
        rank_count[rank] += 1
        suits_count[suit] += 1

    is_flush = max(suits_count.values()) >= 5
    sorted_ranks = sorted([ranks_order[rank] for rank in rank_count if rank_count[rank] > 0], reverse=True)

    # Check for straight
    is_straight = False
    for i in range(len(sorted_ranks) - 4):
        if sorted_ranks[i] - sorted_ranks[i + 4] == 4:
            is_straight = True
            break

    # Check for straight flush
    if is_flush and is_straight:
        return 8000 + max(sorted_ranks)

    # Check for four of a kind
    if 4 in rank_count.values():
        return 7000 + max(ranks_order[rank] for rank, count in rank_count.items() if count == 4)

    # Check for full house
    if 3 in rank_count.values() and 2 in rank_count.values():
        return 6000 + max(ranks_order[rank] for rank, count in rank_count.items() if count == 3)

    # Check for flush
    if is_flush:
        return 5000 + sum(sorted_ranks[:5])

    # Check for straight
    if is_straight:
        return 4000 + max(sorted_ranks)

    # Check for three of a kind
    if 3 in rank_count.values():
        return 3000 + max(ranks_order[rank] for rank, count in rank_count.items() if count == 3)

    # Check for two pair
    pairs = [ranks_order[rank] for rank, count in rank_count.items() if count == 2]
    if len(pairs) >= 2:
        return 2000 + sum(sorted(pairs, reverse=True)[:2])

    # Check for one pair
    if 2 in rank_count.values():
        return 1000 + max(ranks_order[rank] for rank, count in rank_count.items() if count == 2)

    # High card
    return sum(sorted_ranks[:5])

best_hands = {}
for player in players:
    if not players[player]["folded"]:
        all_cards = players[player]["hand"] + community_cards
        all_combinations = itertools.combinations(all_cards, 5)
        best_hand_value = max(evaluate_hand(comb) for comb in all_combinations)
        best_hands[player] = best_hand_value

# Find the player(s) with the best hand
max_hand_value = max(best_hands.values())
winners = [player for player, value in best_hands.items() if value == max_hand_value]

# Distribute the pot
if len(winners) == 1:
    winner = winners[0]
    players[winner]["chips"] += pot
    print(f"{winner} wins the pot of {pot} chips!")
else:
    split_pot = pot // len(winners)
    for winner in winners:
        players[winner]["chips"] += split_pot
    print(f"It's a tie! {', '.join(winners)} split the pot, each receiving {split_pot} chips.")

# Final Results
print("\n--- Final Results ---")
for player in players:
    print(f"{player}: {players[player]['chips']} chips")

print("\nCommunity Cards:")
for card in community_cards:
    print(card)


 
 