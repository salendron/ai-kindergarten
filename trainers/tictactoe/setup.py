'''Cloud ML Engine package configuration.'''
from setuptools import setup, find_packages

setup(name='tictactoe',
      version='1.0',
      packages=find_packages(),
      include_package_data=True,
      description='Train a TicTacToe Player',
      author='Bruno Hautzenberger',
      author_email='bhautzenberger@gmail.com',
      install_requires=[
          'keras==2.1.3',
          'google-cloud-datastore==1.7.3',
          'h5py'],
      zip_safe=False)