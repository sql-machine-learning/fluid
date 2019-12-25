# Fluid

fluid is a transpiler that converts a Python program into a YAML file representing a workflow that can be executed by Tekton Pipeline.

fluid accepts a subset of Python syntax, namely, function definitions and function invocations.  A comprehensive understanding of fluid is an Python compiler that outputs Kubernetes-native programs.

## Kubernetes Resource

Tekton Pipeline is a Kubernetes-native workflow engine.  When we say Kubernetes-native, we mean that users could submit workflow YAML using the official Kubernetes client `kubectl`, and any Kubernetes cluster with Tekton Pipeline installed could understand the content of these YAML files.

Kubernetes understands YAML files that define [*Kubernetes objects*](https://kubernetes.io/docs/concepts/overview/working-with-objects/kubernetes-objects/), or *Kubernetes resources*.  Each Kubernetes object includes the following [required fields](https://kubernetes.io/docs/concepts/overview/working-with-objects/kubernetes-objects/#required-fields).

- `apiVersion` - Which version of the Kubernetes API you’re using to create this object.
- `kind` - What kind of object you want to create.
- `metadata` - Data that helps uniquely identify the object, including a name string, UID, and optional namespace.
- `spec` - What state you desire for the object.

The value of `apiVersion` of all Tekton objects is `tekton.dev/v1alpha1`.  The value of `kind` specifies the kind  of object, which we will go over in the rest of this document and examine how to represent them in Python syntax.  The value of `metadata` and `spec` depends on the kind.

### Task

A Task looks like a a function definition, according to the [definition](https://github.com/tektoncd/pipeline/blob/master/docs/tasks.md).

A Task consists one or more steps, each is like a statement.  Each step runs as a container.

Here follows a Task example from [Tekton's tutorial](https://github.com/tektoncd/pipeline/blob/master/docs/tutorial.md#task).  It has only one step.  The function name is specified in the the field `name` under `metadata`.

```yaml
apiVersion: tekton.dev/v1alpha1
kind: Task
metadata:
  name: echo-hello-world
spec:
  steps:
    - name: echo
      image: ubuntu
      command:
        - echo
      args:
        - "hello world"
```

We hope Fluid users could represent it with the following Python function definition.

```python
import fluid

@fluid.function
def echo_hello_word():
    fluid.step(image="ubuntu", cmd="echo", args=["hello world"])
```

We want to define the function `fluid.step`, which writes the above YAML file to standard output.

A Task could also include inputs, like parameters of a function, and outputs, like return values of a function.  We will go over them later.

### TaskRun 

A TaskRun object is like a function invocation.

A TaskRun object defines a call to a Task.  The following is a TaskRun example from [Tekton's tutorial](https://github.com/tektoncd/pipeline/blob/master/docs/tutorial.md#task).

```yaml
apiVersion: tekton.dev/v1alpha1
kind: TaskRun
metadata:
  name: echo-hello-world-task-run
spec:
  taskRef:
    name: echo-hello-world
```

We hope Fluid users could represent it with the following function invocation.

```python
echo_hello_world()
```

Please be aware that the above line of Python/Fluid code doesn't name the invocation as something like  `echo-hello-world-task-run` the the above YAML file.  To generate the above YAML file, we would need to derive a TaskRun name from the invocation, which could be the function name plus the file and line number of the invocation.

A TaskRun could provide inputs to a Task.  We will cover this later.

### PipeLineResource

A Tekton PipelineResource object is like a global variable of struct type.  In [Tekton tutorial](https://github.com/tektoncd/pipeline/blob/master/docs/tutorial.md#task-inputs-and-outputs), the following example shows a variable of struct `git`, which has two fields: `revision` and `url`.

```yaml
apiVersion: tekton.dev/v1alpha1
kind: PipelineResource
metadata:
  name: skaffold-git
spec:
  type: git
  params:
    - name: revision
      value: master
    - name: url
      value: https://github.com/GoogleContainerTools/skaffold 
```

We hope Fluid users could represent it by the following line.

```python
skaffold_git = fluid.Git(
    revision="master", 
    url="https://github.com/GoogleContainerTools/skaffold)
```

Please be aware that the call to `fluid.Git` doesn't include the name `skaffold-git` in the above YAML file.  To generate a name, `fluid.Git` needs to use some heuristics.  The generated name should be returned and saved in the Python variable `skaffold_git`, so it could be referred by some other Tekton objects.

Tekton also provides a PipelineResource of type `image` that refers to a Docker image.

```yaml
apiVersion: tekton.dev/v1alpha1
kind: PipelineResource
metadata:
  name: skaffold-image-leeroy-web
spec:
  type: image
  params:
    - name: url
      value: gcr.io/wangkuiyi/leeroy-web
```

We hope Fluid users could represent the above YAML file by the following line.

```python
skaffold_image_leeroy_web = fluid.Image(
    url="gcr.io/wangkuiyi/leeroy-web")
```

### Task with Inputs and Outputs

A Python function can take parameters as inputs and return zero, one, or more return values.  A Python function could read from and/or write to global variables.

A Task can have input parameters and output (return) values.  It can also refer to PipeLineResources as inputs and outputs.   In a Task definition, we need to list the PipelineResource used by the Task, and denote each one as either input or output.

According to the [document](https://github.com/tektoncd/pipeline/blob/master/docs/resources.md#using-resources),

> Input resources, like source code (git) or artifacts, are dumped at path `/workspace/task_resource_name` within a mounted volume and are available to all steps of your Task. The path that the resources are mounted at can be overridden with the targetPath field. Steps can use the path variable substitution key to refer to the local path to the mounted resource.

The following example from the [Tekton tutorial](https://github.com/tektoncd/pipeline/blob/master/docs/tutorial.md#task-inputs-and-outputs) takes an input resource, an output resource, and two input parameters.

```yaml
goapiVersion: tekton.dev/v1alpha1
kind: Task
metadata:
  name: build-docker-image-from-git-source
spec:
  inputs:
    resources:
      - name: docker-source
        type: git
    params:
      - name: pathToDockerFile
        type: string
        description: The path to the dockerfile to build
        default: /workspace/docker-source/Dockerfile
      - name: pathToContext
        type: string
        description:
          The build context used by Kaniko
          (https://github.com/GoogleContainerTools/kaniko#kaniko-build-contexts)
        default: /workspace/docker-source
  outputs:
    resources:
      - name: builtImage
        type: image
  steps:
    - name: build-and-push
      image: gcr.io/kaniko-project/executor:v0.14.0
      # specifying DOCKER_CONFIG is required to allow kaniko to detect docker credential
      env:
        - name: "DOCKER_CONFIG"
          value: "/tekton/home/.docker/"
      command:
        - /kaniko/executor
      args:
        - --dockerfile=$(inputs.params.pathToDockerFile)
        - --destination=$(outputs.resources.builtImage.url)
        - --context=$(inputs.params.pathToContext)
```

We hope Fluid users could represent it by the following Python/Fluid code.

```python
def build_docker_image_from_git_source(
```
