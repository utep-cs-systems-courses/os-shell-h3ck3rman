import os
import sys
import re
from my_read_line import my_read_line

def out_redir(args):
    if '|' in args:
        args.remove('|')
    os.close(1)
    os.open(args[args.index('>') + 1], os.O_WRONLY | os.O_CREAT)
    os.set_inheritable(1,True)
    args.remove(args[args.index('>') + 1])
    args.remove('>')
    for dir in re.split(":",os.environ['PATH']):  #try each directory
        program = "%s/%s" % (dir, args[0])
        try:
            os.execve(program, args, os.environ) #try to execute program
        except FileNotFoundError:
            pass
    os.write(2, ("Command not found\n").encode())
    sys.exit(1)

def in_redir(args):
    if '|' in args:
        args.remove('|')
    os.close(0)
    os.open(args[args.index('<') + 1], os.O_RDONLY)
    os.set_inheritable(1,True)
    args.remove(args[args.index('<') + 1])
    args.remove('<')
    for dir in re.split(":",os.environ['PATH']):  #try each directory
        program = "%s/%s" % (dir, args[0])
        try:
            os.execve(program, args, os.environ) #try to execute program
        except FileNotFoundError:
            pass
    os.write(2, ("Command not found\n").encode())
    sys.exit(1)

def pipe(args):
    pid = os.getpid()
    import fileinput
    pr, pw = os.pipe()

    for f in (pr,pw):
        os.set_inheritable(f, True)
    print("pipe fds: pr=%d, pw=%d" % (pr, pw))
    print("About to fork (pid=%d)" % pid)

    rc = os.fork()

    if rc < 0:
        print("fork failed, returning %d\n" % rc, file = sys.stderr)
        sys.exit(1)

    elif rc == 0:
        print("Child: My pid==%d. Parent's pid=%d" % (os.getpid(), pid), file=sys.stderr)
        os.close(1)       #output redirect
        os.dup(pw)
        for fd in (pw, pr):
            os.close(fd)
        print("hello from child")

    else:
        print("Parent: My pid==%d. Child's pid=%d" % (os.getpid(), rc), file=sys.stderr)
        os.close(0)
        os.dup(pr)
        for fd in (pw, pr):
            os.close(fd)
        for line in fileinput.input():
            print("From child: <%s>" % line)
    print("Args before redirect: %s" % args)

    if '>' in args:
        out_redir(args)

    if '<' in args:
        in_redir(args)

    
while(1):
    os.write(1, "\n$ ".encode())
    
    input = my_read_line()

    if input.lower() == "exit" or len(input) == 0: #shell closes with 'exit' command
        os.write(2,"Exit from shell \n".encode())
        sys.exit(1)

    args = input.split() #tokenized user input
    
    curr_dir = os.getcwd()

    if args[0] == "pwd":
        os.write(2, (os.getcwd()).encode())
    
    elif args[0] == "cd":
        try:
            os.chdir(args[1])
            os.write(2, (os.getcwd()).encode())
            
        except FileNotFoundError:
            pass
            os.write(2, ("Error: File not found...").encode())
        
    else:
        rc = os.fork()       #forks a child process
    
        if rc < 0:
            os.write(2,("Fork failed %d\n" % rc).encode())
            sys.exit(1)

        elif rc == 0:
            if '|' in args:
                pipe(args)
            if '>' in args:
                out_redir(args)
            elif '<' in args:
                in_redir(args)
            else:
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
        
