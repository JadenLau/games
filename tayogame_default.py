import random as random
import os as os
ran = random.randint
import time as time
wait=time.sleep
jb_list =["1.fight","2.people","3.monster","4.team","5.shop","6.levelup","7.dolove","8.pet","9.story"]
stories = {
    "mri_adventure": "Long long time ago, a girl called mri was born. She was a brave girl. She killed thousands of monster since she was just 3. Villagers thought she was the strongest girl in the world. Unluckily, when she was 12, tamos hurt her and reset her level. Now, mri is trying to kill tamos as soon as possible, and you are going to help her.",
    "sam_adventure": "Sam was learning mathematics. One day, he found out that 1+1=2. He was so angry and he cannot accept the TRUTH since he thought 1+1 = 3. Then, he killed almost  the people in the earth."
}
lang={"en":{
    "mon1": "this game is about some mri and monster"
}}
level=114514
chose=0
dl=0
fightingmonster=0
choosepeople=0
p=print
whatname=0
SERIALNUM=4
started=0
pet_serialnum=0
test=0
coin=0
pet_exp=0
pet_level=0
pet_maxhealth=0
pet_skill=0
pet_property=0
Id=4
p("this game is about some mri and monster")
wait(0.1)
p("you need to kill the mri monster")
wait(0.1)
p("you got some coin and exp when you kill the monster")
class skill():
    def __init__(self,name,add_damage,mana_consumption,type):
        self.name=name
        self.add_damage=add_damage
class pet():
    def __init__(self,name,quality,addsave,adddamage,addhealth,serialnum_pet,skill_pet=None):
        self.name=name
        self.type=pet
        self.hp=100
        self.maxhp=100
        self.damage=10
        self.protect=0
        self.type="pet" 
        self.quality=quality
        self.addsave=addsave
        self.adddamage=adddamage
        self.addhealth=addhealth
        self.serialnum_pet=serialnum_pet
        if self.quality=="R":#80%
            self.hp=100
        if self.quality=="SR":#15%
            self.hp=200
            self.damage=20
            self.maxhp=200
        if self.quality=="SSR":#4%
            self.hp=500
            self.damage=50
            self.maxhp=500
        if self.quality=="UR":#1%
            self.hp=1000
            self.maxhp=1000
            self.damage=100
    # def __init__(self,name,age,sex,)
def cmd(linux,windows):
    os.system(f"{linux} # & {windows}")
def clear():
    os.system("clear # & cls")
class people():
  def __init__ (self,name,age,sex,serialnum,damage_wood,damage_fire,damage_water,damage_wind,id,mom=None,dad=None,fight=True,role=None,dolove=True,skill=None):
      self.type="people"
      self.died=False
      self.name=name
      self.sex=sex
      self.mom = mom
      self.dad = dad
      self.age=age
      self.serialnum=serialnum
      self.health=10
      self.maxhealth=1e2
      self.damage=1
      self.basedanage=1
      self.boom=1
      self.fight=True
      self.exp=0
      self.baoji=0
      self.baos=2
      self.role=role
      self.energy=100
      self.maxenergy=100
      self.id = id
      if self.age <= 12:
          self.dolove = False
      def do_love(self, other):
          try:
             if self.type != "people" or other.type != "people":
                 p("do not do love with someone that is not people")#æ´å¥½åéªæ¥æ113*111          
          except Exception as e:
             p(f"invalid class {e}")
             if self.mom == other.mom or self.dad == other.dad:
                  ran(0,1)
          if self.sex == other.sex:
              print("You can't let these two do love.")
              print("It should be a girl and a boy.")
          elif other.dolove is False or self.dolove is False:
              p("they can't do love")
          else:
              print("They can do love!")
              if self.age < 12 or other.age < 12:
                  print("required gang man shi er shui")
              elif not self.fight:
                  p("They can't have a baby.")          
              else:
                  if random.randint(0,1) == 0:
                      print("They don't have a baby.")
                  else:
                      print("They have a baby!")
                      baby_sex = random.randint(0, 1)
                      if baby_sex == 0:
                          global Id
                          global SERIALNUM
                          baby_name = input("What is the baby's name?")
                          SERIALNUM += 1 # increase 1 to serial number
                          Id += 1
                          baby = people(baby_name,0,0,SERIALNUM,0,0,0,0,Id,mom=other,dad=self,fight=False)
                          print("This baby is a boy.")
                          other.fight = False
                          other.dolove = False
                          return baby
                      else:
                          SERIALNUM+=1
                          Id += 1
                          baby_name=input("What is the baby's name?")
                          baby=people(baby_name,0,1,SERIALNUM,0,0,0,0,Id,mom=other,dad=self,fight=False)
                          print("this baby is a girl")

