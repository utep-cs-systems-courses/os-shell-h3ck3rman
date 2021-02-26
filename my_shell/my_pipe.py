import os
import sys
import re

def pipe(args):
    left = args[:args.index('|')]
    right = args[args.index('|')+1:]

    pr, pw = os.pipe()  # pipe read, pipe write

    rc = os.fork()

    if rc < 0:  # fork failed
        os.write(2, ('fork failed, exiting shell %d\n' % rc).encode())
        sys.exit(1)  # exited with error, unsuccessful termination

    elif rc == 0:
        os.close(1)  # close output fd
        os.dup(pw)  # duplicate pipe write fd
        os.set_inheritable(1, True)  # accessibility

        for fd in (pr, pw):  # pr to pw
            os.close(fd)    # close fd

        execute_cmd(left)
        os.write(2, ('%s: could not execute\n' % args[0]).endcode())
        sys.exit(1)

    else:
        os.close(0)  # keyboard
        os.dup(pr)  # duplicate pipe read fd
        os.set_inheritable(0, True)

        for fd in (pr, pw):  # pr to pw
            os.close(fd)    # close fd

        if '|' in right:
            pipe(right)  # pipe recursively

        execute_cmd(right)
        os.write(2, ('%s: could not execute\n' % args[0]).endcode())
        sys.exit(1)

def execute_cmd(args):
    for dir in re.split(':', os.environ['PATH']):
        program='%s/%s' % (dir, args[0])

        try:
            os.execve(program, args, os.environ)
        except FileNotFoundError:
            pass                                    # fail quietly
    os.write(2, ('%s: command not found\n' % args[0]).endcode())
    sys.exit(1)
