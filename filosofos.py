import threading
import random
import time

class Filosofo(threading.Thread):
    running = True 
    def __init__(self, indice, tenedorizquierdo, tenedorderecho):
        threading.Thread.__init__(self)
        self.indice = indice
        self.tenedorizquierdo = tenedorizquierdo
        self.tenedorderecho = tenedorderecho

    def run(self):
        while(self.running):
            time.sleep(random.randint(1,4)) #tiempo de espera
            print ('Filosofo %s esta esperando' % self.indice)
            self.comer()

    def comer(self):
        # verificar si los tenedores estan libres para comer
        tenedor1, tenedor2 = self.tenedorizquierdo, self.tenedorderecho
        #print('a')
        while self.running:
            tenedor1.acquire() # wait operation on izquierdo tenedor
            #print ('Filosofo %s obtiene el tenedor izquierdo' % self.indice)
            locked = tenedor2.acquire(False) 
            #print(locked)
            #print ('Filosofo %s intenta obtener el tenedor derecho' % self.indice)
            if locked: break #if derecho tenedor is not available leave izquierdo tenedor
            tenedor1.release()
            #print ('Filosofo %s suelta los tenedores que tenia' % self.indice)
            tenedor1, tenedor2 = tenedor2, tenedor1
        else:
            return
        self.comiendo()
        tenedor2.release()#suelta tenedor derecho
        tenedor1.release()#suelta tenedor izquierdo
 
    def comiendo(self):			
        print ('Filosofo %s empieza a comer '% self.indice)
        time.sleep(random.randint(1,4))#tiempo comiendo
        print ('Filosofo %s termina de comer' % self.indice)

def main():
    tenedores = [threading.Semaphore() for n in range(5)]

    Filosofos= [Filosofo(i, tenedores[i%5], tenedores[(i+1)%5])
            for i in range(5)]

    Filosofo.running = True
    for p in Filosofos: p.start()
    time.sleep(10)
    Filosofo.running = False
 

if __name__ == "__main__":
    main()

