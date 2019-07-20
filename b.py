#! /usr/bin/python
#-----------------------------------------------------------------------
# robot_basic: a tool to support BASIC programming for GRBL based robot
#
#
#
#-----------------------------------------------------------------------

"""
forked from https://github.com/richpl/PyBasic

This class implements a BASIC interpreter that
presents a prompt to the user. The user may input
program statements, list them and run the program.
The program may also be saved to disk and loaded
again.
"""

from basictoken import BASICToken as Token
from lexer import Lexer
from program import Program
from sys import stderr
import sys

def readfile(filename):
    f = open(filename,'rb')
    fs = f.read()
    fs = fs.decode('utf-8')
    f.close()
    return fs

def main():
    banner = (
        """
        PPPP   Y   Y  BBBB    AAA    SSSS    I     CCC
        P   P   Y Y   B   B  A   A  S        I    C   
        P   P   Y Y   B   B  A   A  S        I    C
        PPPP     Y    BBBB   AAAAA  SSSS     I    C
        P        Y    B   B  A   A      S    I    C
        P        Y    B   B  A   A      S    I    C
        P        Y    BBBB   A   A  SSSS     I     CCC
        """)
    print(banner)

    lexer = Lexer()
    program = Program()

    # Continuously accept user input and act on it until
    # the user enters 'EXIT'
    while True:

        stmt = input('> ')
        #print('stmt:',stmt,len(stmt))
        
        try:
            tokenlist = lexer.tokenize(stmt)
            #print('tokenlist:',tokenlist)
            # Execute commands directly, otherwise
            # add program statements to the stored
            # BASIC program

            if len(tokenlist) > 0:

                # Exit the interpreter
                if tokenlist[0].category == Token.EXIT:
                    break

                # Add a new program statement, beginning
                # a line number
                elif tokenlist[0].category == Token.UNSIGNEDINT\
                     and len(tokenlist) > 1:
                    program.add_stmt(tokenlist)

                # Delete a statement from the program
                elif tokenlist[0].category == Token.UNSIGNEDINT \
                        and len(tokenlist) == 1:
                    program.delete_statement(int(tokenlist[0].lexeme))

                # Execute the program
                elif tokenlist[0].category == Token.RUN:
                    try:
                        program.execute()

                    except KeyboardInterrupt:
                        print("Program terminated")

                # List the program
                elif tokenlist[0].category == Token.LIST:
                    program.list()

                # Save the program to disk
                elif tokenlist[0].category == Token.SAVE:
                    program.save(tokenlist[1].lexeme)
                    print("Program written to file")

                # Load the program from disk
                elif tokenlist[0].category == Token.LOAD:
                    program.load(tokenlist[1].lexeme)
                    print("Program read from file")

                # Delete the program from memory
                elif tokenlist[0].category == Token.NEW:
                    program.delete()

                # Unrecognised input
                else:
                    print("Unrecognised input", file=stderr)
                    for token in tokenlist:
                        token.print_lexeme()
                    print(flush=True)

        # Trap all exceptions so that interpreter
        # keeps running
        except Exception as e:
            print(e, file=stderr, flush=True)


def main2(p):
    lexer = Lexer()
    program = Program()

    # Continuously accept user input and act on it until
    # the user enters 'EXIT'
    s2 = p.split('\n')
    s2.append('RUN')
    
    for s3 in s2:
        #stmt = s3.rstrip('\r\n').rstrip('\r').rstrip('\n')
        stmt = s3.rstrip('\r\n').rstrip('\r').rstrip('\n')
        #print('stmt:',stmt,len(stmt))
        try:
            tokenlist = lexer.tokenize(stmt)
            #print('tokenlist:',tokenlist)
            # Execute commands directly, otherwise
            # add program statements to the stored
            # BASIC program

            if len(tokenlist) > 0:

                # Exit the interpreter
                if tokenlist[0].category == Token.EXIT:
                    break

                # Add a new program statement, beginning
                # a line number
                elif tokenlist[0].category == Token.UNSIGNEDINT\
                     and len(tokenlist) > 1:
                    program.add_stmt(tokenlist)

                # Delete a statement from the program
                elif tokenlist[0].category == Token.UNSIGNEDINT \
                        and len(tokenlist) == 1:
                    program.delete_statement(int(tokenlist[0].lexeme))

                # Execute the program
                elif tokenlist[0].category == Token.RUN:
                    try:
                        program.execute()

                    except KeyboardInterrupt:
                        print("Program terminated")

                # List the program
                elif tokenlist[0].category == Token.LIST:
                    program.list()

                # Save the program to disk
                elif tokenlist[0].category == Token.SAVE:
                    program.save(tokenlist[1].lexeme)
                    print("Program written to file")

                # Load the program from disk
                elif tokenlist[0].category == Token.LOAD:
                    program.load(tokenlist[1].lexeme)
                    print("Program read from file")

                # Delete the program from memory
                elif tokenlist[0].category == Token.NEW:
                    program.delete()

                # Unrecognised input
                else:
                    print("Unrecognised input", file=stderr)
                    for token in tokenlist:
                        token.print_lexeme()
                    print(flush=True)

        # Trap all exceptions so that interpreter
        # keeps running
        except Exception as e:
            print(e, file=stderr, flush=True)            

            
if __name__ == "__main__":
    #print(len(sys.argv))
    if len(sys.argv) > 1:
        p = readfile(sys.argv[1])
        main2(p)
    else:
        main()