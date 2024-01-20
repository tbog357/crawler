from setuptools import setup

setup(
   name='news',
   version='1.0',
   description='A useful module',
   author='A news',
   author_email='tbog357',
   packages=['spiders'],  #same as name
   install_requires=['requests'], #external packages as dependencies
)