# -*- coding: utf-8 -*-
'''This module demonstrates writing Tekton tutorial TaskRun in Fluid.

'''

import fluid


@fluid.task
def build_docker(docker_source: "input,git",
                 built_image: "output,image",
                 path_to_dockerfile,
                 path_to_context):
    '''Define a Tekton Task that builds a Docker image from a Git repo'''
    fluid.step(image="gcr.io/kaniko-project/executor:v0.14.0",
               cmd=["/kaniko/executor"],
               args=["--dockerfile", path_to_dockerfile,
                     "--destination", built_image,
                     "--context", path_to_context],
               env={"DOCKER_CONFIG": "/tekton/home/.docker/"})


SKAFFOLD_GIT = fluid.git_resource(
    "https://github.com/GoogleContainerTools/skaffold",
    revision="master")

SKAFFOLD_IMAGE_LEEROY_WEB = fluid.image_resource(
    "dockerhub.com/cxwangyi/leeroy-web")


build_docker(SKAFFOLD_GIT,
             path_to_dockerfile="Dockerfile",
             path_to_context="/workspace/docker-source/examples/microservices/leeroy-web",
             built_image=SKAFFOLD_IMAGE_LEEROY_WEB)
