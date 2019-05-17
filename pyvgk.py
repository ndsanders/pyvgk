#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Python program to run ESDU's VGK software as a subprocess on Windows.

Examples
--------
>>> from pyvgk import vgk, vgkcon
>>> returncode, errors = vgkcon(args)  # Run vgkcon.exe as a subprocess
>>> returncode, errors = vgk(args)  # Run vgk.exe as a subprocess.

:Author:
    Nicholas Sanders <N.Sanders@exeter.ac.uk>
:Date:
    17 May 2019
"""
import sys
from pathlib import PurePath
from subprocess import Popen, PIPE, TimeoutExpired
import logging

__all__ = ["vgk, vgkcon"]

VGK_EXE = "vgk.exe"
VGKCON_EXE = "vgkcon.exe"
ENCODING = "utf-8"
logger = logging.getLogger("PyVGK")


def vgk(filename, timeout=5, dir_="."):
    """
    Run ``vkg.exe`` as a subprocess.

    Parameters
    ----------
    filename : str
        Filename *with* the ``*.sir`` extension.
    timeout : float, optional
        The number of seconds to wait before the subprocess times out. The
        default is to wait for 5 seconds.
    dir_ : str, optional
        The directory in which ``vgk.exe`` is located. By default it is in the
        current working directory.

    Returns
    -------
    int
        Return-code from the ``vgk.exe`` subprocess. 0 indicates a successful
        completion; anything else is considered failure.
    str
        Errors from the ``vgk.exe`` subprocess. ``NoneType`` if no errors
        occured.
    """
    vgk_exe = str(PurePath(dir_, VGK_EXE))
    logger.debug(f"vgk_exe := {vgk_exe}")

    # Run vgk with the given arguments.
    filename = (filename + "\n").encode(ENCODING)
    with Popen([vgk_exe], stdout=PIPE, stdin=PIPE, stderr=PIPE) as proc:
        try:
            __, errs = proc.communicate(filename, timeout=timeout)
        except TimeoutExpired as err:
            logger.error(
                f"TimeoutExpired: communication with {vgk_exe} has timed out "
                f"after {timeout} seconds.",
                exc_info=True
            )
            proc.kill()
            sys.exit(1)

        return proc.returncode, errs.decode(ENCODING).strip()


def vgkcon(*args, timeout=5, dir_="."):
    """
    Run ``vgkcon.exe`` with the arguments.

    Parameters
    ----------
    *args
        Arbitrary number of arguments to pass to vgkcon.exe. Note that these
        must be in the correct order and format accepted by ``vgkcon.exe``.
    timeout : float, optional
        The number of seconds to wait before the subprocess times out. The
        default is to wait for 5 seconds.
    dir_ : str, optional
        The directory in which ``vgk.exe`` is located. By default it is in the
        current working directory.

    Returns
    -------
    int
        Return-code for the ``vgkcon.exe`` subprocess. 0 indicates a successful
        completion; anything else is considered failure.
    str
        Errors from the ``vgkcon.exe`` subprocess. ``NoneType`` if no errors
        occured.

    Notes
    -----
    The output from ``vgkcon.exe`` will be written to your current directory.
    """
    vgkcon_exe = str(PurePath(dir_, VGKCON_EXE))
    logger.debug(f"vgkcon_exe := {vgkcon_exe}")
    
    # Build the argument string from `args`.
    args = "\n".join(map(str, args)) + "\n"
    args = args.encode(ENCODING)
    logger.debug(f"args := {args}")
    
    # Run vgk with the given arguments.
    with Popen([vgkcon_exe], stdout=PIPE, stdin=PIPE, stderr=PIPE) as proc:
        try:
            __, errs = proc.communicate(args, timeout=timeout)
        except TimeoutExpired as err:
            logger.error(
                f"TimeoutExpired: communication with {vgkcon_exe} has timed "
                f"out after {timeout} seconds.",
                exc_info=True
            )
            proc.kill()
            sys.exit(1)
        
        return proc.returncode, errs.decode(ENCODING).strip()