class Team:
    def __init__ (self,name):
        self.name = name  # éä¼åç§°
        self.members = []  # éååè¡¨  
        self.petmember=[]
    def add_member(self,member2):
        if member2 not in self.members:
            if type(member2) is pet:
                if len(self.petmember)>=1:
                    p("The pet of team is full")
                    return False
                else:
                    self.petmember.append(member2)
            if type(member2) is member2:
                if len(self.members)>=4:
                    p("The person of team is full")
                    return False
                else:
                    self.members.append(member2)
                    p(f"{member2.name} has been added to {self.name}")                    
class gamecontroller():
    def __init__(self):
          self.team={}
          self.people_pool=[]
          self.pet_pool=[]
    def create_team(self,team_name):
        if team_name not in self.team:
            self.team[team_name]=Team(team_name)
            p(f"{team_name} has been created")
        # if person
        else:
            p(f"{team_name} has already been created")
    def add_to_pool(self,people):
        if people not in self.people_pool:
            self.people_pool.append(people) 
        else:
            p(f"{people} has already been added to the pool")
    def add_to_pool_pet(self,pets):
        if pets not in self.pet_pool:
            self.pet_pool.append(pets)
class monster():  
    def __init__(self,name):
        self.type="monster"
        self.name=name
        self.maxhp=100*level+ran(1,(20*level))
        self.hp=self.maxhp
        self.protect=ran(1,5)
        self.damage=10*level+ran(1,(5*level))
        if level<=10:
            self.protect=0
    def moss(self):
        self.hp=(100*level+ran(1,(20*level)))*2
        self.damage=(10*level+ran(1,(5*level)))*2
game_controler=gamecontroller()
 #é è¨­è§è²      
som=people("some^2",12,0,10,0,0,0,0,1)
tmns=people("10ç±³è«¾æ¯",12,1,20,0,0,0,0,2)
mri=people("mri",12,1,3,0,0,0,0,3) # 
sam=people("sam",12,0,4,0,0,0,0,4) # surface-to-air missile
smi=monster("semi")#monster
tamos=monster("tam")
mrim=monster("mrim")
sz=monster("sz")
som=gamecontroller.add_to_pool(som)
tmns=gamecontroller.add_to_pool(tmns)
mri=gamecontroller.add_to_pool(mri)

gamecontroller.add_to_pool(28)

