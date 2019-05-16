"""
Configuration management class for `vgkcon.exe`.

Examples
--------
>>> from pyvgk import vgk, vgkcon, VGKConfiguration
>>>
>>> # It's recommended to create a dictionary of configuration options, and
>>> # then pass the dictionary to `VGKConfiguration`.
>>> configuration = {
    "filename":example,
    "title":"Example usage of VGKConfiguration.",
    "viscous":True,
    "datfile":"rae2822.dat",
    "mach":0.7,
    "incidence":2.0,
    "reynolds":6.04e6,
    "xtu":0.05,
    "xtl":0.05
    }
>>> vgkconfig = VGKConfiguration(**configuration)
>>> vgkcon("example", vgkconfig.encode())
>>> vgkcon("example")

:Author:
    Nicholas Sanders <N.Sanders@exeter.ac.uk>
:Date:
    20 Sep 2018
"""
from re import match


class VGKConfiguration():
    
    def __init__(self, filename, viscous, datfile, mach, incidence, reynolds, 
            xtu, xtl, *args, **kwargs):
        """
        Constructs VGK configuration file.
        
        Parameters
        ----------
        filename : str
            Input/output filename.
        viscous : {True, False}
            Viscous run iff `True`, otherwise an inviscid run is performed.
        datfile : str
            Aerofoil design co-ordinates file (*with* `.dat` extension).
        mach : float
            Mach number.
        incidence : float
            Angle of incidence.
        reynolds : float
            Reynold's number.
        *args, **kwargs
            Additional (keyword) arguments to modify the default configuration.
        """
        # TODO(ns354) Finish (and test) default constructor behaviour.
        # Mandatory configuration parameters.
        self.filename = filename
        self.viscous = viscous
        self.datfile = datfile
        self.mach = mach
        self.incidence = incidence
        self.reynolds = reynolds
        self.xtu = xtu
        self.xtl = xtl
        
        # Optional configuration parameters.
        self.title = kwargs.get("title", "")
        self.continuation = kwargs.get("continuation", None)
        self.output_tos = kwargs.get("output_tos", "no")  # TODO(ns354) Change to boolean?
        self.output_griddata = kwargs.get("output_griddata", "no")  # TODO(ns354) Change to boolean?
        self.output_binarydump = kwargs.get("output_binarydump", "no")  # TODO(ns354) Change to boolean?
        self.lift = kwargs.get("lift", None)
        
        # Default VGK parameters.
        self._change_defaults = "n"
        self.partially_conservative = kwargs.get("partially_conservative", None)
        self.artificial_viscosity = kwargs.get("artificial_viscosity", None)
        self.dd22 = kwargs.get("dd22", None)  # TODO(ns354) Give better name.
        self.dd21 = kwargs.get("dd21", None)  # TODO(ns354) Give better name.
        self.coarse_relaxation = kwargs.get("coarse_relaxation", None)
        self.fine_relaxation = kwargs.get("fine_relaxation", None)
        self.under_relaxation = kwargs.get("under_relaxation", None)
        self.over_relaxation = kwargs.get("over_relaxation", None)
        self.finemesh_gridlines = kwargs.get("finemesh_gridlines", None)
        self.finemesh_iterations = kwargs.get("finemesh_iterations", None)
        self.coarsemesh_iterations = kwargs.get("coarsemesh_iterations", None)
    
    def encode(self, encoding="utf-8"):
        """
        Gets the encoded string representation of the configuration.
        
        Parameters
        ----------
        encoding : str, optional
        
        Returns
        -------
        bytes
            Encoded representation of the configuration.
        """
        return str(self).encode(encoding)
        
    def __str__(self):
        """
        Builds and returns the string representation of the configuration.
        
        Returns
        -------
        str
        """
        args = [self._filename, self._title, self._viscous]
        
        if self._continuation:
            args += [0, self._continuation]
        else:
            args += [1, self._datfile, self._output_tos, self._output_griddata]
        
        args += [self._mach, self._incidence]
        args += [1, self._lift] if self._lift else [0]
        args += [self._reynolds, self._xtu, self._xtl]
        
        if self._change_defaults:
            args += [
                "y",
                self._finemesh_gridlines,
                self._coarsemesh_iterations,
                self._finemesh_iterations,
                self._over_relaxation,
                self._under_relaxation,
                self._coarse_relaxation,
                self._niterations_inviscid_flow,
                self._fine_relaxation,
                self._niterations_fine_inviscid_flow,
                self._dd21,
                self._dd22,
                self._artificial_viscosity,
                self._partially_conservative
            ]
        else:
            args += ["n"]
        
        return "\n".join(map(str, args)) + "\n"
    
    @filename.setter
    def filename(self, filename):
        """
        Sets the input/output filename to use for vgkcon.exe and vgk.exe.
        
        Parameters
        ----------
        filename : str
            Alpha-numeric input/ouput filename to use.
            
        Raises
        ------
        ValueError
            Filename is either longer than eight characters or contains 
            non-alphanumeric characters.
        """
        if match("^[a-zA-Z0-9]{1,8}$", filename):
            self._filename = filename
        else:
            raise ValueError(
                "Filename must only contain alphanumeric characters and not "
                "be longer than 8 characters, but {} given.".format(filename)
            )
            
    @title.setter
    def title(self, title):
        """
        Sets a descriptive title for this VGK run.
        
        Parameters
        ----------
        title : str
        
        Raises
        ------
        ValueError
            The title is longer than 68 characters.
        """
        if len(title) <= 68:
            self._title = title
        else:
            raise ValueError(
                "Title must not be longer than 68 characters, but {} ({}) "
                "given.".format(title, len(title))
            )
            
    @datfile.setter
    def datfile(self, datfile):
        """
        Sets the design filename (`.dat` file).
        
        Parameters
        ----------
        datfile : str
            The aerofoil design file.
        
        Raises
        ------
        ValueError
            Design filename longer than eight characters (before the dot) *or*
            missing the `.dat` extension.
        """
        if match("^[a-zA-Z0-9]{1,8}\.dat$", datfile):
            self._datfile = datfile
        else:
            raise ValueError(
                "Design filename must contain the `.dat` extension and not be "
                "longer than 8 characters (before the dot), but {} given."
                .format(datfile)
            )
    
    @incidence.setter
    def incidence(self, incidence):
        """
        Sets the angle of incidence.
        
        Parameters
        ----------
        incidence : float
        
        Raises
        ------
        ValueError
            The angle of incidence is not in the range [-20, 20].
        """
        if -20 <= incidence <= 20:
            self._incidence = incidence
        else:
            raise ValueError(
                "Angle of incidence must be in [-20, 20], but {} given."
                .format(incidence)
            )
            
    @mach.setter
    def mach(self, mach):
        """
        Sets the Mach number.
        
        Parameters
        ----------
        mach : float
        
        Raises
        ------
        ValueError
            The mach number is not in the range [0.05, 0.95].
        """
        if 0.05 <= mach <= 0.95:
            self._mach = mach
        else:
            raise ValueError(
                "Mach number must be in the range [0.05, 0.95], but {} given."
                .format(mach)
            )
    
    @lift.setter
    def lift(self, lift):
        """
        Sets the coefficient of lift.
        
        Parameters
        ----------
        lift : float
        
        Raises
        ------
        ValueError
            The coefficient of lift is not in the range [0, 1].
        """
        if lift is None:
            self._user_defined_lift = False
            self._lift = None
        # TODO(ns354) Check this constraint.
        elif 0 <= lift <= 1:
            self._user_defined_lift = True
            self._lift = lift
        else:
            raise ValueError(
                "Coefficient of lift must be in [0, 1], but {} given."
                .format(lift)
            )
    
    @reynolds.setter
    def reynolds(self, reynolds):
        """
        Sets the Reynold's number.
        
        Parameters
        ----------
        reynolds : float
        
        Raises
        ------
        ValueError
            Reynold's number is not greater than 1x10^5.
        """
        if 1e5 <= reynolds:
            self._reynolds = reynolds / 1e6  # VGK expects Re to be divided by 1 million.
        else:
            raise ValueError(
                "Reynold's number must be greater than 1e5, but {} given."
                .format(reynolds)
            )
    
    @xtu.setter
    def xtu(self, xtu):
        """
        Sets the upper-surface transition location as a percentage of distance
        along the cord.
        
        Parameters
        ----------
        xtu : float
        
        Raises
        ------
        ValueError
            The upper-surface transition location does not exist in the range
            [0.01, 1.00].
        """
        if 0.01 <= xtu <= 1:
            self._xtu = xtu
        else:
            raise ValueError(
                "Upper-surface transition layer must be in [0.01, 1.00], but "
                "{} given".format(xtu)
            )
    
    @xtl.setter
    def xtl(self, xtl):
        """
        Sets the lower-surface transition location as a percentage of distance
        along the cord.
        
        Parameters
        ----------
        xtl : float
        
        Raises
        ------
        ValueError
            The lower-surface transition location does not exist in the range
            [0.01, 1.00].
        """
        if 0.01 <= xtl <= 1:
            self._xtl = xtl
        else:
            raise ValueError(
                "Lower-surface transition layer must be in [0.01, 1.00], but "
                "{} given.".format(xtl)
            )
    
    @continuation.setter
    def continuation(self, binarydump):
        """
        Sets wheter to start a new run or continue an old run.
        
        Parameters
        ----------
        binarydump : str or None
            The name of the binary dump file from which to continue the run. 
            A value of `None` will initialise a new run.
            
        Raises
        ------
        ValueError
            The binary dump file name is either longer than 8 characters or 
            contains invalid characters (alphanumeric characters, -, and 
            _ allowed).
            
        Notes
        -----
        The `.unf` extension is added by VGK, so must not be included in the 
        `binarydump` argument. 
        """
        if binarydump is None:
            self._continuation = False
        elif match("[a-zA-Z0-9-_]{1, 8}", binarydump):
            self._continuation = str(binarydump)
        else: 
            raise ValueError(
                "Binary dump must not be longer than 8 characters and must "
                "only contain alphanumeric characters, -, and _, but {} "
                "given.".format(binarydump)
            )
    
    @viscous.setter
    def viscous(self, viscous):
        """
        Sets whether to start a viscous or inviscid run.
        
        Parameters
        ----------
        viscous : {True, False}
            A value of `True` will start a viscous run.
        """
        if viscous:
            self._viscous = "1"
        else:
            self._viscous = "0"

    @output_griddata.setter
    def output_griddata(self, output):
        """
        Sets whether to output the grid data.
        
        Parameters
        ----------
        output : {True, False}
        """
        if output:
            self._output_griddata = "yes"
        else:
            self._output_griddata = "no"

    @output_tos.setter
    def output_tos(self, output):
        """
        Sets whether to output the table of slopes.
        
        Parameters
        ----------
        output : {True, False}
        """
        if output:
            self._output_tos = "yes"
        else:
            self._output_tos = "no"
    
    @output_binarydump.setter
    def output_binarydump(self, output):
        """
        Sets whether to perform a binary dump of the data.
        
        Parameters
        ----------
        output : {True, False}
        """
        if output:
            self._output_binarydump = "yes"
        else:
            self._output_binarydump = "no"
   
    @finemesh_gridlines.setter
    def finemesh_gridlines(self, value):
        """
        Sets the number of fine-mesh gridlines around the aerofoil.
        
        Parameters
        ----------
        value : int, None
        
        Raises
        ------
        ValueError
            The number of fine-mesh gridlines must be an integer in the range 
            96, 97, ..., 169.
        """
        if value is None:
            self._finemesh_gridlines = "d"
        elif 96 <= value <= 169 and isinstance(value, int):
            self._change_defaults = True
            self._finemesh_gridlines = value
        else:
            raise ValueError(
                "Number of fine-mesh gridlines must be in the range "
                "96, 97, ..., 160."
            )
    
    @coarsemesh_iterations.setter
    def coarsemesh_iterations(self, value):
        """
        Sets the number of coarse-mesh iterations.
        
        Parameters
        ----------
        value : int, None
        
        Raises
        ------
        ValueError
            The number of coarse-mesh iterations must be a positive integer.
        """
        if value is None:
            self._coarsemesh_iterations = "d"
        elif 0 < value and isinstance(value, int):
            self._change_defaults = True
            self._coarsemesh_iterations = value
        else:
            raise ValueError("Number of coarse-mesh iterations must be > 0.")
    
     @finemesh_iterations.setter
     def finemesh_iterations(self, value):
        """
        Sets the number of fine-mesh iterations.
        
        Parameters
        ----------
        value : int
        
        Raises
        ------
        ValueError
            The number of fine-mesh iterations must be a positive integer.
        """
        if value is None:
            self._finemesh_iterations = "d"
        elif 0 < value and isinstance(value, int):
            self._change_defaults = True
            self._finemesh_iterations = value
        else:
            raise ValueError("Number of fine-mesh iterations must be > 0.")
       
    @overrelaxation.setter
    def overrelaxation(self, relaxation):
        """
        Sets the over-relaxation parameter.
        
        Parameters
        ----------
        relaxation : float
        
        Raises
        ------
        ValueError
            The over-relaxation parameter must be in the range [0, 2].
        """
        if relaxation is None:
            self._overrelaxation = "d"
        elif 0 <= relaxation <= 2:
            self._change_defaults = True
            self._overrelaxation = relaxation
        else:
            # TODO(ns354) Check this range vvv.
            raise ValueError("Over-relaxation parameter must be in [0, 2].")
    
    @underrelaxation.setter
    def underrelaxation(self, relaxation):
        """
        Sets the under-relaxation parameter`.
        
        Parameters
        ----------
        relaxation : float or None
        
        Raises
        ------
        ValueError
            The under-relaxation parameter must be in the range (0, 1].
        """
        if relaxation is None:
            self._underrelaxation = "d"
        elif 0 < relaxation <= 1:
            self._change_defaults = True
            self._underrelaxation = relaxation
        else:
            raise ValueError("Under-relaxation parameter must be in (0, 1].")
    
    @coarse_relaxation_factor.setter
    def coarse_relaxation_factor(self, relaxation):
        """
        Sets the coarse-mesh relaxation factor at the boundary-layer.
        
        Parameters
        ----------
        relaxation : float or None
        
        Raises
        ------
        ValueError
            The coarse-mesh relaxation factor must be in the range (0.0, 0.5].
        """
        if relaxation is None:
            self._coarse_relaxation_factor = "d"
        elif 0 < relaxation <= 0.5:
            self._change_defaults = True
            self._coarse_relaxation_factor = relaxation
        else:
            raise ValueError(
                "Coarse-mesh relaxation-factor must be in (0.0, 0.5], but {} "
                "given.".format(relaxation)
            )
    
    # TODO(ns354) update naming to `coarse-mesh`.
    @niterations_coarse_inviscid_flow.setter
    def niterations_inviscid_flow(self, niterations):
        """
        Sets the number of inviscid flow iterations between successive boundary
        layer calculations for the coarse mesh.
        
        Parameters
        ----------
        niterations : int or None
        
        Raises
        ------
        ValueError
            Number of iterations is either non-interger or outside of the range
            1, 2, ..., 20.
        """
        if niterations is None:
            self._niterations_coarse_inviscid_flow = "d"
        elif 0 < niterations <= 20 and isinstance(niterations, int):
            self._change_defaults = True
            self._niterations_coarse_inviscid_flow = niterations
        else:
            raise ValueError(
                "Number of coarse-mesh inviscid flow iterations must be in "
                "{{1, 2, ..., 20}}, but {} given.".format(niterations)
            )
    
    @niterations_fine_inviscid_flow.setter
    def niterations_fine_inviscid_flow(self, niterations):
        """
        Sets the number of fine-mesh inviscid flow iterations between 
        successive boundary layer calculations.
        
        Parameters
        ----------
        niterations : int or None
        
        Raises
        ------
        ValueError
            Number of iterations is either non-integer or outside of the range
            1, 2, ..., 20.
        """
        if niterations is None:
            self._niterations_fine_inviscid_flow = "d"
        if 0 < niterations <= 20 and isinstance(niterations, int):
            self._change_defaults = True
            self._niterations_fine_inviscid_flow = niterations
        else:
            raise ValueError(
                "Number of fine-mesh inviscid flow iterations must be in "
                "{{1, 2, ..., 20}}, but {} given.".format(niterations)
            )
            
    @fine_relaxation_factor.setter
    def fine_relaxation_factor(self, relaxation):
        """
        Sets the fine-mesh relaxation factor at the boundary-layer.
        
        Parameters
        ----------
        relaxation : float or None
        
        Raises
        ------
        ValueError
            The fine-mesh relaxation factor must be in the range (0.0, 0.5].
        """
        if relaxation is None:
            self._fine_relaxation_factor = "d"
        elif 0 < relaxation <= 0.5:
            self._change_defaults = True
            self._fine_relaxation_factor = relaxation
        else:
            raise ValueError(
                "Fine-mesh relaxation factor must be in (0.0, 0.5]."
            )
    
    @dd21.setter
    def dd21(self, increment):
        """
        Sets the increment in non-dimensional momentum thickness at the 
        upper-layer transition boundary location (XTU).
        
        Parameters
        ----------
        increment : float or None
        
        Raises
        ------
        ValueError
            The incrememnt value is not in the range [0.00, 0.01].
        """
        if increment is None:
            self._dd21 = "d"
        if 0 <= increment <= 0.01:
            self._change_defaults = True
            self._dd21 = increment
        else:
            raise ValueError(
                "Increment in non-dimensional momentum thickness at XTU must "
                "be in [0.00, 0.01], but {} given.".format(increment)
            )
    
    @dd22.setter
    def dd22(self, increment):
        """
        Sets the increment in non-dimensional momentum thickness at the 
        lower-layer transition boundary location (XTL).
        
        Parameters
        ----------
        increment : float or None
        """
        if dd22 is None:
            self._dd22 = "d"
        if 0 <= increment <= 0.01:
            self._change_defaults = True
            self._dd22 = increment
        else:
            raise ValueError(
                "Increment in non-dimensional momentum thickness at XTL must "
                "be in [0, 0.01], but {} given.".format(increment)
            )
    
    @artificial_viscosity.setter
    def artificial_viscosity(self, viscosity):
        """
        Sets the artificial viscosity parameter, `ep`.
        
        Parameters
        ----------
        viscosity : float or None
        
        Raises
        ------
        ValueError
            Artificial viscosity parameter is not in the range [0, 1].
        """
        if viscosity is None:
            self._artificial_viscosity = "d"
        elif 0 <= viscosity <= 1:
            self._change_defaults = True
            self._artificial_viscosity = viscosity
        else:
            raise ValueError(
                "Artificial viscosity parameter must be in [0, 1], but {} "
                "given.".format(viscosity)
            )
    
    @partially_conservative.setter
    def partially_conservative(self, value):
        """
        Sets the partially-conservative parameter.
        
        Parameters
        ----------
        value : float or None
        
        Raises
        ------
        ValueError
            Partially-conservative parameter is not in the range [0, 1].
        """
        if value is None:
            self._partially_conservative = "d"
        if 0 <= value <= 1:
            self._change_defaults = True
            self._partially_conservative = value
        else:
            raise ValueError(
                "Partially-conservative parameter is not in the range [0, 1], "
                "but {} given.".format(value)
            )