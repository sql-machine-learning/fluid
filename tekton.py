# -*- coding: utf-8 -*-
'''This module tekton defines Python functions, each returns a Python
dictionary that represents a Tekton Resource.

'''

import inspect
import k8s


def task(func):
    '''Return a Task'''
    return obj(
        kind="Task",
        name=func.__name__,
        spec={
            "inputs": {
                "params": task_params(inspect.getfullargspec(func))
            }
        })


def task_run(func, args):
    '''Return a TaskRun'''
    return obj(
        kind="TaskRun",
        name=func.__name__ + "-run",
        spec={
            "taskRef": {
                "name": func.__name__
            },
            "inputs": {
                "params": task_run_params(inspect.getfullargspec(func), args)
            }
        })


def obj(kind, name, spec):
    '''Return a dict of Tekton object'''
    return {
        "apiVersion": "tekton.dev/v1alpha1",
        "kind": kind,
        "metadata": {
            "name": k8s.safe_name(name),
        },
        "spec": spec
    }


def task_params(argspec):
    '''Return a list of parameters for Task inputs'''
    _ps = []
    # NOTE: #(defaults)<=#(args).
    delta = len(argspec.args) - len(argspec.defaults)
    for i, arg in enumerate(argspec.args):
        _ps.append(task_param(
            arg,
            None if i < delta else argspec.defaults[i-delta]))
    return _ps


def task_param(arg_name, default_value):
    '''Return a param for Task inputs.'''
    _r = {
        "name": arg_name,
        "type": "string",   # NOTE: Python doesn't have type.
        "description": "",  # NOTE: Python cannot specify description.
    }
    if default_value is not None:
        _r["default"] = default_value
    return _r


def task_run_params(argspec, args):
    '''Return a list of parameters as TaskRun inputs'''
    _ps = []
    for i, arg in enumerate(args):
        _ps.append(task_run_param(argspec.args[i], arg))
    return _ps


def task_run_param(arg_name, arg_value):
    '''Return a param for TaskRun inputs.'''
    return {
        "name": arg_name,
        "value": arg_value
    }


def step(name, image, cmd, args):
    '''Return a step'''
    return {
        "name": name,
        "image": image,
        "command": cmd,
        "args": args
    }
