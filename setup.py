from setuptools import setup, find_packages
import versioneer
import q2_surpi.__init__ as init

setup(
    name=init.__name__,
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    packages=find_packages(),
    package_data={
        init.__package_name__: [init.__citations_fname__]
    },
    author=init.__author__,
    author_email=init.__email__,
    description=init.__description__,
    license=init.__license__,
    url=init.__url__,
    entry_points={
        'qiime2.plugins':
        [f'{init.__name__}={init.__package_name__}.plugin_setup:plugin']
    },
)
