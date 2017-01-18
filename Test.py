import os
import time

from random import randint, choice

currentKamer = 1
class Character: 
  #data
  def __init__(self): 
    self.naam = "" 
    self.levens = 1 
    self.levens_max = 1 
  
  #het vecht systeem voor speler en tegenstander is hetzelfde (ik ben lui en dit is makkelijker)
  def do_schade(self, tegenstander): 
    schade = min( 
        max(randint(0, self.levens) - randint(0, tegenstander.levens), 0), 
        tegenstander.levens) 
    tegenstander.levens = tegenstander.levens - schade 
    if schade == 0: print "%s ontwijkt %s's aanval." % (tegenstander.naam, self.naam) 
    else: print "%s beschadigd %s!" % (self.naam, tegenstander.naam) 
    return tegenstander.levens <= 0 

#tegenstander functies 
class Tegenstander(Character): 
  def __init__(self, speler):
    randomtegenstander = randint(0, 10)
    Character.__init__(self)
    self.levens = randint(1, speler.levens)
    if randomtegenstander > 5:
      self.naam = 'een aziaat' 
    else:
      self.naam = 'een brugger' 

class Wim(Character):
  def __init__(self, speler): 
      Character.__init__(self) 
      self.naam = 'Levens verpester Wim' 
      self.levens = randint(3, speler.levens)
      

#speler functies 
class Speler(Character): 
  def __init__(self): 
    Character.__init__(self) 
    self.state = 'normal' 
    self.levens = 10 
    self.levens_max = 10 
  
  #stoppen
  def quit(self): 
    print "%s kan niet meer uit de school ontsnappen en gaat dood.\nR.I.P." % self.naam 
    self.levens = 0 
  
  #help commando
  def help(self): print Commands.keys() 
  
  #laat levens zien
  def status(self): print "%s's levens: %d/%d" % (self.naam, self.levens, self.levens_max) 
  
  #als je te lang loopt
  def moe(self): 
    print "%s voelt zich moe." % self.naam 
    self.levens = max(1, self.levens - 1) 
  
  #slapen/rusten
  def rest(self): 
    if self.state != 'normal': print "%s kan nu niet rusten!" % self.naam; self.tegenstander_attacks() 
    else: 
      print "%s rust." % self.naam 
      if randint(0, 1): 
        self.tegenstander = Tegenstander(self) 
        print "%s is abrupt wakker gemaakt door %s!" % (self.naam, self.tegenstander.naam) 
        self.state = 'fight' 
        self.tegenstander_attacks() 
      else: 
        if self.levens < self.levens_max: 
          self.levens = self.levens + 1 
        else: print "%s heeft te veel gerust." % self.naam; self.levens = self.levens - 1 
  
  #rond lopen
  def verken(self): 
    if self.state != 'normal': 
      print "%s is te druk bezig!" % self.naam 
      self.tegenstander_attacks() 
    else: 
      print ("%s verkent " + kamers[currentKamer]["naam"]) % self.naam 
      if randint(0, 1): 
        self.tegenstander = Tegenstander(self) 
        print "%s treft %s!" % (self.naam, self.tegenstander.naam) 
        self.state = 'fight' 
      else: 
        if randint(0, 1): self.moe() 
  
  #vluchten
  def flee(self): 
    if self.state != 'fight': print "%s rent in angst weg." % self.naam; self.moe() 
    else: 
      if randint(1, self.levens + 5) > randint(1, self.tegenstander.levens): 
        print "%s vlucht van %s." % (self.naam, self.tegenstander.naam) 
        self.tegenstander = None 
        self.state = 'normal' 
      else: print "%s kon niet ontsnappen van %s!" % (self.naam, self.tegenstander.naam); self.tegenstander_attacks() 
  
  #aanvallen
  def attack(self): 
    if self.state != 'fight': print "%s zwaait in de lucht, maar hij geeft op." % self.naam; self.moe() 
    else: 
      if self.do_schade(self.tegenstander): 
        print "%s vermoord %s!" % (self.naam, self.tegenstander.naam) 
        self.tegenstander = None 
        self.state = 'normal' 
        if randint(0, self.levens) < 10: 
          self.levens = self.levens + 1 
          self.levens_max = self.levens_max + 1 
          print "%s voelt zich sterker!" % self.naam
      else: self.tegenstander_attacks() 
  
  #als tegenstander je dood
  def tegenstander_attacks(self): 
    if self.tegenstander.do_schade(self): print "%s was vermoord bij de gemene meneer %s!!!\nR.I.P." %(self.naam, self.tegenstander.naam) 
    
  def showRoom(self):
    #kamer
    print(20 * "-")
    print("Hier ben je: " + kamers[currentKamer]["naam"])
    print("hier kan je naartoe: %s ") % [i['naam'] for i in kamers.values() if kamers[currentKamer]]
    #leuk zinnetje per kamer
    if "note" in kamers[currentKamer]:
        print (20 * "-")
        print("--" + kamers[currentKamer]["note"])
    print(20 * "-")

  #kamer systeem
  def move(self):
    global currentKamer
    while True:
      self.showRoom()
      naartoe = raw_input("> ").lower().split()
      if naartoe[0] == "go":
          #vertelt waar je gaat
          if naartoe[1] in kamers[currentKamer]:
              #veranderd kamer naar niewe kamer
              currentKamer = kamers[currentKamer][naartoe[1]]
              if randint(0, 1):
                komtwim = randint(0, 10)
                if komtwim < 2:
                  self.tegenstander = Tegenstander(self) 
                  print "%s treft %s!" % (self.naam, self.tegenstander.naam) 
                  self.state = 'fight'
                else:
                  self.tegenstander = Wim(self)
                  print "%s zag dat %s rotzooi zat te maken, %s komt je straffen!" % (self.tegenstander.naam, self.naam, self.tegenstander.naam) 
                  self.state = 'fight'
              else: 
                if randint(0, 1): self.moe()
              break
          #wanneer dat niet werkt
          else:
              print("Een wilde Wim zegt 'Daar mag je niet naartoe!'")
      if naartoe[0] != "go":
        print "Typ 'go' en dan 'waar je naartoe wilt'"
        
      else:
        print "Typ 'go' en dan 'waar je naartoe wilt'"
    
  def plaats(self):
    print("---------------------------")
    print("Je bevindt je hier: " + kamers[currentKamer]["naam"])
    print("---------------------------")

