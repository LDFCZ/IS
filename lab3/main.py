import sys
import os

from PIL import Image, ImageDraw
from colorama import Fore, Style

DATA = dict()
name = sys.argv[0].split('/')[-1]

def main():
    try:
        DATA["action"] = sys.argv[1]

        DATA["image"] = sys.argv[2]

        if DATA["image"][0] != '/':
            DATA["image"] = os.getcwd() + '/' + DATA["image"]

        if not os.path.exists(DATA["image"]):
                raise FileExistsError
        
        if DATA["action"] == '-e':
            DATA["data"] = sys.argv[3]

            if DATA["data"][0] != '/':
                DATA["data"] = os.getcwd() + '/' + DATA["data"]

            if not os.path.exists(DATA["data"]):
                raise FileExistsError
            
            if isset(sys.argv, 4):
                value = int(sys.argv[4])

                if value >= 1 and value <= 4:
                    DATA["balance"] = value

                else:
                    raise ValueError

    except IndexError:
        using("Encrypt: {} -e [path_to_image*] [path_to_data*] [balance]".format(name))
        using("Decrypt: {} -d [path_to_image*]".format(name))
        using("Program information: {} -i".format(name), True)

    except FileExistsError:
        error("Image or data file not found.", True)

    except ValueError:
        using("Balance should be from 1 to 4.", True)

    if DATA["action"] == '-e':

        if not isset(DATA, "balance"):

            try:
                DATA["balance"] = int(input(Style.BRIGHT + Fore.RED + "     Balance (1 to 4) > "))

                if DATA["balance"] < 1 or DATA["balance"] > 4:
                    raise ValueError

            except ValueError:
                error("Set to 2.")
                DATA["balance"] = 2

        file = open(DATA["data"], 'r')
        text = file.read()
        file.close()

        encrypt(DATA["image"], text.strip(), DATA["balance"])

    elif DATA["action"] == '-d':

        key = input(Style.BRIGHT + Fore.RED + "     Key: ")

        try:
            decrypt(DATA["image"], key)

        except IndexError:
            error("Invalid key.")

        except ValueError:
            error("Invalid key.")

    print('')


def find_max_index(array):
    max_num = array[0]
    index = 0

    for i, val in enumerate(array):
        if val > max_num:
            max_num = val
            index = i

    return index


def balance_channel(colors, pix):
    max_color = find_max_index(colors)
    colors[max_color] = int(last_replace(bin(colors[max_color]), pix), 2)

    while True:
        max_sec = find_max_index(colors)
        if max_sec != max_color:
            colors[max_sec] = colors[max_color] - 1
        else:
            break

    return colors


def encrypt(path_to_image, text, balance):
    img = dict()
    size = dict()
    coord = dict()

    img["image"] = Image.open(path_to_image)
    img["draw"] = ImageDraw.Draw(img["image"])
    img["pix"] = img["image"].load()

    size["width"] = img["image"].size[0]
    size["height"] = img["image"].size[1]

    binary_text = text_to_binary(text)
    list_two = split_count(''.join(binary_text), balance)

    coord["x"] = 0
    coord["y"] = 0
    count = 0

    for i in list_two:
        red, green, blue = img["pix"][coord["x"], coord["y"]]

        (red, green, blue) = balance_channel([red, green, blue], i)

        img["draw"].point((coord["x"], coord["y"]), (red, green, blue))

        if coord["x"] < (size["width"] - 1):
            coord["x"] += 1

        elif coord["y"] < (size["height"] - 1):
            coord["y"] += 1
            coord["x"] = 0

        else:
            error("Message too long for this image.", True)

        count += 1

    img["image"].save("out.png", "PNG")

    file = open("key.dat", "w")
    file.write(str(balance) + '$' + str(count))
    file.close()

    success(str(count) + " pixels takes")
    success("Image saved in out.png")
    success("Key saved in key.dat")


def decrypt(path_to_image, key):
    balance = int(key.split('$')[0])
    count = int(key.split('$')[1])

    img = dict()
    coord = dict()

    img["image"] = Image.open(path_to_image)
    img["width"] = img["image"].size[0]
    img["height"] = img["image"].size[1]
    img["pix"] = img["image"].load()

    coord["x"] = 0
    coord["y"] = 0
    code = ''

    i = 0
    while i < count:
        pixels = img["pix"][coord["x"], coord["y"]]

        pixel = str(bin(max(pixels)))

        if balance == 4:
            code += pixel[-4] + pixel[-3] + pixel[-2] + pixel[-1]

        elif balance == 3:
            code += pixel[-3] + pixel[-2] + pixel[-1]

        elif balance == 2:
            code += pixel[-2] + pixel[-1]

        else:
            code += pixel[-1]

        if coord["x"] < (img["width"] - 1):
            coord["x"] += 1
        else:
            coord["y"] += 1
            coord["x"] = 0

        i += 1

    outed = binary_to_text(split_count(code, 8))

    file = open("out.txt", "w")
    file.write(''.join(outed))
    file.close()
    
    success("Data saved in out.txt")



def split_count(text, count):
    result = list()
    txt = ''
    var = 0

    for i in text:
        if var == count:
            result.append(txt)
            txt = ''
            var = 0

        txt += i
        var += 1

    result.append(txt)

    return result


def last_replace(main_string, last_symbols):
    return str(main_string)[:-len(last_symbols)] + last_symbols

def text_to_binary(event):
    return ['0' * (8 - len(format(ord(elem), 'b'))) + format(ord(elem), 'b') for elem in event]


def binary_to_text(event):
    return [chr(int(str(elem), 2)) for elem in event]


def isset(array, key):
    try:
        if type(array) is list:
            array[key]

        elif type(array) is dict:
            return key in array.keys()

        return True
    except:
        return False


def error(text, quit=False):
    print(Style.BRIGHT + Fore.YELLOW + "     " + text + Style.RESET_ALL)

    if quit:
        sys.exit()


def using(text, quit=False):
    print(Style.BRIGHT + Fore.WHITE + "     " + text + Style.RESET_ALL)

    if quit:
        sys.exit()


def success(text):
    print(Style.BRIGHT + Fore.GREEN + "     " + text + Style.RESET_ALL)


if __name__ == "__main__":
    main()