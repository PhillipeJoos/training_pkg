import os
import time

# función para reproducir música desde un archivo con os y mpg123
# recibe el archivo y el tiempo a reproducir como parámetros
def play_music(file, seconds):

    # reproduce el archivo
    os.system("mpg123 ../media/" + file)

    # espera el tiempo especificado
    time.sleep(seconds)
   
    # detiene la reproducción
    os.system("killall mpg123")

if __name__ == "__main__":
    # reproducir música
    play_music("chipi.mp3", 10)