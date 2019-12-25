#!/usr/bin/env python

import fluid


@fluid.task
def echo_hello_world(hello, world="世界"):
    '''Defines an example Tekton Task'''
    fluid.step(image="ubuntu", cmd=["echo"], args=[hello])
    fluid.step(image="ubuntu", cmd=["echo"], args=[world])


if __name__ == "__main__":
    echo_hello_world("你好")