game_controler.add_to_pool([som,tmns,mri,sam])
started=input("what do you want to start with")
if started=="yes":   
    p("let's start the game")
    while True:
        p("1.fight")
        p("2.people")
        p("3.monster")
        p("4.team")
        p("5.shop")
        p("6.levelup")
        p("7.dolove")
        p("8.pet")
        p("9.story")
        p("10.help")
        started=input("what do you want to do")
        if started == "1":
            # ran(1,3)
            p(f"level{level}")
            p("choose your team which you want them to fight")
            p("or your can enter 114514 to exit")
            so=input()
            if so == "114514":
                continue
        if started == "2":
            p("please choose the team which will go to fight")
        if started == "3":
            p("1.semi")
            p("2.tam")
            p("3.mrim")
            p("4.sz")
            p("exit")
            started=input("what do you wan to understand")
            if started=="1":
                p("semi is a monster that is a male and he becomes a monster because of the people,the people let the monster bite  him and he became a monster.Therefore he is very hate people.")
            if started=="2":
                p("tam is teacher before he becomes a monster and he is very hate children.It is because he the children let him to be monster.Therefore he is very harte children.")
            if started=="3":
                pass            
        if started == "4":
            p("1.create team")
            p("2.adjust team")
            p("3.exit")
            started=input("what do you want to do")
            if started == "1":
                p("what is your team name?")
                started=input()
                game_controler.create_team({started})
        if started=="5":
            p("1. buy something else\n2. buy lottery\n 3. exit")
            menu = input("enter menu ID in number, enter nothing to exit\n\x20\\--menu-> ")
            try: menu = int(menu)
            except Exception as hateness: print(f'invalid menu ID, not string: {hateness}')
            if menu == 1:
                print("menu: buy something else")
                print("1. buy pet\n2. buy skill\n3. exit")
                started=input("what do you want to buy?")
            if menu == 2:
                print("Menu: Buy Lottery")
                print("1. Buy Lottery Ticket")
                print("2. Lotter")                
                p("1.lotter once")
                p("2.lotter 10 times")
                p("3.The poll of the pet")
                p("4.exit")
                started=input("what do you want to do?")
                if started == 1:
                    # BEGIN LOTTER SYSTEM
                    if coin==1000 or coin>=1000:
                        coin-=1000
                        started=ran(1,100)
                        pet_serialnum+=1
                        if started <= 80:
                            started=ran(1,3)
                            if started == 1:
                                p("you got jaden")
                                pet("jaden","R",0,10,0,pet_serialnum)
                            if started == 2:
                                p("you got jabez")
                                pet("jabez","R",10,0,0,pet_serialnum)
                            if started == 3:
                                p("you got dog")
                                pet("dog","R",0,0,10,pet_serialnum)
                        if started <=95 and started >= 81:
                            started=ran(1,3)
                            if started ==1:
                                p("you got sam")
                                pet("Sam","SR",25,10,0,pet_serialnum)
                            if started==2:
                                p("you got hooman")
                                pet("hooman","SR",0,10,25,pet_serialnum)
                            if started==3:
                                p("you got chm")
                                pet("chm","SR",10,25,0,pet_serialnum)
                        if started <=99 and started>=96:
                            started=ran(1,3)
                            if started==1:
                                p("you got piggie")
                                pet("piggie","SSR",50,50,50,pet_serialnum)
                            if started==2:
                                p("you got junny")
                                pet("junny","SSR",50,50,50,pet_serialnum)
                            if started==3:
                                p("you got littlewhite")
                                pet("littlewhite","SSR",50,50,50,pet_serialnum)
                        if started==100:
                            started=ran(1,2)
                            if started==1:
                                p("you got phcwkc!!!")
                                pet("pornwkc","UR",100,100,100,pet_serialnum)
                            if started==2:
                                p("you got jadenproplusmaxultra!!!")
                                pet("pornwkc","UR",100,100,100,pet_serialnum)
                    else:
                        p(f"you don't have enough coin.you need {1000-coin} more coin")
                if started == 2:
                    if coin==10000 or coin>=10000:
                        coin-=10000
                        for i in range(10):
                                started=ran(1,100)
                                pet_serialnum+=1
                                if started <= 80:
                                    started=ran(1,3)
                                    if started == 1:
                                        p("you got jaden")                      
                                        pet("jaden","R",0,10,0,pet_serialnum)
                                    if started == 2:
                                        p("you got jabez")
                                        pet("jabez","R",10,0,0,pet_serialnum)
                                    if started == 3:
                                        p("you got dog")
                                        pet("dog","R",0,0,10,pet_serialnum)
                                if started <=95 and started >= 81:
                                    started=ran(1,3)
                                    if started ==1:
                                        p("you got sam")
                                        pet("Sam","SR",25,10,0,pet_serialnum)
                                    if started==2:
                                        p("you got hooman")                                  
                                        pet("hooman","SR",0,10,25,pet_serialnum)
                                    if started==3:
                                        p("you got chm")
                                        pet("chm","SR",10,25,0,pet_serialnum)
                                if started <=99 and started>=96:
                                    started=ran(1,3)
                                    if started==1:
                                        p("you got piggie")
                                        pet("piggie","SSR",50,50,50,pet_serialnum)
                                    if started==2:
                                        p("you got junny")
                                        pet("junny","SSR",50,50,50,pet_serialnum)
                                    if started==3:
                                        p("you got littlewhite")
                                        pet("littlewhite","SSR",50,50,50,pet_serialnum)
                                if started==100:
                                    started=ran(1,2)
                                    if started==1:
                                        p("you got phcwkc!!!")
                                        pet("pornwkc","UR",100,100,100,pet_serialnum)
                                    if started==2:
                                        p("you got jadenproplusmaxultra!!!")
                                        pet("jadenproplusmaxultra","UR",100,100,100,pet_serialnum)
                    else:
                        p(f"you don't have enough coin.you need {10000-coin} more coin") 
                if started==3:
                    p("jaden(26.7%)add save:0,add damage:10,add health:0")
                    p("jabez(26.7%)add save:10,add damage:0,add health:0")
                    p("dog(26.7%)add save:0,add damage:0,add health:10")
                    p("Sam(5%)add save:25,add damage:10,add health:0")
                    p("hooman(5%)add save:0,add damage:10,add health:25")
                    p("chm(5%)add save:10,add damage:25,add health:0")
                    p("piggie(1.3%)add save:50,add damage:50,add health:50")
                    p("junny(1.3%)add save:50,add damage:50,add health:50")
                    p("littlewhite(1.3%)add save:50,add damage:50,add health:50")
                    p("phcwkc(0.5%)add save:100,add damage:100,add health:100")
                    p("jadenproplusmaxultra(0.5%)add save:100,add damage:100,add health:100")
                    started=input("press 1 to exit")
                    if started == 1:
                        continue
                if started == 4:
                    continue
