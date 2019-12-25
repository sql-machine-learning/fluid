# Fluid

Fluid is a Python package allowing users to write [Tekton](https://github.com/tektoncd/pipeline) workflows in Python other than YAML.

Here is an example.  To the left is a Python program defining a Task and related TaskRun.  To the right is the equivalent YAML file.

<table><tr><td valign=top>

```python
import fluid

@fluid.task
def echo_hello_world(hello, world="El mundo"):
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

## Fluid as a Langauge

You can consider Fluid a programming langauge with a small subset of Python syntax.

- Only function definitions and function invocations.
- Only positional arguments, but no keyword (named) arguments.
- Functions have no return values. (Tekton doesn't support Task output parameters.)

When you run a Fluid program, which is indeed a Python program, it prints the YAML file, which, you can then to submit the YAML to Tekton.
