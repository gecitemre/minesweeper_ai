from numpy.core.defchararray import find
import pyautogui
import numpy
from PIL import Image
from os import listdir
from tensorflow import keras
from itertools import product


def get_code(image):
    return CLASS_NAMES[
        model.predict(
            numpy.expand_dims(keras.utils.img_to_array(image), axis=0)
        ).argmax()
    ]


def exclusive_gray_filter(image: Image):
    filtered_image = image.copy()
    pixels = filtered_image.load()
    for y in range(filtered_image.size[0]):
        for x in range(filtered_image.size[1]):
            if pixels[y, x][0] < 96 and pixels[y, x][1] < 96 and pixels[y, x][2] < 96:
                pixels[y, x] = (0, 0, 0)
    return filtered_image


def get_cell_coordinates(image):
    # left top right bottom
    pixels = numpy.asarray(exclusive_gray_filter(image))
    sum = pixels.sum(axis=2).sum(axis=0)
    lst0 = []
    index = 0
    while index < len(sum):
        if sum[index]:
            lst0.append([-1, -1])
            lst0[-1][0] = index
            while sum[index + 1]:
                index += 1
                lst0[-1][1] = index
                if index + 1 >= len(sum):
                    break
        index += 1

    sum = pixels.sum(axis=2).sum(axis=1)
    lst1 = []
    index = 0
    while index < len(sum):
        if sum[index]:
            lst1.append([-1, -1])
            lst1[-1][0] = index
            while sum[index + 1]:
                index += 1
                lst1[-1][1] = index
                if index + 1 >= len(sum):
                    break
        index += 1
    return [(p[1][0], p[0][0], p[1][1], p[0][1]) for p in product(lst1, lst0)]


def click_cell(cell_coordinate: numpy.ndarray, button="left") -> numpy.ndarray:
    coordinate = (
        numpy.flip(cell_coordinate) * numpy.array((CELL_WIDTH, CELL_HEIGTH))
        + TOP_LEFT
        + numpy.array((CELL_WIDTH // 2, CELL_HEIGTH // 2))
    )
    pyautogui.click(coordinate[0], coordinate[1], button=button)


def update_field(field: numpy.ndarray):
    screenshot = pyautogui.screenshot(
        region=(
            TOP_LEFT[0],
            TOP_LEFT[1],
            IMAGE_WIDTH,
            IMAGE_HEIGHT,
        )
    )
    for y in range(FIELD_HEIGHT):
        for x in range(FIELD_WIDTH):
            cell_id = FIELD_WIDTH * y + x
            if field[y, x] == UNKNOWN:
                cell = screenshot.crop(cell_coordinates[cell_id])
                field[y, x] = get_code(cell)
                # dir = max([int(dir[:-4]) for dir in listdir(str(field[y,x]))])
                # cell.save(f"{field[y,x]}/{dir+1}.png")


input("top left: ")
position = pyautogui.position()
left, top = position
print(f"\033[F\033[{len('top left: ')}G {position}")
input("bottom right: ")
position = pyautogui.position()
right, bottom = position
print(f"\033[F\033[{len('bottom right: ')}G {position}")
pixels = numpy.asarray(
    exclusive_gray_filter(
        pyautogui.screenshot(region=(left, top, right - left, bottom - top))
    )
)
whites = pixels.sum(axis=2).sum(axis=0).nonzero()[0]
right = whites[-1] + left
left += whites[0]
whites = pixels.sum(axis=2).sum(axis=1).nonzero()[0]
bottom = whites[-1] + top
top += whites[0]

FLAGGED = -4
SAFE = -3
MINE = -2
UNKNOWN = -1
IMAGE_WIDTH = right - left
IMAGE_HEIGHT = bottom - top
TOP_LEFT = numpy.array((left, top))
CLASS_NAMES = [int(dir) for dir in listdir("data")]


model = keras.models.Sequential(
    (
        keras.layers.Resizing(32, 32),
        keras.layers.Flatten(),
        keras.layers.Rescaling(1 / 255),
        keras.layers.Dense(len(CLASS_NAMES), activation="softmax"),
    )
)
model.compile(optimizer="adam", loss="categorical_crossentropy", metrics=["accuracy"])
model.load_weights("weights")


pixels = numpy.asarray(
    exclusive_gray_filter(
        pyautogui.screenshot(
            region=(
                TOP_LEFT[0],
                TOP_LEFT[1],
                IMAGE_WIDTH,
                IMAGE_HEIGHT,
            )
        )
    )
)

sum = pixels.sum(axis=2).sum(axis=0)
lst0 = []
index = 0
while index < len(sum):
    if sum[index]:
        lst0.append([-1, -1])
        lst0[-1][0] = index
        while sum[index + 1]:
            index += 1
            lst0[-1][1] = index
            if index + 1 >= len(sum):
                break
    index += 1

sum = pixels.sum(axis=2).sum(axis=1)
lst1 = []
index = 0
while index < len(sum):
    if sum[index]:
        lst1.append([-1, -1])
        lst1[-1][0] = index
        while sum[index + 1]:
            index += 1
            lst1[-1][1] = index
            if index + 1 >= len(sum):
                break
    index += 1

cell_coordinates = [(p[1][0], p[0][0], p[1][1], p[0][1]) for p in product(lst1, lst0)]
FIELD_WIDTH = len(lst0)
FIELD_HEIGHT = len(lst1)
CELL_WIDTH = IMAGE_WIDTH / FIELD_WIDTH
CELL_HEIGTH = IMAGE_HEIGHT / FIELD_HEIGHT