# minesweeper_ai
minesweeper bot - python

This is not a complete project.
The AI can recognize digits up to 5 currently. If a "6", "7" or "8" would show up, the program would find no solutions and halt itself, raising an error.
The AI is trained on 9x9 and 30x16 fields. In other fields, since the image sizes will change, the AI might have some mistakes. Even then, the AI will have +%90 accuracy rate.
The train data is in data folder. You can change the train data and create a new classifier network using classifier.py.

How to use:
1 - Download Microsoft Minesweeper from Microsoft Store, and open.
2 - Choose a field.
3 - Run "bot.py" (No other windows must not be on top of the minefield).
4 - The program needs the coordinates of the field in order to run. To specify the coordinates, you should specify a top_left coordinate and a bottom_right coordinate. The field should lay inside these to corners. The area between these two corners can be greater than the field, but not smaller. To specify these coordinates, drag your mouse to the top left of the field and send an enter using standart input. After doing the same for the bottom right, the program will start running, enjoy!
