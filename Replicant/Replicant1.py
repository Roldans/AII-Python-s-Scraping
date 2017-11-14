def crearArchivo(number):
    numberAux=number
    print number
    while numberAux < 10:
        print "a"
        f = open('Replicant'+str(numberAux+1)+'.py','w')
        f.write('Hello World')
        f.close()
        numberAux= numberAux+1
