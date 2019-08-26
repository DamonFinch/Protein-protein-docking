import warnings

import numpy as np

from deeprank.conf import logger
from deeprank.targets import rmsd_fnat


def __compute_target__(decoy, targrp):
    """Calculate binary class ID using IRMSD.

    Args:
        decoy(bytes): pdb data of the decoy
        targrp(h5 file hadnle): HDF5 'targets' group

    Examples:
        >>> f = h5py.File('1LFD.hdf5')
        >>> decoy = f['1LFD_9w/complex'][()]
        >>> targrp = f['1LFD_9w/targets']
    """
    # set target name
    tarname = 'BIN_CLASS'

    # set target element and cutoff to binarize target
    tarelem = 'IRMSD'
    cutoff = 4

    # fet the mol group
    molgrp = targrp.parent
    molname = molgrp.name

    if tarname in targrp.keys():
        del targrp[tarname]
        warnings.warn(f"Removed old {tarname} from {molname}")

    # process target element
    if tarelem not in targrp:
        _ = rmsd_fnat.__compute_target__(decoy, targrp, tarelem)
    # empty dataset
    elif targrp[tarelem][()].shape is None:
        del targrp[tarelem]
        warnings.warn(f"Removed old {tarname} from {molname}")
        _ = rmsd_fnat.__compute_target__(decoy, targrp, tarelem)

    # get target value
    if targrp[tarelem][()] <= cutoff:
        classID = 1
        msg = f"{molname} is a hit with {tarelem}: {targrp[tarelem][()]} <= {cutoff}Å"
        logger.info(msg)
    else:
        classID = 0

    targrp.create_dataset('BIN_CLASS', data=np.array(classID))
