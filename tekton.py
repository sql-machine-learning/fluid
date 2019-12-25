import inspect
import k8s


def task(func):
    return obj(
        kind="Task",
        name=func.__name__,
        spec={
            "inputs": {
                "params": task_params(inspect.getfullargspec(func))
            }
        })


def task_run(func, *args, **kwargs):
    return obj(
        kind="TaskRun",
        name=func.__name__ + "-run",
        spec={
            "taskRef": {
                "name": func.__name__
            },
            "inputs": {
                "params": len(args) + len(kwargs)  # Complete this.
            }
        })


def obj(kind, name, spec):
    '''Returns a dict of Tekton object'''
    return {
        "apiVersion": "tekton.dev/v1alpha1",
        "kind": kind,
        "metadata": {
            "name": k8s.safe_name(name),
        },
        "spec": spec
    }


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


def step(name, image, cmd, args):
    return {
        "name": name,
        "image": image,
        "command": cmd,
        "args": args
    }
