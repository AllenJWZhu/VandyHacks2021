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
    # file_name = input("Enter the file path and name: ")
    encrypted_array = ellipticCurve.encrypt_to_disk(file_name)

    multiples_array = googleCloud.get_multiples(encrypted_array)
    googleCloud.edit_gsheet(multiples_array)

    display_image(encrypted_array).save("../img/final.png")

    # print("final.png complete")


def decrypt_picture(file_name):
    original_encrypted = read_image("../img/final.png")
    decrypted = ellipticCurve.decrypt_to_pic(original_encrypted)
    imgToDat.restoreImg(decrypted, file_name)


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


# def decrypt_to_picture()


# 660 -880
def mosaic_to_disc(file_name, imdata):
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

    newim.save("../img/the_golden_disc.png")


def encrypt_to_disc(file_name, disc_data_file="disc_data.txt"):
    encrypted_array = ellipticCurve.encrypt_to_disk(file_name)
    mosaic_to_disc(disc_data_file, encrypted_array)


if __name__ == '__main__':
    # encrypted_array = ellipticCurve.encrypt_to_disk()
    # print("checkpoint 1")
    # encrypt_to_disc("disc_data.txt", encrypted_array)
    encrypt_to_disc("../img/space.jpg")
