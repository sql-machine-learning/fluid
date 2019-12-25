# Fluid

Fluid is a Python package allowing users to write [Tekton Pipeline](https://github.com/tektoncd/pipeline) workflows in Python other than YAML.

You can consider Fluid a programming langauge with a small subset of Python syntax.

- Only function definitions and function invocations.
- Only positional arguments, but no keyword (named) arguments.
- Functions have no return values. (Tekton doesn't support Task output parameters.)

When you run a Fluid program, which is indeed a Python program, it prints the YAML to standard output.  You can then to submit the YAML to Tekton.

Here is an example Fluid program.

```python
import fluid

@fluid.task
def echo_hello_world(hello, world="El mundo"):
    '''Defines an example Tekton Task'''
    fluid.step(image="ubuntu", cmd=["echo"], args=[hello])
    fluid.step(image="ubuntu", cmd=["echo"], args=[world])

if __name__ == "__main__":
    echo_hello_world("Aloha")
```


