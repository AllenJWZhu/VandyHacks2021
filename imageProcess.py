from PIL import Image
import ellipticCurve
import googleCloud
import imgToDat
import numpy as np

# TODO create a function to reformat the size of picture


WIDTH = 146
HEIGHT = 96


def display_image(imdata):
    newim = Image.new("RGB", (219, 192))

    for i in range(len(imdata)):
        imdata[i] = (imdata[i][0] % 256, imdata[i][1] % 256, imdata[i][2] % 256)

    newim.putdata(imdata)
    return newim


def read_image(jpg):
    im = Image.open(jpg)
    r = []
    g = []
    b = []

    for row in im.getdata():
        r.append(int(row[0]))
        g.append(int(row[1]))
        b.append(int(row[2]))

    multiples = googleCloud.get_column()

    newimdata = []
    for i in range(len(r)):
        newimdata.append((r[i] + 256 * multiples[i * 3], g[i] + 256 * multiples[i * 3 + 1],
                          b[i] + 256 * multiples[i * 3 + 2]))

    return newimdata


def encrypt_picture(file_name):
    encrypted_array = ellipticCurve.encrypt_to_disk(file_name)

    multiples_array = googleCloud.get_multiples(encrypted_array)
    googleCloud.edit_gsheet(multiples_array)

    display_image(encrypted_array).save("../img/final.png")


def decrypt_picture(input, save_file_name):
    original_encrypted = read_image(input)
    decrypted = ellipticCurve.decrypt_to_pic(original_encrypted)
    imgToDat.restoreImg(decrypted, save_file_name)


def golden_disc_data(disc):
    golden = Image.open(disc)

    r_golden = []
    g_golden = []
    b_golden = []
    for row in golden.getdata():
        r_golden.append(int(row[0]))
        g_golden.append(int(row[1]))
        b_golden.append(int(row[2]))
    disc_data = []
    for i in range(len(r_golden)):
        disc_data.append(r_golden[i])
        disc_data.append(g_golden[i])
        disc_data.append(b_golden[i])

    f1 = open("disc_data.txt", 'w')
    f1.write(str(disc_data))
    f1.close()


def mosaic_to_disc(file_name, imdata):
    multiples_array = googleCloud.get_multiples(imdata)
    googleCloud.edit_gsheet(multiples_array)

    f2 = open(file_name, 'r')
    raw_data = f2.read()
    raw_data = raw_data[1:len(raw_data) - 1].split(', ')
    disc_data = []
    for i in range(len(raw_data) // 3):
        disc_data.append((int(raw_data[i * 3]), int(raw_data[i * 3 + 1]),
                          int(raw_data[i * 3 + 2])))

    for i in range(len(imdata)):
        imdata[i] = (imdata[i][0] % 256, imdata[i][1] % 256, imdata[i][2] % 256)

    i = 0
    position = 759272
    while i < len(imdata):
        if i % 219 == 0:
            position += 1200 - 219
        disc_data[position + i] = imdata[i]
        i += 1

    newim = Image.new("RGB", (1200, 1200))
    newim.putdata(disc_data)

    newim.save("static/uploads/the_golden_disc.png")


def encrypt_to_disc(file_name, disc_data_file="disc_data.txt"):
    """
    :param file_name: image path and name to encrypt
    :param disc_data_file: the data file of the disc picture
    :return: save the final picture to the img folder with a name of "the_golden_disc.png"
    """
    encrypted_array = ellipticCurve.encrypt_to_disk(file_name)
    mosaic_to_disc(disc_data_file, encrypted_array)


def decrypt_to_picture(disc_file_name, save_file_name):
    """
    :param disc_file_name: the image path and name to decrypt
    :param save_file_name: the path and name to save the picture
    :return: the original picture in img folder
    """
    disc = Image.open(disc_file_name)
    position = 759272
    imdata = []
    i = 0

    array = list(disc.getdata())

    while i < 219 * 192:
        if i % 219 == 0:
            position += 1200 - 219
        imdata.append(array[position + i])
        i += 1

    mosaic = Image.new("RGB", (219, 192))
    mosaic.putdata(imdata)
    mosaic.save("static/uploads/temp.png")

    decrypt_picture("static/uploads/temp.png", save_file_name)


# if __name__ == '__main__':
    # encrypted_array = ellipticCurve.encrypt_to_disk()
    # print("checkpoint 1")
    # encrypt_to_disc("disc_data.txt", encrypted_array)
    # encrypt_to_disc("../img/space.jpg")
    # decrypt_to_picture("../img/the_golden_disc.png", "../img/original_space.png")
