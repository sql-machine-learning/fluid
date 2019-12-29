# -*- coding: utf-8 -*-
'''This module demonstrates writing Tekton tutorial TaskRun in Fluid.

'''

import fluid


@fluid.task
def build_docker_image_from_git_source(
        docker_source: "input,git",
        built_image: "output,image",
        path_to_dockerfile="/workspace/docker-source/Dockerfile",
        path_to_context="/workspace/docker-source"):
    '''Define a Tekton Task that builds a Docker image from a Git repo'''
    fluid.step(image="gcr.io/kaniko-project/executor:v0.14.0",
               cmd=["/kaniko/executor"],
               args=[f"--dockerfile={path_to_dockerfile}",
                     f"--destination={built_image.url}",
                     f"--context={path_to_context}"],
               env={"DOCKER_CONFIG": "/tekton/home/.docker/"})


SKAFFOLD_GIT = fluid.git_resource(
    url="https://github.com/GoogleContainerTools/skaffold",
    revision="master")

SKAFFOLD_IMAGE_LEEROY_WEB = fluid.image_resource(
    url="dockerhub.com/cxwangyi/leeroy-web")


with fluid.Secret(fluid.service_account("regcred")):
    build_docker_image_from_git_source(
        SKAFFOLD_GIT,
        SKAFFOLD_IMAGE_LEEROY_WEB,
        "Dockerfile")
