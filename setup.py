from distutils.core import setup

from wifite.config import Configuration

setup(
    name='Wifite2',
    version=Configuration.version,
    author='CyberDanish',
    author_email='derv82@gmail.com',
    url='https://github.com/derv82/wifite2',
    packages=[
        'wifite',
        'wifite/attack',
        'wifite/model',
        'wifite/tools',
        'wifite/util',
    ],
    data_files=[
        ('share/dict', ['wordlist2.txt'])
    ],
    entry_points={
        'console_scripts': [
            'wifite2 = wifite.__main__:entry_point'
        ]
    },
    license='GNU GPLv2',
    scripts=['bin/wifite2'],
    description='Wireless Network Auditor for Linux',
    #long_description=open('README.md').read(),
    long_description='''Wireless Network Auditor for Linux.

    Cracks WEP, WPA, and WPS encrypted networks.

    Depends on Aircrack-ng Suite, Tshark (from Wireshark), and various other external tools.''',
    classifiers = [
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3"
    ]
)
