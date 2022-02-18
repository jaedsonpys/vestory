from setuptools import setup

setup(
    name='vestory',
    version='1.0.0',
    packages=['vestory'],
    entry_points={
        'console_scripts': [
            'vestory = vestory.__main__:main'
        ]
    }
)
