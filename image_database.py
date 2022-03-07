#This will be used to store images on the server 

import sqlite3
def imagedbhandler(file_name, file_path, original_poster):
    file_name = str(file_name)
    file_path = str(file_path)
    original_poster = str(original_poster)

    dataToAdd = [(file_name,file_path,original_poster,)]

    conn = sqlite3.connect('images.db')

    c = conn.cursor()

    c.executemany('INSERT INTO images (file_name,file_path,original_poster) VALUES(?,?,?);',dataToAdd)


    conn.commit()

    conn.close()

imagedbhandler('example a','example b','example c')