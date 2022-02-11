import setuptools


setuptools.setup(
    name='toolstr',
    version='0.0.2',
    packages=['toolstr'],
    install_requires=[
        'tooltime',
        'typing_extensions',
    ],
    package_data={
        'toolstr': ['py.typed'],
    }
)

