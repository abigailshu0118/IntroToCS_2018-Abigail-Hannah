add_library('sound')
import random, os, time

path = os.getcwd()
print (path) 

class Game: 
    def __init__(self): 
        self.w = 800
        self.h = 800
        self.paused = False
        self.state = 'menu' 
        self.score = 0 
        self.g=100 #ground, need this? 
        self.spacing=self.w/9
    
    def createBoard(self):
        self.bgImgs = [] 
        self.cnt = 0 
        self.time = 0 
        self.x = 0 #displacement of the stuff 
        self.y = 0 
        self.vy = 5 #the speed for background images to move 
        
        #align the midpoint of the "creatures" with the x-coordinates of t1,t2 or t3 
        #1st track: self.spacing*2, self.spacing*3 (x-range) 
        #2nd track: self.spacing*4, self.spacing*5 
        #3rd track: self.spacing*6, self.spacing*7 
        self.t1 = self.spacing*(2.5)  
        self.t2 = self.spacing*(4.5) 
        self.t3 = self.spacing*(6.5)
        
        #lists for tracks: correpsonds to t1,t2.t3
        #Enemies to append: MoveTrain, StillTrain, Object, Star
        self.track1 = [] 
        self.track2 = [] 
        self.track3 = []
        
        
        
        
        
        #Add in background images and soundtrack 
        for img in range(4):
            self.bgImgs.append(loadImage(path+'/resources/background_image_'+str(img+1)+'.png'))
            print("list",len(self.bgImgs))
            
            
            
        #add in player 
        self.player = Player(self.t2,750,40,path+"/resources/player.png",0)


        # self.bgMusic=SoundFile(this, path+"/resources/backgroundMusic.mp3")
        # self.bgMusic.amp(0.5)
        # #self.bgMusic.play()
        
    
    def display(self):
        #display time
        self.cnt = (self.cnt+1)%60 
        if self.cnt == 0: #only increment time 
            self.time += 1 
        
        #display images

        self.y+=3
        cnt=0
        image(self.bgImgs[0],self.x,self.y-(cnt*self.h),self.w,self.h)
        cnt+=1
        image(self.bgImgs[1],self.x,self.y-(cnt*self.h),self.w,self.h)
        cnt+=1
        image(self.bgImgs[2],self.x,self.y-(cnt*self.h),self.w,self.h)
        cnt+=1
        image(self.bgImgs[3],self.x,self.y-(cnt*self.h),self.w,self.h)
        cnt+=1
        if self.y-(3*self.h)==0:
            y=0
        
        # image(self.bgImgs[2],0,2*cnt*self.h-self.y, self.w,self.y,  0,0,self.w,self.y)
        # image(self.bgImgs[1],0,cnt*self.h-self.y-1, self.w,self.y,0,0,self.w,self.y)
        # image(self.bgImgs[0],0,cnt-1, self.w,self.h-self.y,0,self.y,self.w,self.h)

        
        # self.y+=3
        # cnt=1
        # image(self.bgImgs[0],0,cnt-1, self.w,self.h-self.y,0,self.y,self.w,self.h)
        # #image(self.bgImgs[0],0,cnt*self.h-self.y-1, self.w,self.y,self.w,self.y,0,0)
        # image(self.bgImgs[1],0,cnt*self.h-self.y-1, self.w,self.y,self.w,self.y,0,0)
        # image(self.bgImgs[2],0,2*cnt*self.h-self.y, self.w,self.y,self.w,self.y,0,0)
   
 
        self.player.display()
        

       #displays of scores etc 
        fill(255)
        text("Score:"+str(self.score),10,25) 
        text("Time:"+str(self.time),10,50) 


class Creature: 
    def __init__(self,x,y,r,imgName,F): 
        self.x = x 
        self.y = y 
        self.r = r #r is radius of character
        self.w = self.r*2 
        self.h = self.r*2 
        self.vy = 0 #just one velocity (its just going vertical) 
        self.F = F #max number of frames
        self.f = 0 #current frame
        self.img = loadImage(imgName)
        
    def update(self):
        self.y += self.vy 
                 
    def display(self):
        self.update()
        #ellipse for the Creatures 
        stroke(255,0,0)
        noFill()
        ellipse(self.x-game.x,self.y,self.r*2, self.r*2) #determine the position later 
        #display image
        image(self.img,self.x-self.r-game.x,self.y-self.r,self.w,self.h,0,0,self.w,self.h) 
         

