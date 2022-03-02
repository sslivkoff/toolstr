import setuptools


setuptools.setup(
    name='toolstr',
    version='0.1.0',
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

