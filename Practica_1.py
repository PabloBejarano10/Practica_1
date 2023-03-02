from multiprocessing import Process
from multiprocessing import BoundedSemaphore, Semaphore, Lock
from multiprocessing import current_process
from multiprocessing import Value, Array
from time import sleep
from random import random, randint

NPROD = 3
N = 5 #cantidad de numeros generados por cada productor 

def delay(factor = 3):
    sleep(random()/factor)

def add_number(storage, index, data, full):
    full.acquire()
    storage[index.value] = data
    delay(6)
    index.value = index.value + 1
    
    
def index_min(a):
    
    l = []
    for x in a:
        l.append(x.value)
    m = minimo(a)
    indice = l.index(m)
    
    return indice


def minimo(a):
    m = min(x.value for x in a if x.value >=0)
    return m
    
def not_all_negative(numbers_prod):
    result = False
    for i in numbers_prod:
        if i.value >= 0:
            result = True
    return result

def producer(sem, number, full):
    for i in range(N): #producimos N numeros
        number.value += randint(1, 7)
        print("PRODUCIENDO")
        sem.release()
        full.acquire()
    
    number.value = -1
    sem.release()
    

def consumer(numbers_prod, lista_sem, lista_full, result):
    
    #Primero esperamos a que todos lor productores produzcan
    for s in lista_sem:
        s.acquire()
    
    indice = 0
    
    while not_all_negative(numbers_prod):
        index = index_min(numbers_prod)
        number = minimo(numbers_prod)
        print("cogiendo el un numero")
        lista_full[index].release()
        delay()
        lista_sem[index].acquire()
        result[indice] = number
        
        indice +=1
        print("escribiendo el numero")
    
    
    
def main():
    
    res = Array('i',NPROD * N)
    numbers_prod = [Value('i',0) for i in range(NPROD)]
    
    lista_sem = [Semaphore(0) for i in range(NPROD)]
    lista_full = [Semaphore(0) for i in range(NPROD)]
    
    lista_prod = [Process(target=producer,
                        name=f'prod_{i}',
                        args=(lista_sem[i], numbers_prod[i], lista_full[i]))
                        for i in range(NPROD)]
    
    cons = Process(target=consumer,
                        name='cons',
                        args=(numbers_prod, lista_sem, lista_full, res))
    
    #Hacemos que los productores produzcan por primera vez:
        
    for p in lista_prod:
        
        p.start()
    
    cons.start()
    
    
    for p in lista_prod:
        
        p.join()
    
    cons.join()
    
    print(list(res))

if __name__ == "__main__":
    main()
        
        
        
        
        
        
        
        
        
        
    
    