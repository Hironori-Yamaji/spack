# Copyright 2013-2019 Lawrence Livermore National Security, LLC and other
# Spack Project Developers. See the top-level COPYRIGHT file for details.
#
# SPDX-License-Identifier: (Apache-2.0 OR MIT)

# ----------------------------------------------------------------------------
# If you submit this package back to Spack as a pull request,
# please first remove this boilerplate and all FIXME comments.
#
# This is a template package file for Spack.  We've put "FIXME"
# next to all the things you'll want to change. Once you've handled
# them, you can save this file and test your package like this:
#
#     spack install nicam-dc-mini
#
# You can edit this file again by typing:
#
#     spack edit nicam-dc-mini
#
# See the Spack documentation for more information on packaging.
# ----------------------------------------------------------------------------

from spack import *


class NicamDcMini(MakefilePackage):
    """FIXME: Put a proper description of your package here."""

    # FIXME: Add a proper url for your package's homepage here.
    homepage = "http://www.example.com"
    git      = "https://github.com/fiber-miniapp/nicam-dc-mini.git"

    version('master', branch='master')
    version('1.1', commit='f0785b8cbf7957648797cb9e03125d0c223f85bf')

    depends_on('mpi')

    build_directory = './src'

    def edit(self, spec, prefix):
        if '%fj' in spec:
            config = FileFilter('./sysdep/Makedef.K')
            config.filter('-Qi -Qt -X03 -Ncompdisp -Koptmsg=1 -Cpp',
                          '-X03 -Ncompdisp -Koptmsg=1 -Cpp', string=True)
            config.filter('-Kprefetch_cache_level=all,' +
                          'prefetch_iteration_L2=50 -Ksimd',
                          '-Kprefetch_cache_level=all,' +
                          'prefetch_iteration_L2=50 -Ksimd -Ntl_notrt',
                          string=True)
            config.filter('-Ec -Eg -Ha -He -Hf -Ho -Hs -Hu -Hx -Ncheck_global',
                          '-Ec -Eg -Ha -He -Hf -Ho -Hs -Hu -Hx' +
                          '-Ncheck_global -Ntl_notrt',
                          string=True)
            config.filter('mpifrtpx', spec['mpi'].mpifc)
            config.filter('mpifccpx', spec['mpi'].mpicc)
            config.filter('-Kfast,parallel,ocl,preex,array_private,' +
                          'region_extension,restp=all -Qt ' +
                          '-Ksimd $(PERF_MONIT)',
                          '-Kfast,parallel,preex -Ksimd -Nclang $(PERF_MONIT)',
                          string=True)

    def setup_environment(self, spack_env, run_env):
        if '%fj' in self.spec:
            spack_env.set('NICAM_SYS', 'K')

    def build(self, spec, prefix):
        with working_dir('src'):
            make()

        copy_tree('.', prefix)
        with working_dir(prefix.test.case):
            make()

#    def install(self, spec, prefix):
#        mkdirp(prefix.bin)
#        copy_tree('.', prefix)

#        with working_dir('src'):
