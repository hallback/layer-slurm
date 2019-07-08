import importlib
from charms.slurm.helpers import get_slurm_version
from charmhelpers.osplatform import get_platform

__platform__ = get_platform()
module = 'charmhelpers.fetch.%s' % __platform__
fetch = importlib.import_module(module)

# fetch/centos.py has no equivalent to get_upstream_version
# query slurm directly instead using sinfo wrapper (both ubuntu/centos)
from charmhelpers.core.hookenv import status_set
from charmhelpers.core.hookenv import application_version_set

from charms.reactive import when_not
from charms.reactive import set_state

# Packages
if __platform__ == 'ubuntu':
    pkg_install = fetch.apt_install
    packages = ['slurm-wlm']
elif __platform__ == "centos":
    pkg_install = fetch.install
    packages = ['slurm-slurmd']


@when_not('slurm.installed')
def install_slurm():
    status_set('maintenance', 'installing slurm packages')

    # Install packages
    pkg_install(packages)

    # TODO: Query if installation was successful, then set flag,
    # status and version accordingly.

    # Set Slurm version
    slurm_version = get_slurm_version()
    if slurm_version is not None:
        application_version_set(slurm_version)
        set_state('slurm.installed')
    else:
        status_set('maintenance', 'failed to install slurm packages, will retry')
