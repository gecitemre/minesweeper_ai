# minesweeper_ai
minesweeper bot - python

[Youtube Demo](https://www.youtube.com/watch?v=qarubOAwA5g)

A bot that plays the minesweeper game with Python. It first detects the game board and creates a matrix representation of the game state using image processing techniques and computer vision. A four-layered sequential neural network in Keras is trained for recognizing the numbers on the board. A special search algorithm searches the possible game states pruning the impossible states, decides the optimal choices, and triggers mouse clicks using a Python library. The bot has a %99+ success rate in completing the game without hitting any mines.

This is not a complete project.
The AI can recognize digits up to 5 currently. If a "6", "7" or "8" shows up, the program would find no solutions and halt itself, raising an error.
The AI is trained on 9x9 and 30x16 fields. In other fields, since the image sizes will change, the AI might have some mistakes. Even then, the AI will have a +%90 accuracy rate.
The training data is in the [data](data) folder. You can change the training data and train a new classifier network using classifier.py.

How to use:
1. Download [Microsoft Minesweeper](https://www.microsoft.com/tr-tr/p/microsoft-minesweeper/9wzdncrfhwcn) from Microsoft Store, and open.
2. Choose a field.
3. Run "bot.py" (No other windows must not be on top of the minefield).
4. The program needs the coordinates of the field in order to run. You should specify a top_left coordinate and a bottom_right coordinate. The field should lay inside these two corners. The area between these two corners can be greater than the field, but not smaller. To specify these coordinates, drag your mouse to the top left of the field and send an enter using standard input. After doing the same for the bottom right, the program will start running. Enjoy!

WARNING: If the program gets out of control, press `ctrl`+`alt`+`delete`. The program will halt itself.
