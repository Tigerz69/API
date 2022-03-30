from flask import Flask,request,render_template
from random import randint

app = Flask(__name__)


duration=0
distance = 0
best_gnome = ""
location =None

@app.route('/sendLocation',methods={'post'})
def sendLocation():
    
    body = request.get_json()
    print(body)
    
    return {"location":body}

@app.route('/getLocation',methods={'get'})
def getLocation():
    
    print('got location ',location)
    loc=location
        
        
    
    return {"location":loc}

@app.route('/send2point',methods={'post'})
def input2():
    body2 = request.get_json()
    print(body2)
    global duration,distance,best_gnome
    duration = body2['duration']
    distance = body2['distance']
    best_gnome = '01'
    print(duration)
    print(distance)
    print(best_gnome)
    return {"success":"got parameters for 2 point and already cal"}
@app.route('/send',methods={'POST'})
def input():
    if request.method == 'POST':
        #print (type(request.get_json()))
        body = request.get_json()
        global duration
        V = body['num']
        MP = body['distanceArray']
        TL = body['timeArray']
        print(V)
        print (MP)
        print(TL)
        POP_SIZE=10
        Genetic(V,MP,POP_SIZE)
        duration=cal_duration(best_gnome,TL)
        print('distance in input'+str(distance))
        print('gnome in input'+str(best_gnome))
        print('duration in input'+str(duration))
    return {"success":"got parameters and already cal"}

@app.route("/")
def homepage():
    return render_template("index.html", title="HOME PAGE")

@app.route('/get',methods={'GET'})
def output():
    global duration,distance,best_gnome
    print('distance in output'+str(distance))
    print('gnome in output'+str(best_gnome))
    print('duration in output'+str(duration))
    dis=distance
    dur=duration
    b_gnome=best_gnome
    
    duration=0
    distance = 0
    best_gnome = ""
    return {"distance":dis,"duration":dur,"gnome":b_gnome}

class individual:
    def __init__(self) -> None:
        self.gnome = ""
        self.fitness = 0
 
    def __lt__(self, other):
        return self.fitness < other.fitness
 
    def __gt__(self, other):
        return self.fitness > other.fitness


def repeat_replace (gnome):
    gnome=list(gnome)
    #print(gnome)
    for i in range(len(gnome)):
        if str(i) not in gnome:
            unvisit=i
            #print(str(i)+"does not exist")
    for i in range(len(gnome)):
        ct=gnome.count(str(i))
        #print('i'+str(i))
        #print('count'+str(ct))
        if ct:
            if ct==2:
                item=str(i)
                start=2
                end=len(gnome)
                #find index repeat node
                index = gnome.index(item,start,end)
                #replce repeat node with unvisit node
                gnome[index] = str(unvisit)
            
        
        
    #print(gnome)
    return ''.join(gnome)

def scx(p1,p2,v,MP):

    #Cost from point 0 to 1 of parents
    #print(ord(p2.gnome[1])-48)
    cost1 = MP[0][ord(p1.gnome[1])-48]
    cost2 = MP[0][ord(p2.gnome[1])-48]
                    #การแปลงจาก str ของ gnome ให้กลับเป็น int
    #print(str(cost1)+str(cost2))
    if(cost1<cost2):
        s1 = slice(2)
        gnome= p1.gnome[s1]
        
        s2 = slice(2,v,1)
        gnome+=(p2.gnome[s2])
        gnome=repeat_replace(gnome)
         
    elif(cost2<=cost1):
        s1 = slice(2)
        gnome= p2.gnome[s1]
        #print('gnome in con1'+str(gnome))
        s2 = slice(2,v,1)
        gnome+=(p1.gnome[s2])
        #print('gnome slice'+str(p1.gnome[s2]))
        gnome=repeat_replace(gnome)
    return gnome

def rand_num(start, end):
    return randint(start, end-1)
 

def repeat(s, ch):
    for i in range(len(s)):
        if s[i] == ch:
            return True
 
    return False

def mutatedGene(gnome,v):
    V=v
    gnome = list(gnome)
    while True:
        r = rand_num(1, V)
        r1 = rand_num(1, V)
        if r1 != r:
            temp = gnome[r]
            gnome[r] = gnome[r1]
            gnome[r1] = temp
            break
    return ''.join(gnome)

def create_gnome(v):
    V=v
    gnome = "0"
    while True:
        if len(gnome) == V:
            break
 
        temp = rand_num(1, V)
        if not repeat(gnome, chr(temp + 48)):
            gnome += chr(temp + 48)
 
    return gnome

def cal_fitness(gnome,arr):
    mp = arr
    f = 0
    for i in range(len(gnome) - 1):
        
        f += mp[ord(gnome[i]) - 48][ord(gnome[i + 1]) - 48]
 
    return f
 
def cal_duration(gnome,arr):
    tl = arr
    t = 0
    for i in range(len(gnome) - 1):
        
        t += tl[ord(gnome[i]) - 48][ord(gnome[i + 1]) - 48]
 
    return t


def Genetic(v,mp,pop_size):
    V=v
    MP=mp
    POP_SIZE=pop_size
    
    # Start Generation Number
    gen = 1
    
    # Number of Gene Iterations (number of generation)
    gen_thres = 40

    population = []
    
    temp = individual()
 
    # Populating the GNOME pool.
    for i in range(POP_SIZE):
        temp.gnome = create_gnome(V)
        temp.fitness = cal_fitness(temp.gnome,MP)
        population.append(temp)
    

    print("\nInitial population: \nGNOME      FITNESS VALUE      DISTANCE VALUE")
    for i in range(POP_SIZE):
        print(population[i].gnome, 1/population[i].fitness,population[i].fitness)
    print()
    
    

    while gen <= gen_thres:
        population.sort()
        global best_gnome,distance
        best_gnome=population[0].gnome
        distance=population[0].fitness
        print('best gnome this generation :'+str(population[0].gnome)+' fitness:'+str(1/population[0].fitness))
        print('distance : '+str(population[0].fitness))
        new_population = []

        #elitism method,select best chomosome and put in new population
        new_population.append(population[0])

        for i in range(POP_SIZE-1):#-1 เพราะเอาอันดีสุดเข้าไปแล้ว 1 chomosome
            while True:
                
                p1 = population[0]
                p2 = population[1]

                new_g=scx(p1,p2,V,MP)
                new_gnome = individual()
                new_gnome.gnome= new_g
                new_gnome.fitness = cal_fitness(new_gnome.gnome,MP)

                if new_gnome.fitness < population[i].fitness:
                    new_population.append(new_gnome)
                    break
 
                else:
                    new_g_mutate = mutatedGene(new_gnome.gnome,V)
                    new_gnome_mutate = individual()
                    new_gnome_mutate.gnome = new_g_mutate
                    new_gnome_mutate.fitness = cal_fitness(new_gnome_mutate.gnome,MP)
                    
                    new_population.append(new_gnome_mutate)
                    break
            
        population = new_population
        print("Generation", gen)
        print("GNOME     FITNESS VALUE     DISTANCE VALUE")

        for i in range(POP_SIZE):
            print(population[i].gnome, 1/population[i].fitness,population[i].fitness)
        if gen==gen_thres:
            population.sort()
            best_gnome=population[0].gnome
            distance=population[0].fitness
            print('best gnome this generation :'+str(population[0].gnome)+' fitness:'+str(1/population[0].fitness))
            print('distance : '+str(population[0].fitness))
        
        
        gen += 1
        
        
        

if __name__ == '__main__':
     app.run(host='0.0.0.0',port='8080',debug=True)
     

