# -*- coding: utf-8 -*-
'''This module tekton defines Python functions, each returns a Python
dictionary that represents a Tekton Resource.

'''

import inspect
import k8s


def task(func):
    '''Return a Task'''
    argspec = inspect.getfullargspec(func)
    input_resources, output_resources = task_resources(argspec)
    params = task_params(argspec)
    return _obj(
        kind="Task",
        name=k8s.safe_name(func.__name__),
        spec={
            "inputs": {
                "params": params,
                "resources": input_resources,
            },
            "outputs": {
                "resources": output_resources,
            },
            "steps": task_steps(func)
        })


def task_params(argspec):
    '''Return a list of parameters for Task inputs'''
    _ps = []
    # NOTE: #(defaults)<=#(args).
    num_args = 0 if argspec.args is None else len(argspec.args)
    num_defaults = 0 if argspec.defaults is None else len(argspec.defaults)
    first_default = num_args - num_defaults
    for i, arg in enumerate(argspec.args):
        if argspec.annotations.get(arg) is None:  # is param
            _ps.append(task_param(
                arg,
                None if i < first_default else argspec.defaults[i-first_default]))
    return _ps


def task_param(arg_name, default_value):
    '''Return a param for Task inputs.'''
    _r = {
        "name": k8s.safe_name(arg_name),
        "type": "string",   # NOTE: Python doesn't have type.
    }
    if default_value is not None:
        _r["default"] = default_value
    return _r


def task_resources(argspec):
    '''Return a list of resources as Task's inputs'''
    input_resources = []
    output_resources = []
    for arg in argspec.args:
        _io, _typ, _is = _is_arg_resource(argspec, arg)
        if _is:
            if _io == "input":
                input_resources.append(task_resource(arg, _typ))
            else:
                output_resources.append(task_resource(arg, _typ))
    return input_resources, output_resources


def _is_arg_resource(argspec, arg):
    anno = argspec.annotations.get(arg)
    _io, _typ = "", ""
    if anno is not None:
        _ri = anno.split(",")
        _io = _ri[0]
        _typ = _ri[1]
    return _io, _typ, anno is not None


def task_resource(name, typ):
    '''Return a resource for using in inputs|outputs.resources of a Task'''
    return {
        "name": k8s.safe_name(name),
        "type": typ
    }


def task_run(func, args):
    '''Return a TaskRun'''
    return _obj(
        kind="TaskRun",
        name=k8s.safe_name(func.__name__ + "-run"),
        spec={
            "taskRef": {
                "name": k8s.safe_name(func.__name__)
            },
            "inputs": {
                "params": task_run_params(inspect.getfullargspec(func), args)
            }
        })


def _obj(kind, name, spec):
    '''Return a dict of Tekton object'''
    return {
        "apiVersion": "tekton.dev/v1alpha1",
        "kind": kind,
        "metadata": {
            "name": k8s.safe_name(name),
        },
        "spec": spec
    }


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


class FakeGitResource:
    '''Used in dry-run a Task  function, which might call res_param.revision'''

    def __init__(self, io, arg):
        self.url = f"$({io}.resources.{k8s.safe_name(arg)}.url)"
        self.revision = f"$({io}.resources.{k8s.safe_name(arg)}.revision)"


class FakeImageResource:
    '''Used in dry-run a Task  function, which might call res_param.url'''

    def __init__(self, io, arg):
        self.url = f"$({io}.resources.{k8s.safe_name(arg)}.url)"


def _fake_resource(io, typ, arg):
    return FakeGitResource(io, arg) if typ == "git" else FakeImageResource(io, arg)


STEPS = []  # For holding steps of a Task.


def task_steps(func):
    '''Call func with fake parameters to trace STEPS'''
    argspec = inspect.getfullargspec(func)
    fake_args = []
    for arg in argspec.args:
        _io, _typ, _is = _is_arg_resource(argspec, arg)
        if _is:
            fake_args.append(_fake_resource(_typ, arg))
        else:
            fake_args.append(f"$(inputs.params.{k8s.safe_name(arg)})")

    global STEPS
    STEPS = []
    func(*fake_args)
    return STEPS


def add_step(name, image, cmd, args, env):
    '''Append a step definition to STEPS'''
    _s = {
        "name": name,
        "image": image,
        "command": cmd,
        "args": args
    }
    if env is not None:
        _s["env"] = step_env(env)
    global STEPS
    STEPS.append(_s)


def step_env(env):
    '''For the convenience of Fluid users, env is a dict; Tekton requires a list'''
    return [{"name": k, "value": v} for i, (k, v) in enumerate(env.items())]


def _resource(name, typ, params):
    '''Return a PipelineResource'''
    return {
        "apiVersion": "tekton.dev/v1alpha1",
        "kind": "PipelineResource",
        "metadata": {
            "name": k8s.safe_name(name)
        },
        "spec": {
            "type": typ,
            "params": params}}


def git_resource(name, url, revision):
    '''Return a PipelineResource of type git'''
    return _resource(name, "git", {
        "url": url,
        "revision": revision})


def image_resource(name, url):
    '''Return a PipelineResource of type image'''
    return _resource(name, "image", {"url": url})


INPUT_RESOURCES = []
OUTPUT_RESOURCES = []
