from setuptools import setup, find_packages

setup(
    name='pyicl',
    version='1.0.0',
    author='Richardson Lima',
    author_email='contato@richardsonlima.com.br',
    description='PyICL (Python In-Context Learning) is a Python library designed to facilitate the implementation of In-Context Learning (ICL) with Large Language Models (LLMs).',
    long_description=open('README.md').read(),
    url='https://github.com/richardsonlima/PyICL.git',
    packages=find_packages(),
    install_requires=['openai==1.46.0', 'nltk', 'stopwords'],
    license='BSD License',
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)