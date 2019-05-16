#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python wrapper for ESDU's VGK software.

Examples
--------
>>> from pyvgk import vgk, vgkcon
>>> returncode, errors = vgkcon(args)  # Run vgkcon.exe as a subprocess
>>> returncode, errors = vgk(args)  # Run vgk.exe as a subprocess.

:Author:
    Nicholas Sanders <N.Sanders@exeter.ac.uk>
:Date:
    12 Jun 2018
"""
import sys
from pathlib import PurePath
from subprocess import Popen, PIPE, TimeoutExpired

__all__ = ["vgk, vgkcon"]
__version__ = "1.0"

VGK_EXE = "vgk.exe"
VGKCON_EXE = "vgkcon.exe"
ENCODING = "utf-8"


def vgk(filename, timeout=5, dir_="."):
    """
    Run vkg.exe as a subprocess.

    Parameters
    ----------
    filename : str
        Filename WITH the *.sir extension.
    timeout : float, optional
        The number of seconds to wait before the subprocess times out. By
        default the timeout is 5 seconds.
    dir_ : str, optional
        The directory in which vgk.exe is located. By default it is in the
        current working directory.

    Returns
    -------
    int
        Return-code from the vgk.exe subprocess. 0 indicates a successful
        completion.
    str
        Errors from the vgk.exe subprocess. ``NoneType`` if no errors occured.
    """
    vgk_exe = str(PurePath(dir_, VGK_EXE))

    # Run vgk with the given arguments.
    filename = (filename + "\n").encode(ENCODING)
    with Popen([vgk_exe], stdout=PIPE, stdin=PIPE, stderr=PIPE) as proc:
        try:
            __, errs = proc.communicate(filename, timeout=timeout)
        except TimeoutExpired as err:
            print(
                "TimeoutExpired: communication with {} has timed out after {} "
                "seconds.".format(vgk_exe, timeout),
                file=sys.stderr
            )
            proc.kill()
            sys.exit(1)
        finally:
            return proc.returncode, errs.decode(ENCODING).strip()


def vgkcon(*args, timeout=5, dir_="."):
    """
    Run vgkcon.exe with the arguments.

    Parameters
    ----------
    *args
        Arbitrary number of arguments to pass to vgkcon.exe. Note that these
        must be in the correct order and format accepted by vgkcon.exe.
    timeout : float, optional
        The number of seconds to wait before the subprocess times out. By
        default the timeout is 5 seconds.
    dir_ : str, optional
        The directory in which vgk.exe is located. By default it is in the
        current working directory.

    Returns
    -------
    int
        Return-code for the vgkcon subprocess. 0 indicates a successful
        completion.
    str
        Errors from the vgkcon.exe subprocess. ``NoneType`` if no errors
        occured.

    Notes
    -----
    The vgkcon.exe will save its output to the same directory.
    """
    vgkcon_exe = str(PurePath(dir_, VGKCON_EXE))
    
    # Build the argument string from `args`.
    args = "\n".join(map(str, args)) + "\n"
    args = args.encode(ENCODING)
    print("`vgkcon.exe` arguments:", args)  # TODO(ns354) Delete this print().
    
    # Run vgk with the given arguments.
    with Popen([vgkcon_exe], stdout=PIPE, stdin=PIPE, stderr=PIPE) as proc:
        try:
            __, errs = proc.communicate(args, timeout=timeout)
        except TimeoutExpired as err:
            print(
                "TimeoutExpired: communication with {} has timed out after {} "
                "seconds.".format(vgkcon_exe, timeout),
                file=sys.stderr
            )
            proc.kill()
            sys.exit(1)
        
        return proc.returncode, errs.decode(ENCODING).strip()