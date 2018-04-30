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
        self.movetrain = []
        self.stilltrain = []
        self.stars = [] 
        self.object = []
        self.cnt = 0 
        self.time = 0 
        self.x = 0 #displacement of the stuff 
        self.y=0 #scrolling of images
        
        #Add in background images and soundtrack 
        for i in range(4):
            self.bgImgs.append(loadImage(path+'/resources/background_image_'+str(i+1)+'.png'))
        
        #temporary:  
        self.player = Player(self.spacing*4.5,750,40,100,path+"/resources/player.png",0) 
        
        # #use CSV file to add in the different stuff (Character, train etc)
        f = open(path+'/resources/componants.csv','r')
        for item in f:
            item = item.strip().split(",")
        #     # if item[0] == 'Player':
        #     #     pass
        #         #self.player = player(int(item[1]),int(item[2]),int(item[3]),int(item[4]),item[5],int(item[6]))
            if item[0] == 'MoveTrain':
                self.movetrain.append(MoveTrain(int(item[1]),int(item[2]),int(item[3]),int(item[4]),item[5],int(item[6])))
            elif item[0] == 'Star':
                self.stars.append(Star(int(item[1]),int(item[2]),int(item[3]),int(item[4]),item[5],int(item[6])))
            elif item[0] == 'StillTrain':
                self.stilltrain.append(StillTrain(int(item[1]),int(item[2]),int(item[3]),int(item[4]),(item[5]),int(item[6])))
            elif item[0]=='End':
                self.stage_x_end = int(item[1])
        f.close()

        # self.bgMusic=SoundFile(this, path+"/resources/backgroundMusic.mp3")
        # self.bgMusic.amp(0.5)
        # #self.bgMusic.play()
        
        
    def display(self):
        #display images 
        cnt=0
        space=self.spacing
 
        for img in self.bgImgs[:]:
            y=(self.y//10)%self.h
            if cnt == 0:
                space=0
                w=self.w
             #   y = (self.y//10)%self.h
               # image(img,0,0,self.w,self.h)
            elif cnt == 1:
              #  y = (self.y//5)%self.h
                space=2*self.spacing
                w=self.spacing
                #image(img,2*self.spacing,0,self.spacing,self.h)
            elif cnt == 2:
              #  y = (self.y//3)%self.h
                space=4*self.spacing
                w=self.spacing
                #image(img,4*self.spacing,0,self.spacing,self.h)
            elif cnt == 3:
               # y = (self.y//2)%self.h
                space=6*self.spacing
                w=self.spacing
                #image(img,6*self.spacing,0,self.spacing,self.h)


            #image(img,0,0,self.w,self.h,)
            image(img,space,0,w,self.h-y,space,0,space+w,self.h-y)
            image(img,space,0,w,self.h-y-1,space,0,space+w,self.h-y-1)
            cnt+=1

        #     def display(self):
        # self.cnt  = (self.cnt + 1)%60
        # if self.cnt == 0:
        #     self.time-=1
        
        # cnt = 0
        # for img in self.bgImgs[::-1]:
        #     if cnt == 0:
        #         x = (self.x//10)%self.w
        #     elif cnt == 1:
        #         x = (self.x//5)%self.w
        #     elif cnt == 2:
        #         x = (self.x//3)%self.w
        #     elif cnt == 3:
        #         x = (self.x//2)%self.w
        #     else:
        #         x = (self.x)%self.w
                
            # image(img,0,0,self.w-x,self.h,x,0,self.w,self.h)
            # image(img,self.w-x-1,0,x,self.h,0,0,x,self.h)
            
        #display the objects etc 
        # for s in self.stars:
        #     s.display()
            
        # for st in self.stilltrain:
        #     st.display()

        # for mt in self.movetrain:
        #     mt.display()   
        
        self.player.display()
        
        # cnt+=1
        # self.cnt = (self.cnt+1)%60 
        # if self.cnt == 0: #only increment time (is this how you do it?) --> need to display it 
        #     self.time += 1 
        
        
        #display background images with moving velocity
        
       #displays of scores etc 
        fill(255)
        text("Score:"+str(self.score),10,25) 
        text("Time:"+str(self.time),10,50) 

 

class Creature: 
    def __init__(self,x,y,r,g,imgName,F): 
        self.x = x 
        self.y = y 
        self.r = r #r is radius of character
        self.w = self.r*2 
        self.h = self.r*2 
        self.w2 = self.r*2 #for trains 
        self.h2 = self.r*4 #for trains 
        self.g = g #need this? 
        self.vy = 0 #just one velocity (its just going vertical) 
        self.v = 0 #this is the extra velocity for moving trains 
        self.F = F #max number of frames
        self.f = 0 #current frame
        self.img = loadImage(imgName) 

    def tile(self):
        self.space = 800/9
        self.t1 = self.space*(2.5)  
        self.t2 = self.space*(4.5) 
        self.t3 = self.space*(6.5)
        
        #align the midpoint of the "creatures" with the x-coordinates of t1,t2 or t3 
        #1st track: self.spacing*2, self.spacing*3 (x-range) 
        #2nd track: self.spacing*4, self.spacing*5 
        #3rd track: self.spacing*6, self.spacing*7 
        
        
    def update(self):
        self.y += self.vy 
        
        # if self.x == self.t1:
        #     self.x = self.t1 
        # elif self.x == self.t2:
        #     self.x = self.t2 
        # elif self.x == self.t3:
        #     self.x = self.t3 
        
                 
    def display(self):
        self.update()
        
        #ellipse for the Creatures 
        stroke(255,0,0)
        noFill()
        ellipse(self.x-game.x,self.y,self.r*2, self.r*2) #determine the position later 
        
        #display image
        image(self.img,self.x-self.r-game.x,self.y-self.r,self.w,self.h,0,0,self.w,self.h) 
        
          
            

class Player(Creature):
    def __init__(self,x,y,r,g,imgName,F): 
        Creature.__init__(self,x,y,r,g,imgName,F)
        self.keyHandler = {LEFT:False, RIGHT:False, UP:False, DOWN:False}
        #sounds go in here too 
        self.space = 800/9
        self.t1 = self.space*(2.5)  
        self.t2 = self.space*(4.5) 
        self.t3 = self.space*(6.5)
        
    def update(self):
        #left and right (with tiles) 
        #what's the velocity though? for the image to instantly move
        self.y += self.vy 

        if self.keyHandler[LEFT]:
            if self.x == self.t1:
                self.x = self.t1 
            elif self.x == self.t2:
                self.x = self.t1 
            elif self.x == self.t3:
                self.x = self.t2 
        elif self.keyHandler[RIGHT]:
            if self.x == self.t1:
                self.x = self.t2 
            elif self.x == self.t2:
                self.x = self.t3
            elif self.x == self.t3:
                self.x = self.t3
        
        
        #collisions: define up and down here (to pass the collision) 
            
        
        
class MoveTrain(Creature):
    def __init__(self,x,y,r,g,imgName,F):
        Creature.__init__(self,x,y,r,g,imgName,F)
        pass
class StillTrain(Creature): 
    def __init__(self,x,y,r,g,imgName,F):
        Creature.__init__(self,x,y,r,g,imgName,F)
        pass 
class Object(Creature): 
    def __init__(self,x,y,r,g,imgName,F):
        Creature.__init__(self,x,y,r,g,imgName,F)
        pass
#something to dug under 
        
class Star(Creature): 
    def __init__(self,x,y,r,g,imgName,F):
        Creature.__init__(self,x,y,r,g,imgName,F)
        pass


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
