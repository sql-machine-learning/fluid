# Fluid

Fluid is a Python package allowing users to write [Tekton Pipeline](https://github.com/tektoncd/pipeline) workflows in Python other than YAML.

You can consider Fluid a programming langauge with a small subset of Python syntax.

- Only function definitions and function invocations.
- Only positional arguments, but no keyword (named) arguments.
- Functions have no return values. (Tekton doesn't support Task output parameters.)

When you run a Fluid program, which is indeed a Python program, it prints the YAML to standard output.  You can then to submit the YAML to Tekton.

Here is an example Fluid program.

<table><tr><td valign=top>

```python
import fluid

@fluid.task
def echo_hello_world(hello, world="El mundo"):
    '''Defines an example Tekton Task'''
    fluid.step(image="ubuntu", cmd=["echo"], args=[hello])
    fluid.step(image="ubuntu", cmd=["echo"], args=[world])

echo_hello_world("Aloha")
```

</td><td valign=top>

```yaml
---
apiVersion: tekton.dev/v1alpha1
kind: Task
metadata:
  name: echo-hello-world
spec:
  inputs:
    params:
    - description: ''
      name: hello
      type: string
    - default: El mundo
      description: ''
      name: world
      type: string
  steps:
  - args:
    - $(inputs.params.hello)
    command:
    - echo
    image: ubuntu
    name: example-py-12
  - args:
    - $(inputs.params.world)
    command:
    - echo
    image: ubuntu
    name: example-py-13
---
apiVersion: tekton.dev/v1alpha1
kind: TaskRun
metadata:
  name: echo-hello-world-run
spec:
  inputs:
    params:
    - name: hello
      value: Aloha
  taskRef:
    name: echo_hello_world
```

</tr></td></table>
