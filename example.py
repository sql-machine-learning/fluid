# -*- coding: utf-8 -*-
'''This module demonstrates how to write a Fluid program.

'''

import fluid


@fluid.task
def echo_hello_world(hello, world="El mundo"):
    '''Defines an example Tekton Task'''
    fluid.step(image="ubuntu", cmd=["echo"], args=[hello])
    fluid.step(image="ubuntu", cmd=["echo"], args=[world])


if __name__ == "__main__":
    echo_hello_world("Aloha")
