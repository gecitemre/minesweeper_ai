import numpy
import pyautogui
import msms
import numpy
from itertools import combinations

FLAGGED = -4
SAFE = -3
MINE = -2
UNKNOWN = -1
DICTIONARY = {-4: "!", -1: "?", 0: "0", 1: "1", 2: "2", 3: "3", 4: "4", 5: "5"}


def id2coordinate(cell_id):
    return cell_id // msms.FIELD_WIDTH, cell_id % msms.FIELD_WIDTH


def print_field(field):
    for y in range(msms.FIELD_HEIGHT):
        for x in range(msms.FIELD_WIDTH):
            print(DICTIONARY[field[y, x]], end=" ")
        print()
    print()


def find_unknown_cells(field, coordinate):
    cell_y, cell_x = coordinate
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


def count_mines(field, coordinate):
    cell_y, cell_x = coordinate
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


def find_solutions(field, cell_id):
    solutions = []
    for cell_id in range(cell_id, msms.FIELD_WIDTH * msms.FIELD_HEIGHT):
        coordinate = id2coordinate(cell_id)
        if field[coordinate] > 0:
            if field[coordinate] - count_mines(field, coordinate) >= 0:
                unknown_cells = find_unknown_cells(field, coordinate)
                combs = combinations(
                    unknown_cells, field[coordinate] - count_mines(field, coordinate)
                )
                new_field = field.copy()
                if combs:
                    for combination in combs:
                        for index in combination:
                            new_field[index] = MINE
                        for index in set(unknown_cells) - set(combination):
                            new_field[index] = SAFE
                        solutions += find_solutions(new_field, cell_id + 1)
                else:
                    for index in unknown_cells:
                        new_field[index] = SAFE
                    solutions += find_solutions(new_field, cell_id + 1)
            break
    else:
        solutions = [field]
    return solutions


field = UNKNOWN * numpy.ones((msms.FIELD_HEIGHT, msms.FIELD_WIDTH), dtype=numpy.int8)

while True:
    solutions = numpy.array(find_solutions(field, 0))
    if not solutions.size:
        quit()
    print(solutions)
    safes = numpy.vstack(
        ((solutions == SAFE).sum(axis=0) == len(solutions)).nonzero()
    ).transpose()
    for coordinate in safes:
        msms.click_cell(coordinate)
    if not safes.size:
        coordinate = id2coordinate((solutions == SAFE).sum(axis=0).argmax())
        if field[coordinate] != UNKNOWN:
            unknowns = (field == UNKNOWN).nonzero()
            coordinate = unknowns[0][0], unknowns[1][0]
        msms.click_cell(coordinate)
    mines = ((solutions == MINE).sum(axis=0) == len(solutions)).nonzero()
    field[mines] = FLAGGED
    for coordinate in numpy.vstack(mines).transpose():
        msms.click_cell(coordinate, button="right")
    msms.update_field(field)
    #print_field(field)
    if (field == UNKNOWN).all():
        quit()
