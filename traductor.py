from sly import Lexer, Parser


class ClassLexer(Lexer):

    # Tokenlist
    tokens = {
        ID,
        OR,
        AND,
        INT,
        NUM,
        IF,
        ELSE,
        WHILE,
        PRINTF,
        SCANF,
        EQ,
        NEQ,
        GTEQ,
        LTEQ,
		MASEQ,
		MENOSEQ,
		POREQ,
		DIVEQ,
		MODEQ,
        PP,
        MM,
        STR,
    }

    # Ignores and literals
    ignore = " \t"
    ignore_comment = r"\/\/.*"
    # ignore_newline = r'\n+'
    literals = {
        "*",
        "+",
        "-",
        "/",
        ",",
        ";",
        "[",
        "]",
        "(",
        ")",
        "!",
        "=",
        ">",
        "<",
        "%",
        "\""
    }

    OR = r"\|\|"
    AND = r"&&"
    EQ = r"=="
    NEQ = r"!="
    GTEQ = r">="
    LTEQ = r"<="
    MASEQ = r"\+="
    MENOSEQ = r"-="
    POREQ = r"\*="
    DIVEQ = r"/="
    MODEQ = r"%="
    # PP = r"\+\+"
    # MM = r'--'


    NUM = r"[0-9]+"
    ID = r"[a-zA-Z_][a-zA-Z0-9_]*"
    STR = r"\"[.]+\""

    ID["int"] = INT

    # Special cases
    ID["if"] = IF
    ID["return"] = IF
    ID["else"] = ELSE
    ID["while"] = WHILE
    ID["printf"] = PRINTF
    ID["scanf"] = SCANF

    @_(r"[0-9]+")
    def NUM(self, t):
        t.value = int(t.value)
        return t

    @_(r"\n+")
    def ignore_newline(self, t):
        self.lineno += len(t.value)

    def error(self, t):
        print("illegal character: ", t.value[0])
        self.index += 1


# LEXER END

global tablaAsig, tablaValor

class Nodo:
    def escribir(self):
        pass


class NodoInt(Nodo):
    def escribir(self):
        return "int"



class ClassParser(Parser):
    tokens = ClassLexer.tokens

    def __init__(self):
        self.names = {}

    @_('sentencia ";" entrada')
    def entrada(self, t):
        pass

    @_(" ")
    def entrada(self, t):
        pass


    #---------------------------------------------------------------------------
	# Definiciones
    #---------------------------------------------------------------------------

    @_('definicion')
    def sentencia(self, t):
        pass

    @_('tipo lista')
    def definicion(self, t):
        return t.tipo

    @_("INT")
    def tipo(self, t):
        return NodoInt()

    @_('empty1 elto empty2 resto')
    def lista(self, t):
        return t[-1]

    @_("")
    def empty1(self, t):
        return t[-1]

    @_("")
    def empty2(self, t):
        return t[-2]

    @_('ID')
    def elto(self, t):
        tablaAsig[t.ID] = t[-2].escribir()

    @_('ID "=" operacion')
    def elto(self, t):
        tablaAsig[t.ID] = t[-4].escribir()
        tablaValor[t.ID] =  t.operacion

    @_('"," empty3 elto empty4 resto')
    def resto(self, t):
        pass

    @_("")
    def empty3(self, t):
        return t[-4]

    @_("")
    def empty4(self, t):
        return t[-3]

    @_("")
    def resto(self, t):
        pass



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
        return t.NUM

    @_('ID')
    def brack(self, t):
        return tablaValor[t.ID]    

	#---------------------------------------------------------------------------
	# Operaciones de asignación
    #---------------------------------------------------------------------------
    @_('asignacion')
    def sentencia(self, t):
        pass

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
    # Functions
    #---------------------------------------------------------------------------
    # @_('ID "(" paramlist ")"')
    # def funcion(self, t):
    #     
    #     pass
    
    # @_('PRINTF "(" STR restoF ")"')
    # def funcion(self, t):
    #     pass
    
    # @_('SCANF "(" STR restoS ")"')
    # def funcion(self, t):
    #     pass
    
    # @_('elm restoF')
    # def paramlist(self, t):
    #     pass
    
    # @_(' ')
    # def paramlist(self, t):
    #     pass

    # @_('ID')
    # def elm(self, t):
    #     pass

    # @_('NUM')
    # def elm(self, t):
    #     pass
    
    # @_('operacion')
    # def elm(self, t):
    #     pass

    # @_('declaracion')   ESTO PQ PQ?? PQQQQQ??? PQPQPQPQPQPQPQxaljsdjqsBDLÑKma
    # def elm(self, t):
    #     pass

    # @_('"," elm restoF')
    # def restoF(self, t):
    #     pass

    # @_(' ')
    # def restoF(self, t):
    #     pass

    # @_('"," "&" ID restoS')
    # def restoS(self, t):
    #     pass

    # @_('"," "&" ID')
    # def restoS(self, t):
    #     pass


    #---------------------------------------------------------------------------
    
# PARSER END

if __name__ == "__main__":
    global tablaAsig, tablaValor

    lexer = ClassLexer()
    parser = ClassParser()

    tablaAsig = {}
    tablaValor = {}
    # while True:

    text = input("data type list > ")
    parser.parse(lexer.tokenize(text))
    print(tablaAsig)
    print(tablaValor)
