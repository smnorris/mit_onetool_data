from codecs import open
from setuptools import setup, find_packages
import os

# Get the long description from the relevant file
with open('README.md', encoding='utf-8') as f:
    long_description = f.read()


def find_files(filepat, top):
    files = []
    for path, dirlist, filelist in os.walk(top):
        for name in fnmatch.filter(filelist, filepat):
            files.append(os.path.join(path, name))
    return files
datafiles = find_files("*", "data")

setup(name='dissdata',
      version='0.0.1',
      description="Data collection for MIT's DISS application",
      long_description=long_description,
      classifiers=[],
      keywords='',
      author='Simon Norris',
      author_email='snorris@hillcrestgeo.ca',
      url='https://github.com/smnorris/dissdata',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      package_data={'dissdata': datafiles},
      zip_safe=False,
      install_requires=[
          'click',
          'csvkit'
      ],
      extras_require={
          'test': ['pytest'],
      },
      entry_points="""
      [console_scripts]
      dissdata=dissdata.scripts.cli:cli
      """
      )
