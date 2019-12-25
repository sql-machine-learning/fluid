#!/usr/bin/env python
import yaml
import re
import inspect
import sys


def tekton_obj(kind, name, spec):
    '''Returns a dict of Tekton object'''
    return {
        "apiVersion": "tekton.dev/v1alpha1",
        "kind": kind,
        "metadata": {
            "name": k8s_name(name),
        },
        "spec": spec
    }


def k8s_name(name):
    '''Replace "_", ".", "\", "/" in name by "-"'''
    _sub = re.sub(r"_|\.|\\|/", "-", name)
    return _sub.strip("-")


def dump_yaml(content):
    print("---")
    yaml.dump(content, sys.stdout)


def task(func):
    '''Dump func as Task and returns a function to print TaskRun'''
    dump_yaml(
        tekton_obj(
            kind="Task",
            name=func.__name__,
            spec={
                "inputs": {
                    "params": task_params(inspect.getfullargspec(func))
                }
            }))

    def print_taskrun(*args, **kwargs):
        dump_yaml(
            tekton_obj(
                kind="TaskRun",
                name=func.__name__ + "-run",
                spec={
                    "taskRef": {
                        "name": func.__name__
                    },
                    "inputs": {
                        "params": len(args) + len(kwargs)  # Complete this.
                    }
                }))
    return print_taskrun


def task_params(argspec):
    '''Return a list of parameters'''
    _ps = []
    for arg in argspec.args:
        _ps.append(task_param(arg))
    return _ps


def task_param(argspec_arg):
    '''Return a Tekton parameter.'''
    return {
        "name": argspec_arg,
        "type": "string",       # Need to derive type.
        "description": "",  # Need to derive description.
        "default": "",  # Need to derive default value.
    }


STEPS = []  # For holding steps of a Task.


def step(image, cmd, args):
    '''Append a step to global variable STEPS'''

    def step_name():
        '''step_name is only supposed to be called by step'''
        # See https://stackoverflow.com/a/6628348/724872.
        caller_of_step = inspect.stack()[2]
        filename = caller_of_step[1]
        lineno = caller_of_step[2]
        return k8s_name(f"{filename}-{lineno}")

    global STEPS
    STEPS.append({
        "name": step_name(),
        "image": image,
        "command": cmd,
        "args": args
    })


@task
def echo_hello_world(hello, world="世界"):
    '''Defines an example Tekton Task'''
    step(image="ubuntu", cmd=["echo"], args=[hello])
    step(image="ubuntu", cmd=["echo"], args=[world])


if __name__ == "__main__":
    echo_hello_world("你好")
