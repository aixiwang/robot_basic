#! /usr/bin/python

"""Class to represent a token for the BASIC
programming language. A token consists of
three items:

column      Column in which token starts
category    Category of the token
lexeme      Token in string form

"""


class BASICToken:

        """BASICToken categories"""

        EOF             = 0   # End of file
        LET             = 1   # LET keyword
        LIST            = 2   # LIST command
        PRINT           = 3   # PRINT command
        RUN             = 4   # RUN command
        FOR             = 5   # FOR keyword
        NEXT            = 6   # NEXT keyword
        IF              = 7   # IF keyword
        THEN            = 8   # THEN keyword
        ELSE            = 9   # ELSE keyword
        ASSIGNOP        = 10  # '='
        LEFTPAREN       = 11  # '('
        RIGHTPAREN      = 12  # ')'
        PLUS            = 13  # '+'
        MINUS           = 14  # '-'
        TIMES           = 15  # '*'
        DIVIDE          = 16  # '/'
        NEWLINE         = 17  # End of line
        UNSIGNEDINT     = 18  # Integer
        NAME            = 19  # Identifier that is not a keyword
        EXIT            = 20  # Used to quit the interpreter
        DIM             = 21  # DIM keyword
        GREATER         = 22  # '>'
        LESSER          = 23  # '<'
        STEP            = 24  # STEP keyword
        GOTO            = 25  # GOTO keyword
        GOSUB           = 26  # GOSUB keyword
        INPUT           = 27  # INPUT keyword
        REM             = 28  # REM keyword
        RETURN          = 29  # RETURN keyword
        SAVE            = 30  # SAVE command
        LOAD            = 31  # LOAD command
        NOTEQUAL        = 32  # '<>'
        LESSEQUAL       = 33  # '<='
        GREATEQUAL      = 34  # '>='
        UNSIGNEDFLOAT   = 35  # Floating point number
        STRING          = 36  # String values
        TO              = 37  # TO keyword
        NEW             = 38  # NEW command
        EQUAL           = 39  # '='
        COMMA           = 40  # ','
        STOP            = 41  # STOP keyword
        COLON           = 42  # ':'
        ON              = 43  # ON keyword
        POW             = 44  # Power function
        SQR             = 45  # Square root function
        ABS             = 46  # Absolute value function
        DIM             = 47  # DIM keyword
        RANDOMIZE       = 48  # RANDOMIZE keyword
        RND             = 49  # RND keyword
        ATN             = 50  # Arctangent function
        COS             = 51  # Cosine function
        EXP             = 52  # Exponential function
        LOG             = 53  # Natural logarithm function
        SIN             = 54  # Sine function
        TAN             = 55  # Tangent function
        DATA            = 56  # DATA keyword
        READ            = 57  # READ keyword
        
        CHECKONLINE     = 58  # added for motion
        CLOSELOCNOTI    = 59
        STOPALL         = 60
        STOPALLE        = 61
        GETPARAM        = 62
        SETPARAM        = 63
        CLRLOC          = 64
        GETAXISSTS      = 65
        MOVE            = 66
        MOVEREL         = 67
        MOVERELPRE      = 68
        MOVERELMULTI    = 69
        SLP           = 70
        GETLOC          = 71
        

        # Displayable names for each token category
        catnames = ['EOF', 'LET', 'LIST', 'PRINT', 'RUN',
        'FOR', 'NEXT', 'IF', 'THEN', 'ELSE', 'ASSIGNOP',
        'LEFTPAREN', 'RIGHTPAREN', 'PLUS', 'MINUS', 'TIMES',
        'DIVIDE', 'NEWLINE', 'UNSIGNEDINT', 'NAME', 'EXIT',
        'DIM', 'GREATER', 'LESSER', 'STEP', 'GOTO', 'GOSUB',
        'INPUT', 'REM', 'RETURN', 'SAVE', 'LOAD',
        'NOTEQUAL', 'LESSEQUAL', 'GREATEQUAL',
        'UNSIGNEDFLOAT', 'STRING', 'TO', 'NEW', 'EQUAL',
        'COMMA', 'STOP', 'COLON', 'ON', 'POW', 'SQR', 'ABS',
        'DIM', 'RANDOMIZE', 'RND', 'ATN', 'COS', 'EXP',
        'LOG', 'SIN', 'TAN', 'DATA', 'READ','MINIT',
        'CHECKONLINE','CLOSELOCNOTI','STOPALL','STOPALLE','GETPARAM','SETPARAM','CLRLOC','GETAXISSTS',
        'MOVE','MOVEREL','MOVERELPRE','MOVERELMULTI','SLP','GETLOC']

        smalltokens = {'=': ASSIGNOP, '(': LEFTPAREN, ')': RIGHTPAREN,
                       '+': PLUS, '-': MINUS, '*': TIMES, '/': DIVIDE,
                       '\n': NEWLINE, '<': LESSER,
                       '>': GREATER, '<>': NOTEQUAL,
                       '<=': LESSEQUAL, '>=': GREATEQUAL, ',': COMMA,
                       ':': COLON}

        # Dictionary of BASIC reserved words
        keywords = {'LET': LET, 'LIST': LIST, 'PRINT': PRINT,
                    'FOR': FOR, 'RUN': RUN, 'NEXT': NEXT,
                    'IF': IF, 'THEN': THEN, 'ELSE': ELSE,
                    'EXIT': EXIT, 'DIM': DIM, 'STEP': STEP,
                    'GOTO': GOTO, 'GOSUB': GOSUB,
                    'INPUT': INPUT, 'REM': REM, 'RETURN': RETURN,
                    'SAVE': SAVE, 'LOAD': LOAD, 'NEW': NEW,
                    'STOP': STOP, 'TO': TO, 'ON':ON, 'POW': POW,
                    'SQR': SQR, 'ABS': ABS,
                    'RANDOMIZE': RANDOMIZE, 'RND': RND,
                    'ATN': ATN, 'COS': COS, 'EXP': EXP,
                    'LOG': LOG, 'SIN': SIN, 'TAN': TAN,
                    'DATA': DATA, 'READ': READ,
                    'CHECKONLINE':CHECKONLINE,
                    'CLOSELOCNOTI':CLOSELOCNOTI,
                    'STOPALL':STOPALL,
                    'STOPALLE':STOPALLE,
                    'GETPARAM':GETPARAM,
                    'SETPARAM':SETPARAM,
                    'CLRLOC':CLRLOC,
                    'GETAXISSTS':GETAXISSTS,
                    'MOVE':MOVE,
                    'MOVEREL':MOVEREL,
                    'MOVERELPRE':MOVERELPRE,
                    'MOVERELMULTI':MOVERELMULTI,
                    'SLP':SLP,
                    'GETLOC':GETLOC}

        # Functions
        functions = {ABS, ATN, COS, EXP, LOG, POW, RND, SIN, SQR, TAN, 
                     CHECKONLINE,CLOSELOCNOTI,STOPALL,STOPALLE,GETPARAM,SETPARAM,CLRLOC,GETAXISSTS,
                     MOVE,MOVEREL,MOVERELPRE,MOVERELMULTI,SLP,GETLOC}

        def __init__(self, column, category, lexeme):

            self.column = column      # Column in which token starts
            self.category = category  # Category of the token
            self.lexeme = lexeme      # Token in string form

        def pretty_print(self):
            """Pretty prints the token

            """
            print('Column:', self.column,
                  'Category:', self.catnames[self.category],
                  'Lexeme:', self.lexeme)

        def print_lexeme(self):
            print(self.lexeme, end=' ')

