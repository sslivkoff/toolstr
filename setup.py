import setuptools


setuptools.setup(
    name='toolstr',
    version='0.1.1',
    packages=['toolstr'],
    install_requires=[
        'tooltime',
        'typing_extensions',
        'scikit-image',
    ],
    package_data={
        'toolstr': ['py.typed'],
    }
)

