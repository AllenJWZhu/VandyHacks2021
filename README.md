# VandyHacks2021
This is the project for VandyHacks VIII. This project is about the transformation of images using the ECC encryption.

# Inspiration
Inspired by the historic journey of the Voyager spacecraft mission in the year 1977, we are launching a Golden Record with a similar, yet unique "time capsule" into space. We have always been wondering about the existence of advanced space-faring civilizations dispersed throughout interstellar space and had a beautiful fantasy of possibly communicating with them... Do you want to be a designer of the next Voyager Golden Record and send a piece of information that would be unique to you to interstellar space? If so, welcome to the journey!

# What it does
We accept a user input image. The image is then transformed using our hardest-ever yet beautiful algorithm (ECC algorithm) and encoded into a Golden Record which is the only unique disk in the world. Even the same picture would be rendered into two different disks if a different person conducts the encryption, and each picture would have a unique private key associated with it. Of course, with our beautiful algorithm, we are able to translate the message engraving on the disk and transform it back into the original image. Come with your lovely picture and get your disk like a voyager!

# How we built it
Python: Using packages like NumPy and PIL to conduct an Elliptical Curve Cryptography encryption for images and display the encrypted images on a golden voyager disc through image processing techniques.
Google Spreadsheet: Using the Google Cloud Platform to enable API access for both the google drive and google spreadsheet. Then, using a service account coupled with python extension packets (pygsheets for connection to gsheet, and pandas for data frames), necessary data was stored into the spreadsheet and later retrieved through iterating over a generator function of the spreadsheet.
Flask: Incorporating back-end ECC encryption and decryption algorithm with the front end to render web pages and provide functionality. Allowing users to input/upload their local pictures to our platform, and then providing an encrypted image to them as the output.
Html, CSS, Javascript: Using both previous and recently obtained knowledge of web-developing techniques to render front-end web pages. Specifically using the parallax technique to improve the visual appeal of our platform.
# Challenges we ran into
Hard to fully integrate front end with back end
Had Difficulties understanding the ECC’s rationale and the instability of the decipher for the self-implemented ECC algorithm at the beginning of the project
Difficult to maintaining information of the image as much as possible while achieving the most random and diverse transformations in a reasonable amount of time
difficult to integrate the google cloud service
# Accomplishments that we're proud of
Everything! We started by getting pretty vague decryption after going through our ECC algorithm. We modified its clarity and largely improved the run time of each encryption/decryption process.
Attended almost every workshop and immersed in the awesomeness of the Wond’ry 24/7.
Slept only 3 hours for two days and are still alive :)
# What we learned
The concept of the Abelian group and the application of geography into the encryption process.
How to use Flask and the reason for many of its bugs
The story of the Voyager and the meaning of graphs on its disk
Pretty much a lot of topics from the workshop (deep learning, webdev, …)
# What's next for Voyager Cryptor
Further optimize the run time of our EEC algorithm and try achieving a better balance between the encryption efficiency and time consumption.
Improve the robustness of the functions and interfaces on the website
Allow user input of multiple images to encrypt/decrypt at the same time
Open up new realms of application (Bitcoin mining, Encrypted chat room, …)
# Citation
Amara, Moncef, and Amar Siad. “Elliptic Curve Cryptography and Its Applications.” International Workshop on Systems, Signal Processing and Their Applications, WOSSPA, 2011, https://doi.org/10.1109/wosspa.2011.5931464. Singh, Laiphrakpam Dolendro, and Khumanthem Manglem Singh. “Image Encryption Using Elliptic Curve Cryptography.” Procedia Computer Science, vol. 54, 2015, pp. 472–481., https://doi.org/10.1016/j.procs.2015.06.054.