#Leuke zegjes
zin = ['In de verte hoor je Henk van Ommen schreeuwen', 'Je ruikt een raar geurtje', 'Je ziet een brugger door de gang rennen, wim wordt kwaad',]
 	
#commando's 
Commands = { 
  'quit': Speler.quit, 
  'help': Speler.help, 
  'status': Speler.status, 
  'rest': Speler.rest, 
  'verken': Speler.verken, 
  'flee': Speler.flee, 
  'attack': Speler.attack,
  'move' : Speler.move,
  'plaats' : Speler.plaats,
  } 

#dict voor layout
kamers = {

            1 : {  "naam"  : "de Lobby" ,
                   "a"  : 2,
                   "w" : 3 }  ,

            2 : {  "naam"  : "de Trap" ,
                   "d"  : 1,
                   "note"  : "Terwijl je de trap oploopt hoor je in de verte Henk van Ommen schreeuwen" }  ,            

            3 : {  "naam"  : "de Gang rechtdoor" ,
                   "s" : 1,
                   "d" : 4, 
                   "a"  : 5,
                   "w"  : 6 } ,
                   
            4 : {  "naam"  : "de Gymzaal" ,
                   "a" : 3 } ,
            
            5 : {  "naam"  : "de Concierge" ,
                   "a" : 9,
                   "d" : 3 } ,
            
            6 : {  "naam"  : "de Gang rii aula" ,
                   "s" : 3,
                   "a" : 7 } ,
                   
            7 : {  "naam"  : "het Hokje van Juul" ,
                   "d" : 6,
                   "a" : 8 } ,
            
            8 : {  "naam"  : "de Aula kantine" ,
                   "d" : 7,
                   "s" : 9 } ,
            
            9 : {  "naam"  : "het Loerraampje van wim" ,
                   "w" : 8,
                   "d" : 5 }
         }



#introductie
p = Speler() 
p.naam = raw_input("Wat is je naam ? ")
os.system('clear')
print (20 * '-')
print "(type help voor een lijst van acties)"
time.sleep(3)
print (20 * '-')
print "%s betreedt het schoolgebouw, zoekend naar Henk van Ommen." % p.naam
time.sleep(3)
print (20 * '-')
print "Steen van de verkener groet %s." % p.naam
time.sleep(3)
print (20 * '-')
os.system('clear')
print("Hoe moet je lopen?")
print("Eerst 'move' en dan 'go [waar je naartoe wilt]'")
print("Je bevind je hier: " + kamers[currentKamer]["naam"])
time.sleep(6)
os.system('clear')
print("Steen van de verkener wenst je succes en zegt: vergeet niet dat help alle commando's toont")

while(p.levens > 0): 
  line = raw_input("> ") 
  args = line.split() 
  if len(args) > 0: 
    commandFound = False 
    for c in Commands.keys(): 
      if args[0] == c[:len(args[0])]: 
        Commands[c](p) 
        commandFound = True 
        break 
    if not commandFound: 
      print "%s dat is een 1 op de toets.(typ iets van help ofzo)" % p.naam 
 