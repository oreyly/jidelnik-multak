import time
import cv2
from ffpyplayer.player import MediaPlayer
from PIL import ImageTk,Image

global cap

def getVideoSource(source, width, height):    
    global cap
    cap = cv2.VideoCapture(source)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    fps = cap.get(cv2.CAP_PROP_FPS)      # OpenCV2 version 2 used "CV_CAP_PROP_FPS"
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count/fps if fps > 0 else 0
    print(fps)
    print(duration)
    return cap, duration

def main():
    #sourcePath = "hej2.mp4"
    """
    sourcePath="https://www.youtube.com/watch?v=AHzU-9iozmo"
    video = pafy.new(sourcePath)
    best = video.getbest().url
    au = video.getbestaudio().url
    """
    global cap
    
    
    best = au = "hej3.mp4"
    player = MediaPlayer(au, paused=True)
    camera, dur = getVideoSource(best, 720, 480)

    t = None
    
    while True:
            
        #ret, frame = camera.read()
        audio_frame, val = player.get_frame()
        ret = 1
        if (ret == 0):
            break

        #frame = cv2.resize(frame, (720, 480))
        cv2.imshow('Camera', audio_frame)

        if cv2.waitKey(20) & 0xFF == ord('q'):
            break

        if val != 'eof' and audio_frame is not None:
            frame, t = audio_frame
            print(str(cap.get(cv2.CAP_PROP_POS_MSEC )/1000) + "-" + str(t))
            if( t > dur-0.1):
                player.close_player()
                time.sleep(0.1)
                break

    #camera.release()
    print(3)
    cv2.destroyAllWindows()
    print(4)

if __name__ == "__main__":
    main()