from sly import Lexer, Parser
from lexico import ClassLexer


tabla = {}          # tabla con los valores del main: funciones: global:
tabla['global'] = set()
functionID = None   # tuple para el nombre de la función y el estado de la pila
callID = None
inFunction = False  # Variable para saber si estamos en una función o no
listaparams = []
numIF = 0
numWhile = 0
etiqueta = None

#   ┌──────────────────────────────────────────────────────────────────────────┐
#                                     Nodos                      
#  └──────────────────────────────────────────────────────────────────────────┘
class Nodo:
    def escribir(self):
        pass


class NodoFuncion(Nodo):
    def escribirPrologo(self, n_funcion):
        global f_salida
        f_salida.write("\n\n.text\n.globl "+n_funcion+"\n.type "+n_funcion+", @function\n\n"+n_funcion+":\n\tpushl %ebp\n\tmovl %esp, %ebp")

    def escribirEpilogo(self):
        global f_salida
        f_salida.write("\n\tmovl %ebp, %esp\n\tpopl %ebp\n\tret")    


class NodoDefinicion(Nodo):
    def escribir(self):
        global f_salida
        f_salida.write("\n\tsubl $4, %esp")     # para escribir cada declaración de una variable


class nodoAsignacion(Nodo):
    def escribir(self, ID):
        global f_salida, tabla, inFunction
        if ID in tabla['global']:
            f_salida.write("\n\tmovl %eax,"+ ID)
        else:
            f_salida.write("\n\tmovl %eax,"+ str(tabla[functionID[0]][ID]) +"(%ebp)")


class NodoNum(Nodo):
    def escribir(self, v):
        global f_salida
        f_salida.write("\n\tmovl $("+str(v)+"), %eax")        


class NodoID(Nodo):
    def escribir(self, ID):
        global inFunction, f_salida, functionID
        if ID in tabla['global']:
            # ID global
            f_salida.write("\n\tmovl "+ID+"%eax")
        else:
            # ID de parametros o de variable local a una función
            f_salida.write("\n\tmovl " + str(tabla[functionID[0]][ID])+ "(%ebp), %eax")
    

class NodoPush(Nodo):
    def escribir(self):
        global f_salida
        f_salida.write("\n\tpushl %eax")


class NodoSumResProdDiv(Nodo):
    def escribir(self, car):
        if car == "idivl":
            f_salida.write("\n\tmovl %eax, %ebx\n\tpopl %eax\n\tcdq\n\t"+car+" %ebx")
        else:
            #if car == "mod":
            #    f_salida.write("\n\tmovl %eax, %ebx;\n\tpopl %eax;")
            #else:
            f_salida.write("\n\tmovl %eax, %ebx\n\tpopl %eax\n\t"+car+" %ebx, %eax")

class nodoCallFun(Nodo):
    def escribir(self, ID):
        f_salida.write("\n\tcall " + ID + "\n\taddl $("+str(4*len(tabla[callID]))+"), %esp")


class nodoParams(Nodo):
    def escribir(self, params):
        for i in reversed(params):
            print(i)
            if i in tabla[functionID[0]]:
                f_salida.write("\n\tmovl "+ str(tabla[functionID[0]][i])+ "(%ebp), %eax\n\tpushl %eax")
            else:
                f_salida.write("\n\tmovl $("+str(i)+"), %eax\n\tpushl %eax")
                    

# NODOS PARA IFELSE
class NodoIFELSE(Nodo):
    def escribir(self, cad):
        global f_salida, numIF, etiqueta
        if cad == "IF":
            f_salida.write("\n\tcmpl $0, %eax\n\tje "+etiqueta + "\n\t# code for true:") # salta a la etiqueta true, si no saltará al final
        else:
            if cad == "ELSE":
                f_salida.write("\n\tcmpl $0, %eax\n\tje "+etiqueta)
                            

class NodoSalto(Nodo):
    def escribirSalto(self, cad):
        global f_salida
        f_salida.write("\n\tjmp "+cad)
    
    def escribirEtiqueta(self, cad):
        global f_salida
        f_salida.write("\n\n"+cad+":")


