from setuptools import setup

setup(
    name='pakecli',
    version='1.0',
    py_modules=['pakecli'],
    install_requires=[
        'Click',
        'libnum',
        'pycryptodome',
    ],
    entry_points={
        'console_scripts': [
            'pakecli = pakecli:pake',
        ],
    },
)
