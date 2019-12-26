# Fluid Syntax

You can consider Fluid a programming langauge with a small subset of Python syntax.

- Only function definitions and function invocations.
- Only positional arguments, but no keyword (named) arguments.
- Functions have no return values. (Tekton doesn't support Task output parameters.)

When you run a Fluid program, which is indeed a Python program, it prints the YAML file, which, you can then to submit the YAML to Tekton.
