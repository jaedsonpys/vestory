from setuptools import setup
from setuptools.command.install import install
from vestory import vestory_config


class Prepare(install):
    def run(self):
        install.run(self)
        # create config file in home diretory
        vestory_config.create_config()


setup(
    author='Jaedson Silva',
    author_email='imunknowuser@protonmail.com',
    name='vestory',
    version='1.2.0',
    packages=['vestory'],
    cmdclass={'install': Prepare},
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
