import os
import sys
import re
from my_read_line import my_read_line

pid = os.getpid()

while(1):
    os.write(1, "$ ".encode())
    
    input = my_read_line()

    if input.lower() == "exit" or len(input) == 0:
        os.write(2,"Exit From Shell \n".encode())
        sys.exit(1)

    lines = input.split()
    rc = os.fork()

    if rc < 0:
        os.write(2,("Fork Failed, Exit Executed %d\n" % rc).encode())
        sys.exit(1)

    elif rc == 0:
        for dir in re.split(":",os.environ['PATH']):
            program = "%s%s" % (dir, lines[0])
            try:
                os.execve(program, lines, os.environ)
            except FileNotFoundError:
                pass
        os.write(2, ("Command Fails\n").encode())
        sys.exit(1)
    else:
        os.write(1, ('parent pid = %d. child pid = %d\n' % (pid, rc)).encode())
        child_pid = os.wait()
        #os.write(1, ('child = %d terminated\n' % child_pid).encode())
