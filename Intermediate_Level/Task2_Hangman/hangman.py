import random

HANGMAN_PICS = [
    """
       -----
       |   |
           |
           |
           |
           |
    =========
    """,
    """
       -----
       |   |
       O   |
           |
           |
           |
    =========
    """,
    """
       -----
       |   |
       O   |
       |   |
           |
           |
    =========
    """,
    """
       -----
       |   |
       O   |
      /|   |
           |
           |
    =========
    """,
    """
       -----
       |   |
       O   |
      /|\  |
           |
           |
    =========
    """,
    """
       -----
       |   |
       O   |
      /|\  |
      /    |
           |
    =========
    """,
    """
       -----
       |   |
       O   |
      /|\  |
      / \  |
           |
    =========
    """
]

WORDS_AND_HINTS = {
    "python": "A popular programming language, and also a large snake.",
    "developer": "Someone who writes code.",
    "hangman": "The name of this game.",
    "keyboard": "You type on this.",
    "monitor": "The screen you look at.",
    "variable": "A container for storing data values in programming.",
    "function": "A block of code which only runs when it is called.",
    "algorithm": "A step-by-step procedure for solving a problem.",
    "database": "An organized collection of data.",
    "internet": "A global computer network providing a variety of information and communication facilities."
}

def play_hangman():
    word = random.choice(list(WORDS_AND_HINTS.keys()))
    hint = WORDS_AND_HINTS[word]
    
    guessed_letters = set()
    incorrect_guesses = 0
    max_attempts = len(HANGMAN_PICS) - 1
    
    print("Welcome to Hangman!")
    print(f"Hint: {hint}")
    
    while incorrect_guesses < max_attempts:
        print(HANGMAN_PICS[incorrect_guesses])
        
        display_word = "".join([char if char in guessed_letters else "_" for char in word])
        print(f"Word: {' '.join(display_word)}")
        print(f"Guessed letters: {', '.join(sorted(guessed_letters))}")
        
        if "_" not in display_word:
            print("\nCongratulations! You guessed the word correctly.")
            return
            
        guess = input("Guess a letter: ").lower()
        
        if len(guess) != 1 or not guess.isalpha():
            print("Please enter a single valid letter.")
            continue
            
        if guess in guessed_letters:
            print("You already guessed that letter.")
            continue
            
        guessed_letters.add(guess)
        
        if guess in word:
            print("Good guess!")
        else:
            print("Incorrect guess.")
            incorrect_guesses += 1
            
    if incorrect_guesses == max_attempts:
        print(HANGMAN_PICS[incorrect_guesses])
        print(f"\nGame Over! The word was: {word}")

if __name__ == "__main__":
    while True:
        play_hangman()
        replay = input("\nDo you want to play again? (y/n): ").lower()
        if replay != 'y':
            print("Thanks for playing!")
            break
