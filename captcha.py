import cv2
import os
import os.path


def horizontal_lines(img):
    rows, cols = img.shape
    indices = []
    for i in range(rows):
        count = 0
        for j in range(cols):
            if img[i, j] < 30:
                count += 1
        if abs(count - cols) < cols // 10:
            indices.append(i)
    return indices


def vertical_lines(img):
    rows, cols = img.shape
    indices = []
    for i in range(cols):
        count = 0
        for j in range(rows):
            if img[j, i] < 30:
                count += 1
        if abs(count - rows) < rows // 10:
            indices.append(i)
    return indices


def erase_horizontal_line(img, indices):
    new_img = img
    rows, cols = img.shape
    passes = 5
    for p in range(passes):
        for row in indices:
            for col in range(cols):
                if row == 0:
                    new_img.itemset((row, col), (new_img.item(
                        row, col) + new_img.item(row + 1, col)) // 2)
                elif row == rows - 1:
                    new_img.itemset((row, col), (new_img.item(
                        row, col) + new_img.item(row - 1, col)) // 2)
                else:
                    new_img.itemset((row, col), (new_img.item(
                        row, col) + new_img.item(row - 1, col) + new_img.item(row + 1, col)) // 3)
    return new_img


def erase_vertical_line(img, indices):
    new_img = img
    rows, cols = img.shape
    passes = 7
    for p in range(passes):
        for col in indices:
            for row in range(rows):
                if col == 0:
                    new_img.itemset((row, col), (new_img.item(
                        row, col) + new_img.item(row, col + 1)) // 2)
                elif col == cols - 1:
                    new_img.itemset((row, col), (new_img.item(
                        row, col) + new_img.item(row, col - 1)) // 2)
                else:
                    new_img.itemset((row, col), (new_img.item(
                        row, col) + new_img.item(row, col + 1) + new_img.item(row, col - 1)) // 3)
    return new_img


def remove_lines(input_file_name):
    img = cv2.imread(input_file_name, cv2.IMREAD_GRAYSCALE)
    horizontal_indices = horizontal_lines(img)
    vertical_indices = vertical_lines(img)
    final_img = erase_horizontal_line(img, horizontal_indices)
    final_img = erase_vertical_line(final_img, vertical_indices)
    cv2.imwrite('mod_' + input_file_name, final_img)
    return 'mod_' + input_file_name


def read_captcha_image(input_file_name):
    modified_file_name = remove_lines(input_file_name)
    os.system('tesseract ' + modified_file_name + ' captcha_file &>/dev/null')
    os.remove(modified_file_name)
    captcha_file = open('captcha_file.txt', 'r')
    captcha = captcha_file.read(6)
    captcha_file.close()
    os.remove('captcha_file.txt')
    return captcha
