from flask import Flask,request
import ast
from random import randint

app = Flask(__name__)


duration=0
temp_fit = 2147483647
best_gnome = ""


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
        TSPUtil(V,MP,TL,POP_SIZE)
        duration=cal_duration(best_gnome,TL)
        print('distance in input'+str(temp_fit))
        print('gnome in input'+str(best_gnome))
        print('duration in input'+str(duration))
    return {"success":"got parameters and already cal"}

@app.route('/get',methods={'GET'})
def output():
    print('distance in output'+str(temp_fit))
    print('gnome in output'+str(best_gnome))
    print('duration in output'+str(duration))
    dis=temp_fit
    dur=duration
    b_gnome=best_gnome
    return {"distance":dis,"duration":dur,"gnome":b_gnome}

class individual:
    def __init__(self) -> None:
        self.gnome = ""
        self.fitness = 0
 
    def __lt__(self, other):
        return self.fitness < other.fitness
 
    def __gt__(self, other):
        return self.fitness > other.fitness

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

def cooldown(temp):
    return (90 * temp) / 100

def TSPUtil(v,mp,tl,pop_size):
    V=v
    MP=mp
    TL=tl
    POP_SIZE=pop_size
    # Generation Number
    gen = 1
    # Number of Gene Iterations
    gen_thres = 5
 
    population = []
    
    temp = individual()
 
    # Populating the GNOME pool.
    for i in range(POP_SIZE):
        temp.gnome = create_gnome(V)
        temp.fitness = cal_fitness(temp.gnome,MP)
        population.append(temp)
 
    print("\nInitial population: \nGNOME     FITNESS VALUE\n")
    for i in range(POP_SIZE):
        print(population[i].gnome, population[i].fitness)
    print()
 
    found = False
    temperature = 10000
 
    # Iteration to perform
    # population crossing and gene mutation.
    while temperature > 1000 and gen <= gen_thres:
        population.sort()
        print("\nCurrent temp: ", temperature)
        new_population = []
 
        for i in range(POP_SIZE):
            p1 = population[i]
 
            while True:
                new_g = mutatedGene(p1.gnome,V)
                new_gnome = individual()
                new_gnome.gnome = new_g
                new_gnome.fitness = cal_fitness(new_gnome.gnome,MP)
 
                if new_gnome.fitness <= population[i].fitness:
                    new_population.append(new_gnome)
                    break
 
                else:
 
                    # Accepting the rejected children at
                    # a possible probability above threshold.
                    prob = pow(
                        2.7,
                        -1
                        * (
                            (float)(new_gnome.fitness - population[i].fitness)
                            / temperature
                        ),
                    )
                    if prob > 0.5:
                        new_population.append(new_gnome)
                        break
 
        temperature = cooldown(temperature)
        population = new_population
        print("Generation", gen)
        print("GNOME     FITNESS VALUE")
        
        for i in range(POP_SIZE):
            print(population[i].gnome, population[i].fitness)
        gen += 1

        
        for i in range(POP_SIZE):
            global temp_fit,best_gnome
            if temp_fit > population[i].fitness:
                temp_fit = population[i].fitness
                best_gnome = population[i].gnome
    
        print('distance'+str(temp_fit))
        print('best_gnome'+str(best_gnome))


if __name__ == '__main__':
     app.run(host='192.168.1.100', port=5002,debug=True)
     
