import pygsheets
import pandas as pd
import numpy as np

def get_multiples(array):
    multiples = (np.array(array).reshape(-1)) // 256
    return multiples

def edit_gsheet(multiples_array):
    #authorization
    gc = pygsheets.authorize(service_file='vandyhack_cred.json')


    df = pd.DataFrame(multiples_array, columns=['multiples'])

    #open the google spreadsheet
    sh = gc.open('VandyHacks')

    #select the first sheet
    wks = sh[0]

    #update the first sheet
    wks.set_dataframe(df, (1, 1))


    # first_element = 0
    # for each in wks.__iter__():
    #     i = 0
    #     # print(each)
    #     while each[i]:
    #         i += 1
    #     first_element = i
    #     break


def get_column():
    gc = pygsheets.authorize(service_file='vandyhack_cred.json')
    sh = gc.open('VandyHacks')
    wks = sh[0]

    multiples = []

    first_element = True
    for each in wks.__iter__():
        if (first_element):
            first_element = False
            continue

    # i
        multiples.append(int(each[0]))

    return multiples


if __name__ == '__main__':
    # get_column()
    edit_gsheet([2,2,4,3])