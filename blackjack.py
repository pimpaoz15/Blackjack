"""
BLACKJACK HOUSE EDGE BASED ON RULE VARIANTS:

RULE VARIANTS	                          HOUSE EDGE
Single deck, dealer stands on soft 17	  0.17%
Double deck, dealer stands on soft 17	  0.46%
6 decks, dealer stands on soft 17	      0.64%
6 decks, dealer hits on soft 17	        0.84%

NOTES:
- The fewer the decks, the better the odds for the player.
- A dealer standing on soft 17 improves the player's chances.
- These house edges assume the use of perfect basic or advanced strategy.
"""

# --------------------------------------------------------------------------------
# IMPORTS AND CONSTANTS
# --------------------------------------------------------------------------------
card_values = {
    "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
    "7": 7, "8": 8, "9": 9, "10": 10,
    "J": 10, "Q": 10, "K": 10, "A": 11
}

dealer_stands_on_soft = 16  # Default setting, updated at runtime

# --------------------------------------------------------------------------------
# FUNCTIONS
# --------------------------------------------------------------------------------
# Calculate the total value of a hand
def calculate_hand_value(hand):
    value = sum(card_values[card] for card in hand)
    # Adjust for aces
    aces = hand.count("A")
    while value > 21 and aces:
        value -= 10
        aces -= 1
    return value

# Advanced strategy rules
def advanced_strategy(player_hand, dealer_card, allow_double=True):
    player_value = calculate_hand_value(player_hand)
    dealer_value = card_values[dealer_card]
    is_soft = "A" in player_hand and player_value <= 21

    # Blackjack or bust
    if player_value == 21 and len(player_hand) == 2:
        return "Stand"
    if player_value > 21:
        return "Bust"

    # Splitting rules
    if len(player_hand) == 2 and player_hand[0] == player_hand[1]:
        pair_card = player_hand[0]
        if pair_card in ["A", "8"]:
            return "Split"
        if pair_card in ["2", "3"] and dealer_value <= 7:
            return "Split"
        if pair_card in ["6"] and dealer_value <= 6:
            return "Split"
        if pair_card in ["7"] and dealer_value <= 7:
            return "Split"
        if pair_card in ["9"] and dealer_value not in [7, 10, "A"]:
            return "Split"

    # Doubling down
    if len(player_hand) == 2 and allow_double:
        if player_value == 10 or player_value == 11:
            if dealer_value < player_value:
                return "Double Down"
        if is_soft and player_value in [13, 14] and dealer_value in [4, 5, 6]:
            return "Double Down"
        if is_soft and player_value in [15, 16, 17] and dealer_value in [4, 5, 6]:
            return "Double Down"

    # Standing rules
    if player_value >= 17:
        return "Stand"
    if is_soft and player_value >= 19:
        return "Stand"
    if player_value in [13, 14, 15, 16] and dealer_value <= 6:
        return "Stand"

    # Hitting rules
    return "Hit"

# Simulate a round of blackjack
def play_blackjack():
    while True:
        print("\n--------------------\n")
        command = input("Type 'exit' or 'quit' to stop, or press Enter to play a new round: ").strip().lower()
        if command in ["exit", "quit"]:
            print("Thank you for playing!")
            break

        player_hand = input("Enter your initial hand (e.g., 'K A'): ").upper().split()
        dealer_card = input("Enter the dealer's visible card (e.g., '10'): ").upper()

        print(f"Your hand: {player_hand}, Total: {calculate_hand_value(player_hand)}")
        print(f"Dealer shows: {dealer_card}")

        while True:
            action = advanced_strategy(player_hand, dealer_card)
            print(f"Strategy suggests: {action}")

            if action == "Bust":
                print("You bust!")
                break
            elif action == "Stand":
                print("You stand. Waiting for dealer...")
                break
            elif action == "Double Down":
                print("Double Down! Draw one card.")
                new_card = input("Enter the card you drew: ").upper()
                player_hand.append(new_card)
                print(f"Your new hand: {player_hand}, Total: {calculate_hand_value(player_hand)}")
                break
            elif action == "Split":
                print("Splitting hand! Play each hand separately.")
                # Handle splitting logic if desired
                break
            elif action == "Hit":
                new_card = input("Enter the card you drew: ").upper()
                player_hand.append(new_card)
                print(f"Your new hand: {player_hand}, Total: {calculate_hand_value(player_hand)}")
                if calculate_hand_value(player_hand) > 21:
                    print("You bust!")
                    break

        # Dealer's turn (manual input for simplicity)
        dealer_hand = [dealer_card]
        while calculate_hand_value(dealer_hand) < (dealer_stands_on_soft + 1):
            new_card = input("Enter the card the dealer drew: ").upper()
            dealer_hand.append(new_card)
            print(f"Dealer's hand: {dealer_hand}, Total: {calculate_hand_value(dealer_hand)}")
            if calculate_hand_value(dealer_hand) > 21:
                print("Dealer busts! You win!")
                break

        # Determine winner
        player_total = calculate_hand_value(player_hand)
        dealer_total = calculate_hand_value(dealer_hand)
        if dealer_total > 21 or player_total > dealer_total:
            print("You win!")
        elif player_total < dealer_total:
            print("Dealer wins!")
        else:
            print("It's a tie!")

# --------------------------------------------------------------------------------
# MAIN FUNCTION
# --------------------------------------------------------------------------------
if __name__ == "__main__":
    print("Welcome to Blackjack!")
    while True:
        choice = input("Should the dealer stand on soft 17 (yes) or soft 16 (no)?: ").strip().lower()
        if choice in ["yes", "no"]:
            dealer_stands_on_soft = 17 if choice == "yes" else 16
            break
        print("Please enter 'yes' or 'no'.")
    play_blackjack()