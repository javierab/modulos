import sys
import math

#TODO: incorporar plan minero
#TODO: incorporar tamanos exactos de modulos
#TODO: incorporar info niveles
#TODO: incorporar info rampas
#TODO: incorporar calculo de recuperacion
#TODO: incorporar info fase III


def load(t, newload):
    global carga
    global current_carga
    global total_carga
    global lost_days
    #veo si cumplo condiciones para seguir cargando
    if res_carga[current_carga]!= 0 and current_done < res_carga[current_carga]:
        lost_days+=delta
        print "No puedo continuar:"
        print "Riego Refino de modulo %d no ha sido terminado: requisito para cargar %d" %(res_carga[current_carga], current_carga)
        print "******************************"
    else:
        print "Voy a cargar modulo %d" %(current_carga)
        if(carga[current_carga] - newload >0): #cargo y sigo en el mismo
            total_carga+=newload
            carga[current_carga]-=newload
            newload = 0
            print "Total Cargado: %d ton" %total_carga
        elif(carga[current_carga] - newload == 0): #cargo pero avanzo el current,
            total_carga+=newload
            carga[current_carga] -=newload #descargo
            current_carga+=1
            print "Total Cargado: %d ton" %total_carga
        elif(carga[current_carga] - newload < 0): #cargo lo que cabe, avanzo y cargo el resto.
            newload -= carga[current_carga]
            total_carga+=newload
            carga[current_carga] = 0
            current_carga+=1
            load(newload)


def cond_riego(t):
    global delta
    global current_curado
    global current_ils
    global current_refino
    global current_carga
    global current_done
    global curado
    global ils
    global refino
    global res_curado
    global n_riego
    global n_curado
    global started
    
    for i in range(0, current_curado+1):
        curado[i]-=delta
    for i in range(0, current_ils+1):
        ils[i]-=delta  
    for i in range(0, current_refino+1):
        refino[i]-=delta         
    #agrego los posibles nuevos curados.
    #n_riego = current_curado - current_done
    #n_curado = current_curado - current_ils
    #veo si puedo avanzar
    
    #esto no deberia pasar.
    if n_riego >= 6:
            print "Maximo de %d riegos simultaneo alcanzado" %n_riego
    #cumplo la restriccion, soy el unico en proceso.
    while (current_carga > res_curado[current_curado+1] and started == False):
        print "Entro al loop: %d" %carga[current_curado+1]
        #avanzo a curar todos los que puedo.
        if(carga[current_curado+1] == 0):
            current_curado+=1
            print "Se comienza el curado de: %d" %current_curado
            started = True
        else:
            print "No puedo comenzar curado:"
            print "Carga de %d es %d: menor que %d" %(current_curado+1, carga[current_curado+1], weight)
            break
        #n_riego = current_curado - current_done
        #n_curado = current_curado - current_ils
    #ahora veo cuales puedo avanzar en las fases de riego.
    
    for i in range(1, max(current_curado, current_ils, current_refino)+1):
        if refino[i] <= 0 and i> current_done:
            #verifico que termino uno: lo quito del conteo.
            print "Termina refino de: %d" %i
            current_done = max(current_done,i)
        if ils[i] <= 0 and i> current_refino:
            print "Termina ils de: %d" %i
            current_refino = max(current_refino,i)    
        if curado[i] <= 0 and i> current_ils:
            print "Termina curado de: %d" %i
            current_ils = max(current_ils,i)     
    #print "Listo el curado hasta: %s" %current_ils
    #print "Listo el riego ils hasta: %s" %current_refino 
    #print "Listo el riego refino hasta: %s" %current_done 

#definimos las variables importantes
delta = 10 #numero de dias
velocidad = 11 #ton/dia -> 220 cada 10 dias.
#TODO: por ahora vamos a asumir modulos de volumen identico
weight = 220
t_curado = 20 #dias
#TODO: agregar t_ils para los modulos de fase III
t_ils = 30 #dias
t_refino = 30 #dias
total_carga = 0 #por si la carga es irregular
lost_days = 0
started = False
#ahora agregamos las restricciones
#SOLO MODULOS FASE IV

#para ir llevando las cuentas de dias y pesos.
carga = [weight]*108
curado = [t_curado]*108
ils = [t_curado]*108
refino = [t_curado]*108

#para llevar las restricciones.
res_carga = [0]*108
res_curado = [0]*108

#no vamos a usar nunca el elemento 0, solo como "null".
res_carga[2]=1
res_curado[2]=res_carga[12]=10
res_curado[7]=res_carga[18]=11
res_curado[12]=23
res_curado[18]=27
res_curado[24]=res_carga[31]=30
res_curado[31]=res_carga[52]=41
res_curado[37]=res_carga[57]=45
res_curado[42]=res_carga[62]=48
res_curado[46]=res_carga[66]=50
res_curado[49]=res_carga[69]=51
res_curado[52]=res_carga[72]=61
res_curado[57]=res_carga[76]=65
res_curado[62]=res_carga[81]=68
res_curado[66]=res_carga[85]=70
res_curado[69]=res_carga[88]=71
res_curado[72]=res_carga[91]=80
res_curado[76]=res_carga[95]=84
res_curado[81]=res_carga[99]=87
res_curado[85]=res_carga[103]=89
res_curado[88]=res_carga[106]=90
res_curado[91]=98
res_curado[95]=102
res_curado[99]=105
res_curado[103]=107

#comenzamos el ciclo.
t = 0
#estados para guardar cual es el ultimo modulo en cierto proceso.
current_carga= 1
current_curado = 0
current_ils = 0
current_refino = 0
current_done = 0
#cuantos estoy regando simultaneamente
n_curado = 0
n_riego = 0
#cycle()

def main():
    global t
    global current_carga
    global carga
    global velocidad
    global delta
    global lost_days
    global started
    while(t<450):
        t+=delta
        n_riego = current_ils - current_done
        n_curado = current_curado - current_ils
        print "******************************"
        print "******************************"
        print "Momento actual: %d" %t
        print "Variables: c_carga = %d, c_curado = %d, c_ils = %d, c_refino =%d, c_done = %d, n_riego = %d, n_curado = %d" %(current_carga, current_curado, current_ils, current_refino, current_done, n_riego, n_curado)
        print "Dias perdidos por no poder cargar: %d" %lost_days
        print "******************************"

        newload = velocidad*delta
        #aqui asumo que newload cabe entre el modulo actual y el sgte.
        started = False
        load(t, newload)

        #una vez realizada la carga, verificamos si puedo empezar riego:
        
        cond_riego(t)

if __name__ == "__main__":
    main()







        

