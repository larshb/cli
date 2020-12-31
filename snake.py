#!/usr/bin/env python3

from ansi import \
    say, sgr, SGR_INCREASE, SGR_FG_GREEN, SGR_FG_RED, NONE, show_cursor
from time import sleep
from random import choice


SOL = '\b' * 1000  # Start Of Line (TODO: Handle multiline flushes)


class Snake:

    BODY = "⠇⠋⠉⠙⠸⠴⠤⠦"
    FORMAT = sgr(SGR_INCREASE, SGR_FG_GREEN)
    FAILURE = sgr(SGR_INCREASE, SGR_FG_RED) + '✗' + NONE
    SUCCESS = sgr(SGR_INCREASE, SGR_FG_GREEN) + '✓' + NONE

    def __init__(self, message, rate=0.1):
        self.message = message
        self.rate = rate
        self.index = 0

    def __str__(self):
        s = self.FORMAT + self.BODY[self.index]
        self.index = (self.index + 1) % len(self.BODY)
        return s

    def output_message(self):
        say('  ' + self.message)
        return self

    def tick(self):
        say(SOL + str(self))
        sleep(self.rate)

    def succeed(self):
        say(SOL + self.SUCCESS)

    def fail(self):
        say(SOL + self.FAILURE)

    def countdown(self, ticks):
        self.output_message()
        try:
            for _ in range(ticks):
                self.tick()
        finally:
            say(SOL + self.SUCCESS + NONE + '\n')

    def system(self, call):
        
        from threading import Thread
        from queue import Queue

        queue = Queue()
        self.output_message()

        def worker(call):
            from os import system
            exit_code = system(call)
            queue.put(exit_code)
            queue.task_done()

        Thread(target=worker, daemon=True, args=(call,)).start()
        while queue.empty():
            self.tick()

        exit_code = queue.get()
        if exit_code:
            self.fail()
        else:
            self.succeed()

        say('\n')
        show_cursor(True)
        return exit_code


class Demo:

    def finish(self, *args):
        say(NONE)
        show_cursor(True)
        exit(0)

    def demo(self):
        from loading import messages
        try:
            show_cursor(False)
            while True:
                message = choice(messages)
                Snake(message).countdown(16)
        except:
            pass
        finally:
            self.finish()


def main(argv):
    if len(argv) < 2:
        print(f"Usage: ")
        print(f"- {argv[0]} demo")
        print(f"- {argv[0]} <message> <call>")
        return 1

    from signal import signal, SIGINT, SIGTERM
    signal(SIGINT, Demo.finish)
    signal(SIGTERM, Demo.finish)

    if argv[-1] == 'demo':
        Demo().demo()
    else:
        message = argv[1]
        call = ' '.join(argv[2:])
        show_cursor(False)
        Snake(message).system(call)
        show_cursor(True)


if __name__ == '__main__':
    from sys import argv
    main(argv)
