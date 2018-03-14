# Modified from https://github.com/nilesr/braille-art
from PIL import Image
import os, random, sys

def img_average(x1, y1, x2, y2, img):
    average = lambda x: sum(x)/len(x) if len(x) > 0 else 0
    ret = []
    for x in range(x1, x2):
        for y in range(y1, y2):
            ret.append(average(img.getpixel((x, y))[:3]))
    return average(ret)

def convert_index(x):
    if x < 3: return x
    if x == 3: return 6
    if x == 4: return 3
    if x == 5: return 4
    if x == 6: return 5
    if x == 7: return 7

def draw(img, post_info):
    start = 0x2800
    char_width = 10
    char_height = char_width * 2
    dither, sensitivity = 5, 0.6
    char_width_divided, char_height_divided = round(char_width / 2), round(char_height / 4)
    match = lambda a, b: a < b if "--invert" in sys.argv else a > b
    print('username: ' + post_info['username'])
    print('\033[4m' + post_info['site_url'] + '\033[0m \n')
    for y in range(0, img.height - char_height - 1, char_height):
        for x in range(0, img.width - char_width - 1, char_width):
            byte, index = 0x0, 0
            for xn in range(2):
                for yn in range(4):
                    avg = img_average(x + (char_height_divided * xn), y + (char_width_divided * yn), x + (char_height_divided * (xn + 1)), y + (char_width_divided * (yn + 1)), img)
                    if match(avg + random.randint(-dither, dither), sensitivity * 0xFF):
                        byte += 2**convert_index(index)
                    index += 1
            print(chr(start + byte), end = "")
        print()
    print('Likes: ' + post_info['likes'])
    print(post_info['caption'])
    print('-------------------\n')

def resize_image(img):
    basewidth = 550
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth, hsize), Image.ANTIALIAS)
    return img

def display_to_terminal(posts_info):
    file_list = os.listdir('./images/')
    for filename in file_list:
        img = Image.open('./images/' + filename)
        draw(resize_image(img), posts_info[filename])

if __name__ == '__main__':
    display_to_terminal(posts_info)