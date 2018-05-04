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
        
        #align the midpoint of player + objects with the x-coordinates of t1,t2 or t3 
        self.t1 = self.spacing*(2.5)  #1st track: self.spacing*2, self.spacing*3 (x-range)
        self.t2 = self.spacing*(4.5)  #2nd track: self.spacing*4, self.spacing*5 
        self.t3 = self.spacing*(6.5)  #3rd track: self.spacing*6, self.spacing*7 
        
        self.rail = [] 
        for a in range(0,3):
            tmp = [] 
            self.rail.append(tmp)
        
    def createBoard(self): 
        self.bgImgs = [] 
        self.cnt = 0 
        self.time = 0 
        self.x = 0 #displacement of the stuff 
        self.y = 0 #this will change 
        self.z = 0 
        self.vy = 5 #the speed for background images to move
        
        # self.bgMusic=SoundFile(this, path+"/resources/backgroundMusic.mp3")
        # self.bgMusic.amp(0.5)
        # #self.bgMusic.play()
                
        #Add in background images and soundtrack 
        for i in range(4):
            self.bgImgs.append(loadImage(path+'/resources/background_image_'+str(i+1)+'.png'))
        
        #add in player 
        self.player = Player(self.t2,750,40,path+"/resources/player.png",0)
        
        #increment time 
        #start running score 
        
        
    def generate(self):
        #lists for tracks: correpsonds to t1,t2.t3
        #Enemies to append: MoveTrain, StillTrain, Object, Star
        self.track1 = [(MoveTrain(self.t1,self.y,70,175,path+"/resources/ExtraMoveTrain.png")),\
                       (StillTrain(self.t1,self.y,70,175,path+"/resources/fire.png")),\
                       (Object(self.t1,self.y,70,70,path+"/resources/object.png")),\
                       (Star(self.t1,self.y,40,40,path+"/resources/star.png"))] 
        self.track2 = [(MoveTrain(self.t2,self.y,70,175,path+"/resources/ExtraMoveTrain.png")),\
                       (StillTrain(self.t2,self.y,70,175,path+"/resources/fire.png")),\
                       (Object(self.t2,self.y,70,70,path+"/resources/object.png")),\
                       (Star(self.t2,self.y,40,40,path+"/resources/star.png"))]  
        self.track3 = [(MoveTrain(self.t3,self.y,70,175,path+"/resources/ExtraMoveTrain.png")),\
                       (StillTrain(self.t3,self.y,70,175,path+"/resources/fire.png")),\
                       (Object(self.t3,self.y,70,70,path+"/resources/object.png")),\
                       (Star(self.t3,self.y,40,40,path+"/resources/star.png"))]         


        #all enemies randomizing here
        q = random.randint(0,3)
        r = random.randint(0,3) 
        s = random.randint(0,3) 
        while q == r == s:
            q = random.randint(0,3)
            r = random.randint(0,3) 
            s = random.randint(0,3) 
        
        cnt = 2 
        for a in (self.rail):
            cnt = (cnt+1)%3    #for looping through 0,1,2
            #print cnt 
            if cnt==0:  #will not append unless less than 3? 
                a.append(self.track1[q]) 
            elif cnt==1:
                a.append(self.track2[r])
            elif cnt==2:
                a.append(self.track3[s])
        
        #removing objects when its past the screen             
        for a in (self.rail):
            for b in a: 
                if b.y-(b.h/2) > self.h:
                    a.remove(b)
        
        #make sure that the 3 things appended are not all the object the player can't touch 
            
                            
    def update(self):
        #display time
        self.cnt = self.cnt+1
        if self.cnt % 12 == 0:
            self.time += 1 
        
        self.player.update()
        for a in self.rail:
            for b in a:
                b.update()        
    
        if 0 <= self.time <= 500:
            if self.cnt % 70 == 0:
                self.generate()
                #print ("70")
        elif 500 < self.time <= 1000:
            if self.cnt % 65 == 0:
                self.generate()
                #print ("65")
        elif 1000 < self.time <= 2000:
            if self.cnt % 60 == 0:
                self.generate()
                #print ("60")
        elif 2000 < self.time <= 3000:
            if self.cnt % 55 == 0:
                self.generate()
                #print ("55")
        elif self.time > 3000:
            if self.cnt % 53 == 0:
                self.generate()
                #print ("53")

        
    def display(self):
        #display background images 
        self.z+=5
        if self.z-(3*self.h)==0:
            self.z=0
        cnt=0
        image(self.bgImgs[0],self.x,self.z-(cnt*self.h),self.w,self.h)
        cnt+=1
        image(self.bgImgs[1],self.x,self.z-(cnt*self.h),self.w,self.h)
        cnt+=1
        image(self.bgImgs[2],self.x,self.z-(cnt*self.h),self.w,self.h)
        cnt+=1
        image(self.bgImgs[3],self.x,self.z-(cnt*self.h),self.w,self.h)
        
        #display player         
        self.player.display()
        
        #displaying the rest 
        for a in self.rail:
            for b in a: 
                b.display() 
                
       #displays of scores etc 
        fill(255)
        text("Score:"+str(self.time),10,25) 
        #text("Time:"+str(self.time),10,50) 


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
        ellipse(self.x-game.x,self.y,self.w, self.h) #determine the position later 
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
        # print self.keyLock
        if self.keyLock > 0.0:
            self.keyLock -= 1.0
        else:
            self.keyLock=0.0
        #left and right (with tiles) 

        self.y += self.vy 

        if self.keyHandler[LEFT] and self.keyLock == 0:
            self.keyLock = 14.0
            if self.x == self.t1:
                self.x = self.t1 
            elif self.x == self.t2:
                self.x = self.t1 
            elif self.x == self.t3:
                self.x = self.t2 
        elif self.keyHandler[RIGHT] and self.keyLock == 0:
            self.keyLock = 14.0
            if self.x == self.t1:
                self.x = self.t2 
            elif self.x == self.t2:
                self.x = self.t3
            elif self.x == self.t3:
                self.x = self.t3
        
        
        #collision detection and scores   
        if self.x == game.t1:
            count = 0 
        elif self.x == game.t2:
            count = 1 
        elif self.x == game.t3: 
            count = 2 
            
        for b in game.rail[count]:
            if self.distance(b) < self.r+(b.h/2) and self.distance(b) >0:
                if isinstance(b, MoveTrain):
                # if b == game.track1[0] or game.track2[0] or game.track3[0]: #movetrain 
                    if self.keyHandler[UP]:
                        continue
                        # game.score += 30 
                    else:
                        game.__init__()
                        game.createBoard()
                if isinstance(b, StillTrain):   
                # elif b == game.track1[1] or game.track2[1] or game.track3[1]: #still train(fire) 
                    game.__init__()
                    game.createBoard()
                if isinstance(b, Object): 
                # elif b == game.track1[2] or game.track2[2] or game.track3[2]: #object 
                    if self.keyHandler[DOWN]:
                        continue
                        # game.score += 20 
                    else: 
                        game.__init__()
                        game.createBoard()
                if isinstance(b, Star): 
                # elif b == game.track1[3] or game.track2[3] or game.track3[3]: #star 
                    game.time += 100 
                    game.rail[count].remove(b)
            else: continue 
                
                
    def distance(self,other): #for circle
        return (self.y-other.y) 
                                   
                                                                 
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
        image(self.img,self.x-game.x-(self.w/2),self.y-(self.h/2),self.w,self.h,0,0,self.w,self.h) 
        
    def where(self):
        return self.y 
               
        
class MoveTrain(Objects):
    def __init__(self,x,y,w,h,imgName):
        Objects.__init__(self,x,y,w,h,imgName)
        self.vy = 3.5 #velocity for dropping 

    def update(self):
        self.y += self.vy 
        
class StillTrain(Objects): 
    def __init__(self,x,y,w,h,imgName):
        Objects.__init__(self,x,y,w,h,imgName)
        self.vy = 3.5 #velocity same as the background 
    
    def update(self):
        self.y += self.vy 
        
class Object(Objects): 
    def __init__(self,x,y,w,h,imgName):
        Objects.__init__(self,x,y,w,h,imgName)
        self.vy = 3.5 #velocity same as the background 
    
    def update(self):
        self.y += self.vy 
               
class Star(Objects): 
    def __init__(self,x,y,w,h,imgName):
        Objects.__init__(self,x,y,w,h,imgName)
        self.vy = 3.5 #velocity same as background 
    
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
            game.update()
            game.display()
        else:
            fill(255,0,0)
            textSize(32)
            text("Pause",game.w//2,game.h//2)
        
def keyPressed():
    if game.state=="play":
        #print (keyCode)
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
        #print(keyCode)
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
