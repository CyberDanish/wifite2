from distutils.core import setup

from wifite2.config import Configuration

setup(
    name='wifite2',
    version=Configuration.version,
    author='CyberDanish',
    url='https://github.com/CyberDanish/wifite2',
    packages=[
        'wifite2',
        'wifite2/attack',
        'wifite2/model',
        'wifite2/tools',
        'wifite2/util',
    ],
    data_files=[
        ('share/dict', ['wordlist2.txt'])
    ],
    entry_points={
        'console_scripts': [
            'wifite2 = wifite2.__main__:entry_point'
        ]
    },
    license='GNU GPLv2',
    scripts=['bin/wifidk'],
    description='Wireless Network Auditor for Linux',
    #long_description=open('README.md').read(),
    long_description='''Wireless Network Auditor for Linux.

    Cracks WEP, WPA, and WPS encrypted networks.

    Depends on Aircrack-ng Suite, Tshark (from Wireshark), and various other external tools.''',
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3"
    ]
)
