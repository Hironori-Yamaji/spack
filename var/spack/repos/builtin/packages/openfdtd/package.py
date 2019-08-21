# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

from spack import *


class Openfdtd(MakefilePackage):
    """OpenFDTD is general purpose FDTD simulator applicable to a wide range
       of applications. The FDTD method (Finite Difference Time Domain method)
       is a method for numerically calculating the Maxwell equation, which is
       the basic equation of the electromagnetic field,
       by the difference method."""

    homepage = "http://www.e-em.co.jp/OpenFDTD/"
    url      = "http://www.e-em.co.jp/OpenFDTD/OpenFDTD.zip"

    version('2.3.0', sha256='10ac70f2ed7160da87dd9222a5a17ca7b72365ee886235359afc48c4fb7b4be4')

    variant('mpi', default=False, description='Build with MPI Support')

    depends_on('mpi', when='+mpi')

    def edit(self, spec, prefix):
        if '%gcc' or '%fj' in self.spec:
            filter_file('gcc', spack_cc, './src/Makefile_gcc')
            if '+mpi' in self.spec:
                filter_file('mpicc', spec['mpi'].mpicc, './mpi/Makefile_gcc')

    # "Makefile" is used only in Windows development environment.
    # The build in Windows development environment is not confirmed.
    def build(self, spec, prefix):
        with working_dir('src'):
            if '%gcc' or '%fj' in self.spec:
                make('-f', 'Makefile_gcc')
            else:
                make()

        # To make an executable file for mpi needs object files
        # which are made for an executable file not for mpi.
        # Therefore, the build in the "src" directory is necessary
        # for to make an executable file for mpi.
        if '+mpi' in self.spec:
            with working_dir('mpi'):
                if '%gcc' or '%fj' in self.spec:
                    make('-f', 'Makefile_gcc')
                else:
                    make()

    def install(self, spec, prefix):
        mkdirp(prefix.bin)
        install('ofd', prefix.bin)
        if '+mpi' in self.spec:
            install('ofd_mpi', prefix.bin)
