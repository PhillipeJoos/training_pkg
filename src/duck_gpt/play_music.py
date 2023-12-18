import os
import time
import threading

# function to kill mpg123 process after a certain time
def kill_music(seconds):
    # wait for the specified time
    time.sleep(seconds)

    # kill the mpg123 process
    os.system("pkill mpg123")


# función para reproducir música desde un archivo con os y mpg123
# recibe el archivo y el tiempo a reproducir como parámetros
def play_music(file, seconds):

    # thread para matar el proceso de mpg123
    t = threading.Thread(target=kill_music, args=(seconds,))
    t.start()

    # reproduce el archivo
    os.system("mpg123 ../media/" + file)

if __name__ == "__main__":
    # reproducir música
    play_music("chipi.mp3", 3)