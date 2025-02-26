import random
import os
import time
import threading

INVENTORY_FILE = "inventory.txt"
LEADERBOARD_FILE = "leaderboard.txt"

HUNGER = 50
HAPPINESS = 50
ENERGY = 50
CONSECUTIVE_WINNING_TURNS = 0

def save_to_file(filename, data, mode="a"):
    """Save data to a file"""
    with open(filename, mode) as file:
        file.write(data + "\n")

def feed_pet():
    """Feed your pet and adjust attributes."""
    global HUNGER, HAPPINESS, ENERGY
    food = random.choice(["Chicken", "Egg", "Biscuits", "Milk"])

    HUNGER = min(HUNGER + 10, 100)  

    print(f"\nYou fed {food} to your pet!")
    print(f"Current stats - Hunger: {HUNGER}, Happiness: {HAPPINESS}, Energy: {ENERGY}")
    return food

def play_with_pet():
    """Play with your pet and adjust attributes."""
    global HUNGER, HAPPINESS, ENERGY
    toy = random.choice(["Balls", "Frisbees", "Rope", "Squeaky Toys"])

    HAPPINESS = min(HAPPINESS + 15, 100)  
    ENERGY = max(ENERGY - 20, 0)  

    print(f"\nYou played with {toy} with your pet!")
    print(f"Current stats - Hunger: {HUNGER}, Happiness: {HAPPINESS}, Energy: {ENERGY}")
    return toy

def rest_pet():
    """Rest your pet and adjust attributes."""
    global HUNGER, HAPPINESS, ENERGY
    mat = random.choice(["Bed", "Cushion", "Blanket", "Carpet"])

    ENERGY = min(ENERGY + 15, 100)  
    HUNGER = max(HUNGER - 5, 0)  

    print(f"\nYour pet rested on {mat}!")
    print(f"Current stats - Hunger: {HUNGER}, Happiness: {HAPPINESS}, Energy: {ENERGY}")
    return mat

def load_from_file(filename):
    """Load data from a file"""
    if not os.path.exists(filename):
        return []
    with open(filename, "r") as file:
        return [line.strip() for line in file]

def display_inventory():
    """Display the inventory"""
    inventory = load_from_file(INVENTORY_FILE)  
    if inventory:
        print("\nInventory:")
        for item in inventory:
            print(item)
    else:
        print("\nYour inventory is empty.")

def update_leaderboard(pet_name, score):
    """Update the leaderboard with the current score"""
    save_to_file(LEADERBOARD_FILE, f"{pet_name}: {score}")

def countdown_timer(timeout):
    """Countdown timer that stops when the user inputs something."""
    for i in range(timeout, -1, -1):
        print(f"Time remaining: {i} seconds", end="\r")
        time.sleep(1)
        if input_received: 
            break
    if not input_received:
        print("\nTime's up! Game Over.")

def get_user_input_with_timer(prompt, timeout):
    """Get user input with a countdown timer"""
    global input_received
    input_received = False  

    timer_thread = threading.Thread(target=countdown_timer, args=(timeout,))
    timer_thread.start()

    user_input = input(f"{prompt} (You have {timeout} seconds to respond): ").strip()
    
    input_received = True  
    timer_thread.join()  

    return user_input

def check_pet_status():
    """Check the pet's health and winning condition"""
    global HUNGER, HAPPINESS, ENERGY, CONSECUTIVE_WINNING_TURNS

    if HUNGER == 0 or HAPPINESS == 0 or ENERGY == 0:
        print("\nYour pet got sick! Game Over.")
        return False

    if HUNGER > 80 and HAPPINESS > 80 and ENERGY > 80:
        CONSECUTIVE_WINNING_TURNS += 1
        if CONSECUTIVE_WINNING_TURNS >= 3:
            print("\nYour pet is super happy and energetic! You WIN!")
            return False
    else:
        CONSECUTIVE_WINNING_TURNS = 0  

    return True

def virtual_pet():
    print("Come create your virtual pet!")
    pet_name = input("Enter your pet's name: ").strip()

    if os.path.exists(INVENTORY_FILE):
        print("\nResuming your adventure...")
    else:
        print("\nStarting a new adventure...")
        open(INVENTORY_FILE, "w").close()

    score = 0

    while True:
        print("\nWhat would you like to do?")
        print("1. Feed your pet")
        print("2. Play with your pet")
        print("3. Rest")
        print("4. View your inventory") 
        print("5. Quit and save progress")
        choice = get_user_input_with_timer("Enter your choice (1/2/3/4/5):", 10)

        if choice == "1":
            food = feed_pet()
            save_to_file(INVENTORY_FILE, food) 
            score += 1
        elif choice == "2":
            toy = play_with_pet()
            save_to_file(INVENTORY_FILE, toy)  
            score += 1
        elif choice == "3":
            mat = rest_pet()
            save_to_file(INVENTORY_FILE, mat)  
            score += 1
        elif choice == "4":
            display_inventory()  
        elif choice == "5":
            print(f"\nThanks for playing with {pet_name}!")
            print(f"You collected {score} treasures.")
            update_leaderboard(pet_name, score)
            break
        elif choice == "":
            print("Game over! You lost your turn due to timeout!")
            break 
        else:
            print("Invalid choice. Please try again.")

        if not check_pet_status():
            break  

def display_leaderboard():
    """Display the leaderboard"""
    leaderboard = load_from_file(LEADERBOARD_FILE)
    if leaderboard:
        print("\nLeaderboard:")
        for entry in leaderboard:
            print(entry)
    else:
        print("\nNo entries in the leaderboard yet.")

def view_leaderboard():
    print("\n== Leaderboard ==")
    display_leaderboard()

def main():
    while True:
        print("\n== Virtual Pet Menu ==")
        print("1. Start/Resume Game")
        print("2. View Leaderboard")
        print("3. Exit")
        choice = input("Enter your choice (1/2/3): ").strip()

        if choice == "1":
            virtual_pet()
        elif choice == "2":
            view_leaderboard()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
