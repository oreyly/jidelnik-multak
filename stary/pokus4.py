import pafy 
import vlc 
import time

def play(name):
        #video = pafy.new(name)
        #videolink = video.getbest()
        media:vlc.MediaPlayer = vlc.MediaPlayer(name)  
        media.play()
        time.sleep(5)
        media.stop()
        play(name)
        
print("Enter play name:")
play(input())