class Player(Creature):
    def __init__(self,x,y,r,imgName,F): 
        Creature.__init__(self,x,y,r,imgName,F)
        self.keyHandler = {LEFT:False, RIGHT:False, UP:False, DOWN:False}
        #sounds go in here too 
        self.space = 800/9 #should be the same as self.spacing
        self.t1 = self.space*(2.5)  
        self.t2 = self.space*(4.5) 
        self.t3 = self.space*(6.5)
        self.keyLock = 0
        
    def update(self):
        print self.keyLock
        if self.keyLock > 0.0:
            self.keyLock -= 1.0
        else:
            self.keyLock=0.0
        #left and right (with tiles) 
        #what's the velocity though? for the image to instantly move
        self.y += self.vy 

        if self.keyHandler[LEFT] and self.keyLock == 0:
            self.keyLock = 2.0
            if self.x == self.t1:
                self.x = self.t1 
            elif self.x == self.t2:
                self.x = self.t1 
            elif self.x == self.t3:
                self.x = self.t2 
        elif self.keyHandler[RIGHT] and self.keyLock == 0:
            self.keyLock = 2.0
            if self.x == self.t1:
                self.x = self.t2 
            elif self.x == self.t2:
                self.x = self.t3
            elif self.x == self.t3:
                self.x = self.t3
                
        #collisions: define up and down here (to pass the collision)
        # for s in game.stars:
        #     if self.distance(s) < self.r+s.h:  
        #         game.stars.remove(s)
        #         del s      
        #         #self.starSound.play()
        #         game.score += 10
        
        # for o in game.objects:
        #     if self.distance(o) < self.r+o.h and self.keyHandler[DOWN]: #using height here? 
        #         game.score += 20 
        #     elif self.distance(o) < self.r+o.h:
        #         game.__init__()
        #         game.createGame()
                
        # for t in game.stilltrain:
        #     if self.distance(t) < self.r+t.h: 
        #         game.__init__()
        #         game.createGame()
        
        # for m in game.movetrain: 
        #     if self.distance(m) < self.r+m.h and self.keyHandler[UP]:
        #         game.score += 30 
        #     elif self.distance(m) < self.r+m.h:
        #         game.__init__()
        #         game.createGame()
        #still need to let it jump up until the train passes 
                

    def distance(self,other): #for circle
        #return ((self.x-other.x)**2+(self.y-other.y)**2)**0.5                
        return (self.y+other.y) 
                                   
                                                                 
class Objects:
    def __init__(self,x,y,w,h,imgName):
        self.x = x 
        self.y = y 
        self.w = w
        self.h = h 
        self.img = loadImage(imgName)
    
    def update(self):
        self.y += self.vy 
        
    def display(self):
        self.update()
        #ellipse for the Creatures 
        stroke(255,0,0)
        noFill()
        ellipse(self.x-game.x,self.y,self.w, self.h) #determine the position later 
        #display image
        image(self.img,self.x-self.w-game.x,self.y-self.h,self.w,self.h,0,0,self.w,self.h) 
               
        
class MoveTrain(Objects):
    def __init__(self,x,y,w,h,imgName):
        Objects.__init__(self,x,y,w,h,imgName)
        self.vy = 10 #velocity for dropping 

    def update(self):
        self.y += self.vy 
        
class StillTrain(Objects): 
    def __init__(self,x,y,w,h,imgName):
        Objects.__init__(self,x,y,w,h,imgName)
        self.vy = 5 #velocity same as the background 
    
    def update(self):
        self.y += self.vy 
        
class Object(Objects): 
    def __init__(self,x,y,w,h,imgName):
        Objects.__init__(self,x,y,w,h,imgName)
        self.vy = 5 #velocity same as the background 
    
    def update(self):
        self.y += self.vy 
               
class Star(Objects): 
    def __init__(self,x,y,w,h,imgName):
        Objects.__init__(self,x,y,w,h,imgName)
        self.vy = 5 #velocity same as background 
    
    def update(self):
        self.y += self.vy 
        



game=Game()


def setup():
    size(game.w,game.h)
    game.createBoard()
    
def draw():
        
    if game.state=='menu':
        background(0)
        if game.state=="menu" and game.w//2<=mouseX<=game.w//2+160 and game.h//2-30 <= mouseY <= game.h//2+40:
            fill(0,255,0)
        elif game.state=="play":
            if not game.paused:
                background(0)
                game.display()
        else:
            fill(255)
    
        textSize(32)
        text("Play Game",game.w//2,game.h//2)
        noFill()
        rect(game.w//2,game.h//2-30,160,40)

    elif game.state == 'play':
        if not game.paused:
            background(0)
            game.display()
        else:
            fill(255,0,0)
            textSize(32)
            text("Pause",game.w//2,game.h//2)
        
def keyPressed():
    if game.state=="play":
        print (keyCode)
        game.player.keyHandler[keyCode]=True
    
    if game.state=="input name":
        if keyCode==8:
            game.name=game.name[:len(game.name)-1]
        elif keyCode==10:
            f=open("highscores.csv","a")
            f.write(game.name+","+str(game.score)+"\n")
            f.close()
            game.__init__()
            game.createGame()
        print(keyCode)
        if type(key)!=str:
            game.name+=key
    
    if keyCode == 80:
        game.paused = not game.paused
        game.pauseSound.play()
   
def keyReleased():
    game.player.keyHandler[keyCode]=False
    
def mouseClicked():
    if game.state=="menu" and game.w//2<=mouseX<=game.w//2+160 and game.h//2-30 <= mouseY <= game.h//2+40:
        game.state='play'
