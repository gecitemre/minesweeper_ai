import numpy
import pyautogui
import msms
import numpy
from itertools import combinations
from time import sleep


FLAGGED = -4
SAFE = -3
MINE = -2
UNKNOWN = -1
DICTIONARY = {-4: "⚑", -2: "M", -1: "?", 0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5"}


def print_field(field):
    for y in range(msms.FIELD_HEIGHT):
        for x in range(msms.FIELD_WIDTH):
            print(DICTIONARY[field[y, x]], end=" ")
        print()
    print()


def find_unknown_cells(field, cell_y, cell_x):
    unknown_cells = []
    for y in range(cell_y - 1, cell_y + 2):
        if y < 0 or y >= msms.FIELD_HEIGHT:
            continue

        for x in range(cell_x - 1, cell_x + 2):
            if x < 0 or x >= msms.FIELD_WIDTH:
                continue

            if field[y, x] == UNKNOWN:
                unknown_cells.append((y, x))
    return unknown_cells


def count_mines(field, cell_y, cell_x):
    num_mines = 0
    for y in range(cell_y - 1, cell_y + 2):
        if y < 0 or y >= msms.FIELD_HEIGHT:
            continue

        for x in range(cell_x - 1, cell_x + 2):
            if x < 0 or x >= msms.FIELD_WIDTH:
                continue

            if field[y, x] == MINE or field[y, x] == FLAGGED:
                num_mines += 1
    return num_mines


def is_valid(field):
    for y in range(msms.FIELD_HEIGHT):
        for x in range(msms.FIELD_WIDTH):
            if field[y, x] > 0 and field[y, x] < count_mines(y, x):
                return False
    return True


def find_solutions(field, start_id):
    solutions = []
    for cell_id in range(start_id, msms.FIELD_WIDTH * msms.FIELD_HEIGHT):
        x = cell_id % msms.FIELD_WIDTH
        y = cell_id // msms.FIELD_WIDTH
        if field[y, x] > 0:
            if field[y, x] - count_mines(field, y, x) >= 0:
                unknown_cells = find_unknown_cells(field, y, x)
                combs = combinations(
                    unknown_cells, field[y, x] - count_mines(field, y, x)
                )
                if combs:
                    for combination in combs:
                        new_field = field.copy()
                        for index in combination:
                            new_field[index] = MINE
                        for index in set(unknown_cells) - set(combination):
                            new_field[index] = SAFE
                        solutions += find_solutions(new_field, cell_id + 1)
                else:
                    new_field = field.copy()
                    for index in unknown_cells:
                        new_field[index] = SAFE
                    solutions += find_solutions(new_field, cell_id + 1)
            return solutions
    return [field]


field = UNKNOWN * numpy.ones((msms.FIELD_HEIGHT, msms.FIELD_WIDTH), dtype=numpy.int8)
msms.update_field(field)
while True:
    solutions = numpy.array(find_solutions(field, 0))
    safes = numpy.rot90(numpy.vstack(((solutions == SAFE).sum(axis=0) == len(solutions)).nonzero()),axes=(1,0))
    for cell in safes:
        msms.click_cell(cell)
    if not safes.size:
        cell_id = (solutions == SAFE).sum(axis=0).argmax()
        msms.click_cell(numpy.array((cell_id % msms.FIELD_WIDTH, cell_id // msms.FIELD_WIDTH)))
    mines = ((solutions == MINE).sum(axis=0) == len(solutions)).nonzero()
    field[mines] = FLAGGED
    if mines:
        for y, x in zip(mines[0], mines[1]):
            msms.click_cell(numpy.array((x, y)), button="right")
    sleep(1)
    msms.update_field(field)
    print_field(field)
    if (field != UNKNOWN).all():
        pyautogui.screenshot().show()
        quit()