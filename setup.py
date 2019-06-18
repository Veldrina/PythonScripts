from setuptools import setup

setup(name='veldrina_toolbox',
      version='0.1',
      packages=find_packages(),
      install_requires=[
          'docopt==0.6.2'],
      description='A collection of useful (to Veldrina) Python scripts',
      url='https://github.com/Veldrina/PythonScripts',
      author='Veldrina',
      author_email='wualank@gmail.com',
      license='MIT')