#   ┌──────────────────────────────────────────────────────────────────────────┐
#                                     Parser                      
#  └──────────────────────────────────────────────────────────────────────────┘
class ClassParser(Parser):
    tokens = ClassLexer.tokens

    def __init__(self):
        self.names = {}

    #---------------------------------------------------------------------------
	# Entradas y sentencias
    #---------------------------------------------------------------------------
    @_('sentencia entrada')
    def entrada(self, t):
        pass
    
    
    @_('functiondef entrada')
    def entrada(self, t):
        pass
    

    @_(' ')
    def entrada(self, t):
        pass


    @_('definicion ";"')
    def sentencia(self, t):
        pass


    @_('asignacion ";"')
    def sentencia(self, t):
        pass

        
    @_('operacion ";"')
    def sentencia(self, t):
        pass

    
    @_('sentenciaInFunc entradaInFunc')
    def entradaInFunc(self, t):
        pass        

    
    @_('funcionIf entradaInFunc')
    def entradaInFunc(self, t):
        pass
        

    @_('bucleWhile entradaInFunc')
    def entradaInFunc(self, t):
        pass


    @_('')
    def entradaInFunc(self, t):
        pass
        
        
    @_('sentencia')
    def sentenciaInFunc(self, t):
        pass



    @_('funcionIf')
    def sentenciaInFunc(self, t):
        pass


    @_('bucleWhile')
    def sentenciaInFunc(self, t):
        pass


    @_('funcioncall')
    def sentenciaInFunc(self, t):
        pass


    #---------------------------------------------------------------------------
	# Definiciones✓
    #---------------------------------------------------------------------------
    @_('tipo lista')
    def definicion(self, t):
        pass


    @_(' ')
    def definicion(self, t):
        pass


    @_("INT")
    def tipo(self, t):
        pass

    @_('elto resto')
    def lista(self, t):
        pass


    @_('ID')
    def elto(self, t):
        global inFunction, functionID
        if not(inFunction):
            tabla['global'].add(t.ID)
        else: 
            functionID[2] -= 4
            tabla[functionID[0]][t.ID] = functionID[2]
            nodo = NodoDefinicion() 
            nodo.escribir()             # subl $4, %ebp
        


    @_('ID emptyDef0 "=" operacion')
    def elto(self, t): 
        nodo = nodoAsignacion()
        nodo.escribir(t.ID)


    @_(' ')
    def emptyDef0(self, t):
        global inFunction, functionID
        if not(inFunction):
            tabla['global'].add(t[-1])
        else: 
            functionID[2] -= 4
            tabla[functionID[0]][t[-1]] = functionID[2]
            nodo = NodoDefinicion() 
            nodo.escribir()             # subl $4, %ebp
        

    @_('"," elto resto')
    def resto(self, t):
        pass


    @_(' ')
    def resto(self, t):
        pass


	#---------------------------------------------------------------------------
	# Operaciones de asignación
    #---------------------------------------------------------------------------
    @_('ID "=" operacion')
    def asignacion(self, t):
        nodo = nodoAsignacion()
        nodo.escribir(t.ID)


    @_('ID MASEQ operacion')
    def asignacion(self, t):
        tablaValor[t.ID] += t.operacion


    @_('ID MENOSEQ operacion')
    def asignacion(self, t):
        tablaValor[t.ID] -= t.operacion


    @_('ID POREQ operacion')
    def asignacion(self, t):          
        tablaValor[t.ID] *= t.operacion


    @_('ID DIVEQ operacion')
    def asignacion(self, t):
        tablaValor[t.ID] /= t.operacion


    @_('ID MODEQ operacion')
    def asignacion(self, t):
        tablaValor[t.ID] %= t.operacion


    #---------------------------------------------------------------------------
	# Operaciones aritméticas, relacionales y lógicas
    #---------------------------------------------------------------------------
    @_('operacion emptyPush OR bopand')
    def operacion(self, t):
        return (t.operacion or t.bopand)


    @_('bopand')
    def operacion(self, t):
        pass


    @_('bopand emptyPush AND bopeq')
    def bopand(self, t):
        return (t.bopand and t.bopeq)


    @_('bopeq')
    def bopand(self, t):
        pass


    @_('bopeq emptyPush EQ bopcomp')
    def bopeq(self, t):
        return (t.bopeq == t.bopcomp)


    @_('bopeq emptyPush NEQ bopcomp')
    def bopeq(self, t):
        return (t.bopeq != t.bopcomp)


    @_('bopcomp')
    def bopeq(self, t):
        pass

    @_('bopcomp emptyPush "<" exprar')
    def bopcomp(self, t):
        return (t.bopcomp < t.exprar)


    @_('bopcomp emptyPush LTEQ exprar')
    def bopcomp(self, t):
        return (t.bopcomp <= t.exprar)


    @_('bopcomp emptyPush ">" exprar')
    def bopcomp(self, t):
        return (t.bopcomp > t.exprar)


    @_('bopcomp emptyPush GTEQ exprar')
    def bopcomp(self, t):
        return (t.bopcomp >= t.exprar)


    @_('exprar')
    def bopcomp(self, t):
        pass


    @_('exprar emptyPush "+" exprprod')
    def exprar(self, t):
        nodo = NodoSumResProdDiv()
        nodo.escribir(car = 'addl')
    
    
    @_('exprar emptyPush "-" exprprod')
    def exprar(self, t):
        nodo = NodoSumResProdDiv()
        nodo.escribir(car = 'subl')
    

    @_('exprprod')
    def exprar(self, t):
        pass


    @_('exprprod emptyPush "*" uar')
    def exprprod(self, t):
        nodo = NodoSumResProdDiv()
        nodo.escribir(car = 'imull')

    
    @_('exprprod emptyPush "/" uar')
    def exprprod(self, t):
        nodo = NodoSumResProdDiv()
        nodo.escribir(car = 'idivl')

    
    @_('exprprod emptyPush "%" uar')
    def exprprod(self, t):
        return t.exprprod % t.uar

    
    @_('uar')
    def exprprod(self, t):
        pass

    
    @_('"-" brack')
    def uar(self, t):
        return -t.brack

    
    @_('"+" brack')
    def uar(self, t):
        return t.brack


    @_('"!" brack')
    def uar(self, t):
        return not t.brack

    
    @_('brack')
    def uar(self, t):
        pass


    @_('"(" operacion ")"')
    def brack(self, t):
        pass


    @_('NUM')
    def brack(self, t):
        nodo = NodoNum() 
        nodo.escribir(v = t.NUM)


    @_('ID')
    def brack(self, t):
        nodo = NodoID()
        nodo.escribir(ID = t.ID)

    @_('funcioncall')
    def brack(self, t):
        pass


    @_('')
    def emptyPush(self, t):
        nodo = NodoPush()
        nodo.escribir()
    

    #---------------------------------------------------------------------------
    # Functions
    #---------------------------------------------------------------------------
    @_('tipo ID emptyFunc0 "(" tiposInp ")" "{" entradaInFunc devolver "}"')
    def functiondef(self, t):   
        global inFunction
        nodo = NodoFuncion()
        nodo.escribirEpilogo()
        inFunction = False


    @_(' ')
    def emptyFunc0(self, t):
        global functionID, tabla, inFunction
        inFunction = True
        functionID = [t[-1], 4, 0] # functionID = ('name', pila_arriba, pila_abajo)
        tabla[functionID[0]] = {}
        nodo = NodoFuncion()
        nodo.escribirPrologo(n_funcion = functionID[0])


    @_('tipo ID emptyFunc1 tiposInpRe')
    def tiposInp(self, t):
        pass


    @_(' ')
    def emptyFunc1(self, t):
        global functionID, tabla
        functionID[1] += 4
        tabla[functionID[0]][t[-1]] = functionID[1]
        

    @_(' ')
    def tiposInp(self, t):
        pass


    @_('RETURN operacion ";"')
    def devolver(self, t):
        # no hay que hacer nada pq el resultado de la operacion se guarda 
        # en eax y devolvemos lo que se enceuntra en %eax con ret 
        pass

    
    @_('')
    def devolver(self, t):
        # no hay que hacer nada pq el resultado de la operacion se guarda 
        # en eax y devolvemos lo que se enceuntra en %eax con ret 
        pass 


    @_('"," tipo ID emptyFunc1 tiposInpRe')
    def tiposInpRe(self, t):
        pass


    @_('')
    def tiposInpRe(self, t):
        pass


    @_('ID emptyCall "(" paramlist ")"')
    def funcioncall(self, t):
        pass

    @_('')
    def emptyCall(self, t):
        global callID
        callID = t[-1]

        
    @_('PRINTF "(" STR restoF ")"')
    def funcioncall(self, t):
        pass


    @_('SCANF "(" STR "," "&" ID restoScan ")"')
    def funcioncall(self, t):
        pass


    @_('elm restoF')
    def paramlist(self, t):
        pass


    @_('')
    def paramlist(self, t):
        nodo = nodoCallFun()
        nodo.escribir(ID = callID)
        pass
    
    
    @_('ID')
    def elm(self, t):
        global listaparams
        listaparams.append(t.ID)



    @_('NUM')
    def elm(self, t):
        global listaparams
        listaparams.append(t.NUM)


    @_('"," elm restoF')
    def restoF(self, t):
        pass


    @_('')
    def restoF(self, t):
        global listaparams
        nodo = nodoParams()
        nodo.escribir(params = listaparams)
        nodo = nodoCallFun()
        nodo.escribir(ID = callID)

    

    @_('"," "&" ID restoScan')
    def restoScan(self, t):
        pass
    

    @_('')
    def restoScan(self, t):
        pass


    #---------------------------------------------------------------------------
	# If y While
    #---------------------------------------------------------------------------   
    
    @_('IF "(" operacion ")" emptyIF "{" entradaInFunc "}"')
    def funcionIf(self, t):
        nodo = NodoSalto()
        nodo.escribirEtiqueta(cad = "final"+str(numIF))


    @_('')
    def emptyIF(self, t):
        global numIF, etiqueta
        numIF += 1
        etiqueta = "final"+str(numIF)
        nodo = NodoIFELSE()
        nodo.escribir(cad = "IF")
        
    
    #@_('')
    #def emptyJUMP(self, t):
    #    global numIF
    #    nodo = NodoSalto()
    #    nodo.escribir(cad = "final"+numIF)

    

    @_('IF "(" operacion ")" emptyIFELSE "{" entradaInFunc "}" emptyFinal ELSE "{" entradaInFunc "}"')
    def funcionIf(self, t):
        nodo = NodoSalto()
        nodo.escribirEtiqueta(cad = "final"+str(numIF))


    @_('')
    def emptyFinal(self, t):
        global numIF, etiqueta
        etiqueta = "final"+str(numIF)
        nodo = NodoSalto()
        nodo.escribirSalto(cad = etiqueta)
        nodo.escribirEtiqueta(cad = "false"+str(numIF))

    
    @_('')
    def emptyIFELSE(self, t):
       global etiqueta, numIF
       numIF += 1
       etiqueta = "false"+str(numIF)
       nodo = NodoIFELSE()
       nodo.escribir(cad = "ELSE")
        


    # @_('IF "(" operacion ")" "{" entradaInFunc "}" ELSE sentenciaInFunc')
    # def funcionIf(self, t):
    #     pass


    # @_('IF "(" operacion ")" sentenciaInFunc')
    # def funcionIf(self, t):
    #     pass


    # @_('IF "(" operacion ")" sentenciaInFunc ELSE "{" entradaInFunc "}"')
    # def funcionIf(self, t):
    #     pass


    # @_('IF "(" operacion ")" sentenciaInFunc ELSE sentenciaInFunc')
    # def funcionIf(self, t):
    #     pass


    @_('WHILE "(" operacion ")" "{" entradaInFunc "}"')
    def bucleWhile(self, t):
        pass
        

    # @_('WHILE "(" operacion ")" sentenciaInFunc')
    # def bucleWhile(self, t):
    #     pass

#   ┌──────────────────────────────────────────────────────────────────────────┐
#                                       Main                      
#  └──────────────────────────────────────────────────────────────────────────┘

if __name__ == "__main__":

    lexer = ClassLexer()
    parser = ClassParser()

    f_entrada = open('prueba.c', 'r')
    f_salida = open('main.s', 'w') 
    
    text = f_entrada.read()
    f_entrada.close()

    parser.parse(lexer.tokenize(text))
    f_salida.close()
    print(tabla)
    print(listaparams)