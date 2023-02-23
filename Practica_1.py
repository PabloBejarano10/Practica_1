from multiprocessing import Process
from multiprocessing import BoundedSemaphore, Semaphore, Lock
from multiprocessing import current_process
from multiprocessing import Value, Array
from time import sleep
from random import random, randint


NPROD = 3
N = 10 #cantidad de numeros generados por cada productor 

def delay(factor = 3):
    sleep(random()/factor)

def add_number(storage, index, data, full):
    full.acquire()
    storage[index.value] = data
    delay(6)
    index.value = index.value + 1

def gen_number(number):
    """
    Actualiza el valor de number 
    """
    number.Value += randint(1,3)
    
def producer(sem, number, full):
    sem.acquire()
    gen_number(number)
    full.release()
    
def index_min(a,minimo):
     if minimo in a:   
        for i in range(len(a)):
            if a[i] == minimo:
                return i
     else:
        return -1
    

def minimo(a):
    m = min(x for x in a if x>=0)
    return m
    
    
def consumer(numbers_prod, lista_sem, full):
    index = index_min(numbers_prod)
    lista_sem[index].release()
    number = minimo(numbers_prod)
    full.acquire()
    pass
    
def main():
    pass
    
    