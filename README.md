# Couler for Google Tekton

Couler is a Python package allowing users to write Argo and [Tekton](https://github.com/tektoncd/pipeline) workflows in Python other than YAML.

This project is the Couler backend for Tekton.  The version for Argo is at [here](https://github.com/sql-machine-learning/sqlflow/blob/develop/python/couler/).

Here is an example.  To the left is a Python program defining a Task and related TaskRun.  To the right is the equivalent YAML file.

<table><tr><td valign=top>

```python
import fluid as couler

@couler.task
def echo_hello_world(hello, world="El mundo"):
    couler.step(image="ubuntu", cmd=["echo"], args=[hello])
    couler.step(image="ubuntu", cmd=["echo"], args=[world])
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
```

</td></tr><tr><td valign=top>

```python
echo_hello_world("Aloha")
```

</td><td valign=top>

```yaml
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

</td></tr></table>

For more information, please refer to the following documents.

- [Tutorial](doc/tutorial.md)
- [Design](doc/design.md)
- [Syntax](doc/syntax.md)
