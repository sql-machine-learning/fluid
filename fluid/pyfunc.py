# -*- coding: utf-8 -*-
'''This module defines Fluid primitives for users to write Fluid
program.

'''

import inspect
import sys
import re

import yaml

import fluid.tekton as tekton
import fluid.k8s as k8s

__all__ = [
    'Secret', 'FluidSyntaxError', 'dump_yaml', 'task', 'step', 'git_resource',
    'image_resource', 'service_account'
]


def dump_yaml(content):
    '''Pretty print a Python dictionary as a YAML'''
    print("---")
    yaml.dump(content, sys.stdout)


def task(func):
    '''Dump func as Task and returns a function to print TaskRun'''
    _resources_before_params(func)
    dump_yaml(tekton.task(func))

    def print_taskrun(*args):
        dump_yaml(tekton.task_run(func, args))
    return print_taskrun


class FluidSyntaxError(Exception):
    '''FluidSyntaxError records syntax errors'''


def _resources_before_params(func):
    '''Check annotated params (resources)
       are all before non-annoted params
    '''
    seen_param = False
    argspec = inspect.getfullargspec(func)
    for i, arg in enumerate(argspec.args):
        anno = argspec.annotations.get(arg)
        if anno is None:
            seen_param = True
        else:
            _resource_has_no_default(i, arg, anno, argspec)
            _resources_annotation_io_type(arg, anno)
            if seen_param:
                raise FluidSyntaxError(f"{arg} is annotated and is \
                    after a non-annotated param")


def _resource_has_no_default(i, arg, anno, argspec):
    '''Raise an error message is annotation and default both exist'''
    num_args = 0 if argspec.args is None else len(argspec.args)
    num_defaults = 0 if argspec.defaults is None else len(argspec.defaults)
    has_default = i >= num_args - num_defaults
    if anno is not None and has_default:
        raise FluidSyntaxError(f"{arg} cannot be a resource and has default")


PATTERN = re.compile("(input|output),(git|image)")


def _resources_annotation_io_type(arg, anno):
    '''Raise an error if the annotation does not match PATTERN'''
    _z = PATTERN.match(anno)
    if _z is None:
        raise FluidSyntaxError(f"{arg} has illegel annotaiton {anno}")


def _loc(frame):
    '''Return the location of a Python function invocation'''
    # See https://stackoverflow.com/a/6628348/724872.
    caller_of_step = inspect.stack()[frame]
    filename = caller_of_step[1]
    lineno = caller_of_step[2]
    return k8s.safe_name(f"{filename}-{lineno}")


def step(image, cmd, args, env=None):
    '''Define a step'''
    # frame 0 - _loc()
    # frame 1 - fluid.step()
    # frame 2 - caller_of_step
    name = _loc(2)
    tekton.add_step(name, image, cmd, args, env)


def git_resource(url, revision):
    '''Define a Git repo resource. Return the resource metadata.name'''
    # frame 0 - _loc()
    # frame 1 - fluid.git()
    # frame 2 - caller of git
    name = _loc(2)
    dump_yaml(tekton.git_resource(name, url, revision))
    return name


def image_resource(url):
    '''Define a Docker image resource. Return the resource metadata.name'''
    # frame 0 - _loc()
    # frame 1 - fluid.image()
    # frame 2 - caler of image
    name = _loc(2)
    dump_yaml(tekton.image_resource(name, url))
    return name


class Secret:
    '''Use with Python with statement to set and unset
    tekton.SERVICE_ACCOUNT_NAME'''

    def __init__(self, name):
        self._name = name

    def __enter__(self):
        tekton.SERVICE_ACCOUNT_NAME = self._name
        return tekton.SERVICE_ACCOUNT_NAME

    def __exit__(self, typ, value, traceback):
        tekton.SERVICE_ACCOUNT_NAME = None


def service_account(secret):
    '''Return a Kubernetes ServiceAccount'''
    name = _loc(2)
    dump_yaml({
        "apiVersion": "v1",
        "kind": "ServiceAccount",
        "metadata": {
            "name": name
        },
        "secrets": {
            "name": secret
        }
    })
    return name
