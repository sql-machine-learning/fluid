# -*- coding: utf-8 -*-
'''This module defines Fluid primitives for users to write Fluid
program.

'''

import inspect
import sys

import yaml

import tekton
import k8s


def dump_yaml(content):
    '''Pretty print a Python dictionary as a YAML'''
    print("---")
    yaml.dump(content, sys.stdout)


def task(func):
    '''Dump func as Task and returns a function to print TaskRun'''
    dump_yaml(tekton.task(func))

    def print_taskrun(*args):
        dump_yaml(tekton.task_run(func, args))

    return print_taskrun


def step(image, cmd, args):
    '''Define a step'''

    def step_name():
        '''step_name is only supposed to be called by step'''
        # See https://stackoverflow.com/a/6628348/724872.
        # frame 0 - step_name()
        # frame 1 - add_step()
        # frame 2 - fluid.step()
        caller_of_step = inspect.stack()[2]
        filename = caller_of_step[1]
        lineno = caller_of_step[2]
        return k8s.safe_name(f"{filename}-{lineno}")

    tekton.add_step(step_name(), image, cmd, args)
