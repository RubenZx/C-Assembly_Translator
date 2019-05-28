from sly import Lexer

tablaString = {}
IDstr = 0

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
        STR,
        RETURN
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
        "{",
        "}",
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


    NUM = r"[0-9]+"
    ID = r"[a-zA-Z_][a-zA-Z0-9_]*"
    STR = r'".*"'

    ID["int"] = INT

    # Special cases
    ID["if"] = IF
    ID["return"] = RETURN
    ID["else"] = ELSE
    ID["while"] = WHILE
    ID["printf"] = PRINTF
    ID["scanf"] = SCANF

    @_(r"[0-9]+")
    def NUM(self, t):
        t.value = int(t.value)
        return t
    
    @_(r'".*"')
    def STR(self, t):
        global IDstr
        t.value = t.value[1:-1] 
        try:
            tablaString[t.value] = IDstr
            IDstr += 1
        except Exception as e:
            pass
        return t


    @_(r"\n+")
    def ignore_newline(self, t):
        self.lineno += len(t.value)

    def error(self, t):
        print("illegal character: ", t.value[0])
        self.index += 1
