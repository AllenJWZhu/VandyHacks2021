from PIL import Image
import ellipticCurve
import imgToDat

# TODO create a function to reformat the size of picture


WIDTH = 146
HEIGHT = 96


def read_disc_data(file_name):
    """
    read the txt file of the intact disk for future use
    """
    f2 = open(file_name, 'r')
    raw_data = f2.read()
    raw_data = raw_data[1:len(raw_data) - 1].split(', ')
    disc_data = []
    for i in range(len(raw_data) // 3):
        disc_data.append((int(raw_data[i * 3]), int(raw_data[i * 3 + 1]),
                          int(raw_data[i * 3 + 2])))
    f2.close()
    return disc_data


def golden_disc_data(disc_pic):
    """
    Convert the intact disk image into data pts and save them into a txt file
    """
    golden = Image.open(disc_pic)
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


class PipeLine:
    """
    The class for encrypting and decrypting. The intact disk data is save as a class member
    """

    def __init__(self, disc_file_name="disc_data.txt"):
        self.disc_data = read_disc_data(disc_file_name)

    def mosaic_to_disc(self, imdata, save_file):
        """
        Convert the encrypted data into mosaic and embed into the disc
        """
        new_disc = self.disc_data
        # size_mod = (size[0]%256, size[1]%256, )
        imdata_main = []
        imdata_support = []
        imdata_support2 = []

        # divide the encrypted data into three parts
        for i in range(len(imdata)):
            imdata_main.append((imdata[i][0] % 256, imdata[i][1] % 256, imdata[i][2] % 256))
            imdata_support.append(
                (255 - (imdata[i][0] // 256) // 128, 255 - (imdata[i][1] // 256) // 128,
                 255 - (imdata[i][2] // 256) // 128))
            imdata_support2.append(((imdata[i][0] // 256) % 128, (imdata[i][1] // 256) % 128,
                                    (imdata[i][2] // 256) % 128))

        # the center encrypted picture
        i = 0
        position = 759272
        while i < len(imdata):
            if i % 219 == 0:
                position += 1200 - 219
            new_disc[position + i] = imdata_main[i]
            i += 1

        # the rhs encrypted picture
        i = 0
        position = 250
        while i < len(imdata):
            if i % 219 == 0:
                position += 1200 - 219
            new_disc[position + i] = imdata_support[i]
            i += 1

        # the lhs encrypted picture
        i = 0
        position = 1200
        while i < len(imdata):
            if i % 219 == 0:
                position += 1200 - 219
            new_disc[position + i] = imdata_support2[i]
            i += 1

        # save the encrypted disc
        newim = Image.new("RGB", (1200, 1200))
        newim.putdata(new_disc)
        newim.save(save_file, format='png')

    def encrypt_to_disc(self, file_name, save_file_name="static/uploads/converted_disc.png"):
        """
        :param save_file_name: place to save the picture
        :param file_name: image path and name to encrypt
        :return: save the final picture to the img folder with a name of "the_golden_disc.png"
        """
        encrypted_array = ellipticCurve.encrypt_to_disk(file_name)
        PipeLine.mosaic_to_disc(self, encrypted_array, save_file_name)

    def decrypt_to_picture(self, disc_file_name, save_file_name):
        """
        :param disc_file_name: the image path and name to decrypt
        :param save_file_name: the path and name to save the picture
        :return: the original picture in img folder
        """
        disc = Image.open(disc_file_name)
        array = list(disc.getdata())
        imdata = []
        imdata_support = []
        imdata_support2 = []

        # retrieve the encrypted messages
        i = 0
        position_su = 250
        position_su2 = 1200
        position = 759272
        while i < 219 * 192:
            if i % 219 == 0:
                position += 981
                position_su += 981
                position_su2 += 981
            imdata.append(array[position + i])
            imdata_support.append(array[position_su + i])
            imdata_support2.append(array[position_su2 + i])
            i += 1

        # conduct decrypting
        PipeLine.decrypt_picture(self, imdata, imdata_support, imdata_support2, save_file_name)

    def decrypt_picture(self, input_main, input_su, input_su2, save_file_name):
        """
        Resume the data embedded in the disc, decrypt data using ECC, and generate the picture
        """
        original_encrypted = read_image(input_main, input_su, input_su2)
        decrypted = ellipticCurve.decrypt_to_pic(original_encrypted)
        imgToDat.restoreImg(decrypted, save_file_name)


def read_image(input_main, input_su, input_su2):
    """Resume the data embedded in the disc to data that can be deciphered by ECC"""
    newimdata = []
    for (tuple_m, tuple_1, tuple_2) in zip(input_main, input_su, input_su2):
        newimdata.append((resume_f(tuple_m[0], tuple_1[0], tuple_2[0]), resume_f(tuple_m[1], tuple_1[1], tuple_2[1]),
                          resume_f(tuple_m[2], tuple_1[2], tuple_2[2])))

    return newimdata


def resume_f(main, support, support2):
    """Resume a single data point"""
    return ((255 - support) * 128 + support2) * 256 + main


# def display_image(imdata):
#     newim = Image.new("RGB", (219, 192))
#
#     for i in range(len(imdata)):
#         imdata[i] = (imdata[i][0] % 256, imdata[i][1] % 256, imdata[i][2] % 256)
#
#     newim.putdata(imdata)
#     return newim


# def encrypt_picture(file_name):
#     encrypted_array = ellipticCurve.encrypt_to_disk(file_name)
#
#     multiples_array = googleCloud.get_multiples(encrypted_array)
#     googleCloud.edit_gsheet(multiples_array)
#
#     display_image(encrypted_array).save("../img/final.png")


# if __name__ == '__main__':
# encrypted_array = ellipticCurve.encrypt_to_disk()
# print("checkpoint 1")
# encrypt_to_disc("disc_data.txt", encrypted_array)
# temp = PipeLine()
# temp.encrypt_to_disc("./img/space.jpg")
# temp.decrypt_to_picture("./static/uploads/the_golden_disc2.png", "./img/original_space2.png")
