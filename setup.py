import setuptools


setuptools.setup(
    name='toolstr',
    version='0.0.1',
    packages=['toolstr'],
    install_requires=[
        'tooltime',
    ],
    package_data={
        'toolstr': ['py.typed'],
    }
)

