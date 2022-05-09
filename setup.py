import setuptools


setuptools.setup(
    name='toolstr',
    version='0.1.3',
    packages=setuptools.find_packages(),
    install_requires=[
        'tooltime',
        'typing_extensions',
    ],
    package_data={
        'toolstr': ['py.typed'],
    }
)
