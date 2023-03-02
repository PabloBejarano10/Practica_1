from multiprocessing import Process
from multiprocessing import BoundedSemaphore, Semaphore, Lock
from multiprocessing import current_process
from multiprocessing import Value, Array, Manager
from time import sleep
from random import random, randint

NPROD = 3
N = 5 #cantidad de numeros generados por cada productor 

def delay(factor = 3):
    sleep(random()/factor)    
    
def index_min(a):
    """
    Esta funcion devuelve el indice del array a donde se encuentra el minimo
    """
    
    l = []
    for x in a:
        l.append(x.value)
    m = minimo(a)
    indice = l.index(m)
    
    return indice


def minimo(a):
    """
    Devuelve el minimo del array a 
    """
    m = min(x.value for x in a if x.value >=0)
    return m
    
def not_all_negative(numbers_prod):
    """
    Devuelve True si no todos los elementos son negativos y False si hay alguno
    que sea positivo o cero
    """
    result = False
    for i in numbers_prod:
        if i.value >= 0:
            result = True
    return result

def producer(sem, number, full):
    """
    PRODUCTOR:
        Cada productor produce N numeros y el N+1 sera -1. 
        Para evitar la exclusion mutua, debemos tener en cuenta que hay que hacer
        signal cuando el productor haya terminado y wait del semaforo quye indica si 
        la lista donde guardamos los productos esté llena
    """
    
    for i in range(N): #producimos N numeros
        number.value += randint(1, 7)
        print("PRODUCIENDO")
        sem.release()
        full.acquire()
    
    number.value = -1
    sem.release()
    

def consumer(numbers_prod, lista_sem, lista_full, result):
    """
    CONSUMIDOR:
        Espera a que todos los productores hayan producido la primera vez, 
        y posteriormente hace signal en el semaforo del productor del que ha consumido 
        y pone a wait el semaforo de estar lleno donde se guardan los numeros producidos
    """
    #Primero esperamos a que todos lor productores produzcan
    for s in lista_sem:
        s.acquire()
    
    
    while not_all_negative(numbers_prod):
        index = index_min(numbers_prod)
        number = minimo(numbers_prod)
        print("cogiendo el un numero")
        lista_full[index].release()
        delay()
        lista_sem[index].acquire()
        result.append(number)
        
        print("escribiendo el numero")
    
    
    
def main():
    """
    res es el arry donde se guardan los numeros ordenados
    numbers_prod es una lista con los numeros(en Values) producidos
    
    lista_sem son los semaforos que esperaran a que los productores produzcan
    lista_full son los semaforos que revisaran que el productor i ha producido
    
    lista_prod es la lista con los productores
    cons es el consumidor
    """
    res =Manager().list()
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
    
    print(f"La lista final es: {list(res)}")

if __name__ == "__main__":
    main()
        
        
        
        
        
        
        
        
        
        
    
    