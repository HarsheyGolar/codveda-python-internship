import random

def play_game():
    # Generates the Target Number and configure the maximum attempts.
    number = random.randint(1, 100)
    no_of_attempts = 5

    # Display the game title and instructions.
    print("=" * 50)
    print("NUMBER GUESSING GAME".center(50))
    print("=" * 50)

    print("-" * 60)
    print("I am thinking... of a number between 1 and 100.")
    print(f"You have {no_of_attempts} attempts to guess it.")
    print("-" * 60)

    # Continue the game until the player guesses correctly or runs out of attempts.
    while no_of_attempts > 0:
        try:
            # Read and validate the player's guess.
            guess = int(input(f"\n[{no_of_attempts} attempts left] Enter your guess: "))
        except ValueError:
            print("Please Enter the Valid Number.")
            continue

        # Compare the guess with the target number and provide feedback.
        if guess == number:
            print(f"Congratulations! You Won By Guessing The Correct Number {number} in {no_of_attempts} attempts.")
            break
        elif guess < number:
            print("Too Low! Try a higher number.")
        else:
            print("Too High! Try a lower number.")

        # Decrease the remaining attempts after a vaild guess.
        no_of_attempts -= 1

    # Display the target number when all attempts have been exhausted.
    if no_of_attempts == 0:
        print(f"Game Over! You have run out of attempts. The number was {number}")

    #  function call...
if __name__=="__main__": play_game()
    
