from multiprocessing import Process
from multiprocessing import BoundedSemaphore, Semaphore, Lock
from multiprocessing import current_process
from multiprocessing import Value, Array, Manager
from time import sleep
from random import random, randint

NPROD = 6
N = 5 #cantidad de numeros generados por cada productor 
TAM_ARRAY = 5 #tamaño del array circular

def delay(factor = 3):
    sleep(random()/factor) 
    
def print_array(array):
    s = ""
    for i in array:
        s = s + f"| {i}"
    print(s)
    
def index_min(a):
    """
    Esta funcion devuelve el indice del array a donde se encuentra el minimo
    """
    
    l = []
    for x in a:
        l.append(x)
    m = minimo(a)
    indice = l.index(m)
    
    return indice


def minimo(a):
    """
    Devuelve el minimo del array a 
    """
    m = min(x for x in a if x >=0)
    return m
    
def not_all_negative(numbers_prod):
    """
    Devuelve True si no todos los elementos son negativos y False si hay alguno
    que sea positivo o cero
    """
    result = False
    for i in numbers_prod:
        if i >= 0:
            result = True
    return result

def producer(array, indice_lista, sem, full):
    """
    PRODUCTOR:
        Cada productor produce N numeros y el N+1 sera -1. 
        Para evitar la exclusion mutua, debemos tener en cuenta que hay que hacer
        signal cuando el productor haya terminado y wait del semaforo quye indica si 
        la lista donde guardamos los productos esté llena.
        
        Además los numeros que genera se meteran en un Array de donde lo cogerá 
        el consumidor.
    """
    delay(10)
    seed = randint(0,5)
    for i in range(TAM_ARRAY): #Primero llenamos el buffe del productor 
        seed += randint(1, 7)
        array[i] = seed
        print("PRODUCIENDO")
    sem.release()
    full.acquire()
    
    print_array(array)
    
    for i in range(N-TAM_ARRAY):
        full.acquire()
        print("PRODUCIENDO")
        seed += randint(1, 7)
        array[indice_lista.value] = seed
        print("escribiendo el numero en el bufer del productor")
        indice_lista.value = (indice_lista.value + 1) % TAM_ARRAY
        sem.release()
    
    
    array[indice_lista.value] = -1
    indice_lista.value = (indice_lista.value + 1) % TAM_ARRAY
    for _ in range(TAM_ARRAY):
        indice_lista.value = (indice_lista.value + 1) % TAM_ARRAY
        delay(10)
        sem.release()
        full.acquire()

def consumer(numbers_prod, lista_indices_array, lista_array, lista_sem, lista_full, result):
    """
    CONSUMIDOR:
        print("escribiendo el numero")
        Espera a que todos los productores hayan producido la primera vez, 
        y posteriormente hace signal en el semaforo del productor del que ha consumido 
        y pone a wait el semaforo de estar lleno donde se guardan los numeros producidos
    """
    
    #Primero esperamos a que todos lor productores llenen los buffer 
    for i in range(NPROD):
        lista_sem[i].acquire()
    
    #En este momento ya están todos lo buffer llenos
    for i in range(NPROD):
        delay()
        numbers_prod[i]= lista_array[i][lista_indices_array[i].value]
        lista_full[i].release()
       
    while not_all_negative(numbers_prod):
        index = index_min(numbers_prod)
        number = minimo(numbers_prod)
        print(f"cogiendo el un numero de la lista comun {index}")
        print(lista_sem[index])
        lista_sem[index].acquire()
        numbers_prod[index] = lista_array[index][lista_indices_array[index].value]
        lista_full[index].release()
        print(f" estado del semaforo despues del release {lista_full[index]}")
        print(f"cogiendo el un numero del buffer del prod {index} y metiendolo en la lista comun")
        delay()
        print("escribiendo el numero en el resultado")
        result.append((number,index))
        
        
        print(result)
        print_array(numbers_prod)
        
    for i in range(NPROD):
        lista_full[i].release()
        
    print("FIN DE CONSUMER")
    
    
    
def main():
    """
    res es el array donde se guardan los numeros ordenados
    numbers_prod es una lista con los numeros(en Values) producidos
    
    lista_sem son los semaforos que esperaran a que los productores produzcan
    lista_full son los semaforos que revisaran que el productor i ha producido
    
    lista_prod es la lista con los productores
    cons es el consumidor
    """
    res = Manager().list()
    numbers_prod = Array('i',NPROD)
    lista_indices_array = [Value('i',0) for i in range(NPROD)]  
    lista_array = [Array('i',TAM_ARRAY) for i in range(NPROD)]  
    
    lista_sem = [Semaphore(0) for i in range(NPROD)]
    lista_full = [Semaphore(0) for i in range(NPROD)]
    
    lista_prod = [Process(target=producer,
                        name=f'prod_{i}',
                        args=(lista_array[i], lista_indices_array[i], lista_sem[i], lista_full[i]))
                        for i in range(NPROD)]
    
    cons = Process(target=consumer,
                        name='cons',
                        args=(numbers_prod, lista_indices_array, lista_array, lista_sem, lista_full, res))
    
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
        
        
        
        
        
        
        
        
        
        
    
    