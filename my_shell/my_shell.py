import os
import sys
import re
from my_read_line import my_read_line

while(1):
    os.write(1, "$ ".encode())
    
    input = my_read_line()

    if input.lower() == "exit" or len(input) == 0: #shell closes with 'exit' command
        os.write(2,"Exit from shell \n".encode())
        sys.exit(1)

    args = input.split() #tokenized user input
    rc = os.fork()       #forks a child process

    if rc < 0:
        os.write(2,("Fork failed %d\n" % rc).encode())
        sys.exit(1)

    elif rc == 0: 
        for dir in re.split(":",os.environ['PATH']):  #try each directory
            program = "%s/%s" % (dir, args[0])
            try:
                os.execve(program, args, os.environ) #try to execute program
            except FileNotFoundError:
                pass
        os.write(2, ("Command not found\n").encode())
        sys.exit(1)
    else:
        child_pid = os.wait() #waiting for child to finish
        
