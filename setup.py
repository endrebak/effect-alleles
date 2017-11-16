import os
import sys
from setuptools import setup, find_packages
# from Cython.Build import cythonize

# install_requires = ["scipy", "pandas", "numpy", "natsort", "joblib", "pyfaidx", "typing"]

__version__ = "0.0.1"

setup(
    name="effect_alleles",
    packages=find_packages(),

    scripts=["bin/effect_alleles"],
    package_data={'effect_alleles': ['data/aliases.txt']},
    #                        'scripts/chromsizes/*chromsizes',
    #                        'scripts/genome.snakefile']},
    version=__version__,
    description="Find the effect alleles for RS-ids in the GWAS catalogue.",
    author="Endre Bakken Stovner",
    author_email="endrebak85@gmail.com",
    url="http://github.com/endrebak/effect_alleles",
    keywords=["GWAS", "Mendelian Randomization"],
    license=["MIT"],
    # install_requires=install_requires,
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Development Status :: 4 - Beta",
        "Environment :: Other Environment", "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: POSIX :: Linux",
        "Operating System :: MacOS :: MacOS X",
        "Topic :: Scientific/Engineering"
    ],
    long_description= ("Find the effect alleles for RS-ids in the GWAS catalogue."))
