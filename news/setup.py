from setuptools import setup

setup(
   name='crawler',
   version='1.0',
   description='A useful module',
   author='A Crawler',
   author_email='tbog357',
   packages=['crawler'],  #same as name
   install_requires=['requests'], #external packages as dependencies
)