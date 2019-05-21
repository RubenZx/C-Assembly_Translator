from sly import Lexer, Parser
from lexico import ClassLexer


tabla = {}          # tabla con los valores del main: funciones: global:
functionID = None   # tuple para el nombre de la función y el estado de la pila
inFunction = False  # Variable para saber si estamos en una función o no

#   ┌──────────────────────────────────────────────────────────────────────────┐
#                                     Nodos                      
#  └──────────────────────────────────────────────────────────────────────────┘

class Nodo:
    def escribir(self):
        pass


class NodoInt(Nodo):
    def escribir(self):
        return "int"


class NodoFuncion(Nodo):
    def escribirPrologo(self, ID, args):
        global f_salida
        f_salida.write(".text\n.globl ", ID, "\n.type ", ID, ", @function\n", ID, ":\n\tpushl %ebp\n\tmovl %esp, %ebp\n\tsubl ")


class NodoNum(Nodo):
    v = None
    def __init__(self, valor):
        self.v = valor              # le pasamos el valor del dígito
    def escribir(self):
        f_salida.write("movl $(",self.v,"), %eax")        


class NodoPush(Nodo):
    def escribir(self):
        f_salida.write("pushl %eax;\n")


class NodoSumResProdDiv(Nodo):
    car = None
    def __init__(self, valor):
        self.car = valor            # car toma el valor de addl, subl, imull, idivl
    def escribir(self):
        if car == "idivl":
            f_salida.write("\tmovl %eax, %ebx;\n\tpopl %eax;\n\tcdq;\n\t"+car+" %ebx;\n")
        else:
            f_salida.write("\tmovl %eax, %ebx;\n\tpopl %eax;\n\t"+car+" %ebx, %eax;\n")


