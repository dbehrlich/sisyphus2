from setuptools import setup, find_packages

setup(
    name='Sisyphus',
    version='0.2dev',
    packages=find_packages(),
    license='MIT',
    long_description=open('README.md').read(),

    install_requires=['docutils>=0.3', 'tensorflow', 'numpy'],

    author="Alex Atanasov, David Brandfonbrener, Daniel Ehrlich, Jasmine Stone",
    author_email="daniel.ehrlich@yale.edu",
    description="Easy-to-use package for the modeling and analysis of neural network dynamics, directed towards cognitive neuroscientists.",
    keywords="neuroscience, modeling, analysis, neural networks",
    url="https://github.com/dbehrlich/sisyphus2/tree/networks-branch",

)