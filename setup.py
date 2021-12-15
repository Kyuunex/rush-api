from distutils.core import setup

setup(
    name='rushapi',
    packages=[
        'rushapi',
        'rushapi.blueprints',
        'rushapi.reusables',
    ],
    version="0.1",
    description='REST URL Shortener API',
    author='Kyuunex',
    author_email='kyuunex@protonmail.ch',
    url='https://github.com/Kyuunex/rush-api',
    install_requires=[
        'flask',
        'validators',
    ],
)