class NodoID(Nodo):
    v = None
    def __init__(self, valor):
        self.v = valor
    def escribir(self):
        f_salida.write("movl ")

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


    @_('aginacion ";"')
    def sentencia(self, t):
        pass

        
    @_('operacion ";"')
    def sentencia(self, t):
        pass

    
    @_('sentenciaInFunc entradaInFunc')
    def entradaInFunc(self, t):
        pass

    
    @_('functionIf entradaInFunc')
    def entradaInFunc(self, t):
        pass
        

    @_('bucleWhile entradaInFunc')
    def entradaInFunc(self, t):
        pass


    @_(' ')
    def entradaInFunc(self, t):
        pass
        
        
    @_('sentencia')
    def sentenciaInFunc(self, t):
        pass


    @_('funcionIf')
    def sentenciaInFunc(self, t):
        pass


    @_('funcionWhile')
    def sentenciaInFunc(self, t):
        pass


    #---------------------------------------------------------------------------
	# Definiciones
    #---------------------------------------------------------------------------
    @_('tipo lista')
    def definicion(self, t):
        pass


    @_(' ')
    def definicion(self, t):
        pass


    @_("INT")
    def tipo(self, t):
        return NodoInt()


    @_('elto resto')
    def lista(self, t):
        pass


    @_('ID')
    def elto(self, t):
        global inFunction
        if not(inFunction):
            tabla['global'].add(t.value)
        else: 
            tabla[FunctionID[]]
            # por implementar


    @_('ID "=" operacion')
    def elto(self, t):        
        pass


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
        tablaValor[t.ID] = t.operacion


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
    @_('operacion OR bopand')
    def operacion(self, t):
        return (t.operacion or t.bopand)


    @_('bopand')
    def operacion(self, t):
        return t.bopand


    @_('bopand AND bopeq')
    def bopand(self, t):
        return (t.bopand and t.bopeq)


    @_('bopeq')
    def bopand(self, t):
        return t.bopeq


    @_('bopeq EQ bopcomp')
    def bopeq(self, t):
        return (t.bopeq == t.bopcomp)


    @_('bopeq NEQ bopcomp')
    def bopeq(self, t):
        return (t.bopeq != t.bopcomp)


    @_('bopcomp')
    def bopeq(self, t):
        return t.bopcomp


    @_('bopcomp "<" exprar')
    def bopcomp(self, t):
        return (t.bopcomp < t.exprar)


    @_('bopcomp LTEQ exprar')
    def bopcomp(self, t):
        return (t.bopcomp <= t.exprar)


    @_('bopcomp ">" exprar')
    def bopcomp(self, t):
        return (t.bopcomp > t.exprar)


    @_('bopcomp GTEQ exprar')
    def bopcomp(self, t):
        return (t.bopcomp >= t.exprar)


    @_('exprar')
    def bopcomp(self, t):
        return t.exprar
    

    @_('exprar "+" exprprod')
    def exprar(self, t):
        return t.exprar + t.exprprod
    
    
    @_('exprar "-" exprprod')
    def exprar(self, t):
        return t.exprar - t.exprprod
    

    @_('exprprod')
    def exprar(self, t):
        return t.exprprod


    @_('exprprod "*" uar')
    def exprprod(self, t):
        nodo = nodoProd()
        return t.exprprod * t.uar

    
    @_('exprprod "/" uar')
    def exprprod(self, t):
        return t.exprprod / t.uar

    
    @_('exprprod "%" uar')
    def exprprod(self, t):
        return t.exprprod % t.uar

    
    @_('uar')
    def exprprod(self, t):
        return t.uar

    
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
        return t.brack


    @_('"(" operacion ")"')
    def brack(self, t):
        return t.operacion


    @_('NUM')
    def brack(self, t):
        nodo = NodoNum(t.value)
        nodo.escribir()


    @_('ID')
    def brack(self, t):
        return tablaValor[t.ID]    


    #---------------------------------------------------------------------------
    # Functions
    #---------------------------------------------------------------------------
    @_('tipo ID emptyFunc0 "(" tiposInp ")" "{" entradaInFunc "}"')
    def functiondef(self, t): 
        pass
    

    @_(' ')
    def emptyFunc0(self, t):
        global functionID, tabla, inFunction
        inFunction = True
        functionID = (t[-1], 4, 0) # functionID = ('name', pila_arriba, pila_abajo)
        tabla[functionID[0]] = {}


    @_('tipo ID emptyFunc1 tiposInpRe')
    def tiposInp(self, t):
        pass


    @_(' ')
    def emptyFunc1(self, t):
        global functionID, tabla
        funtionID[1] += 4
        tabla[functionID[0]][t[-1]] = functionID[1]
        # return t[-1]
        

    @_(' ')
    def tiposInp(self, t):
        pass


    @_('RETURN operacion')
    def devolver(self, t):
        global inFunction
        inFunction = False # SIN TERMINAR


    @_('"," tipo ID emptyFunc2 tiposInpRe')
    def tiposInpRe(self, t):
        # global functionID, tabla
        # funtionID[1] += 4
        # tabla[functionID[0]][t.ID] = functionID[1]
        pass


    @_(' ')
    def emptyFunc2(self, t):
        global functionID, tabla
        funtionID[1] += 4
        tabla[functionID[0]][t[-1]] = functionID[1]
        # return t[-1]


    @_('')
    def tiposInpRe(self, t):
        pass


    @_('ID "(" paramlist ")"')
    def funcioncall(self, t):
        pass


    @_('PRINTF "(" STR restoF ")"')
    def funcioncall(self, t):
        pass


    @_('SCANF "(" STR "," "&" ID restoScan ")"')
    def funcioncall(self, t):
        pass


    @_('elm restoF')
    def paramlist(self, t):
        pass


    @_(' ')
    def paramlist(self, t):
        pass
    
    
    @_('ID')
    def elm(self, t):
        pass


    @_('NUM')
    def elm(self, t):
        pass
        

    @_('operacion')
    def elm(self, t):
        pass


    @_('"," elm restoF')
    def restoF(self, t):
        pass


    @_('')
    def restoF(self, t):
        pass
    

    @_('"," "&" ID restoScan')
    def restoScan(self, t):
        pass
    

    @_('')
    def restoScan(self, t):
        pass


    #---------------------------------------------------------------------------
	# If y While
    #---------------------------------------------------------------------------
    @_('IF "(" operacion ")" "{" entradaInFunc "}"')
    def funcionIf(self, t):
        pass


    @_('IF "(" operacion ")" "{" entradaInFunc "}" ELSE "{" entradaInFunc "}"')
    def funcionIf(self, t):
        pass


    @_('IF "(" operacion ")" "{" entradaInFunc "}" ELSE sentenciaInFunc')
    def funcionIf(self, t):
        pass


    @_('IF "(" operacion ")" sentenciaInFunc')
    def funcionIf(self, t):
        pass


    @_('IF "(" operacion ")" sentenciaInFunc ELSE "{" entradaInFunc "}"')
    def funcionIf(self, t):
        pass


    @_('IF "(" operacion ")" sentenciaInFunc ELSE sentenciaInFunc')
    def funcionIf(self, t):
        pass


    @_('WHILE "(" operacion ")" "{" entradaInFunc "}"')
    def bucleWhile(self, t):
        pass
        

    @_('WHILE "(" operacion ")" sentenciaInFunc')
    def bucleWhile(self, t):
        pass

#   ┌──────────────────────────────────────────────────────────────────────────┐
#                                       Main                      
#  └──────────────────────────────────────────────────────────────────────────┘

if __name__ == "__main__":

    lexer = ClassLexer()
    parser = ClassParser()

    f_entrada = open('main.c', 'r')
    f_salida = open('main.s', 'x') 

    tablaAsig = {}
    tablaValor = {}
    # while True:

    text = input("data type list > ")
    parser.parse(lexer.tokenize(text))
    print(tablaAsig)
    print(tablaValor)
