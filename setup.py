from setuptools import setup

setup(
    author='Jaedson Silva',
    author_email='imunknowuser@protonmail.com',
    name='vestory',
    version='1.2.0',
    packages=['vestory'],
    install_requires=['PySeqTest', 'argeasy'],
    entry_points={
        'console_scripts': [
            'vestory = vestory.__main__:main'
        ]
    },
    project_urls={
        'Código fonte': 'https://github.com/jaedsonpys/vestory',
        'Licença': 'https://github.com/jaedsonpys/vestory/blob/master/LICENSE'
    },
    license='GNU General Public License v3.0'
)
