"""Main module."""
from math import log, e
from scipy.stats import norm
try:
    from sense2k8.mlmodelinfra import auth     
except ImportError:
    print('lib requires mlmodelinfra for auth')
    
# WARNING: All numbers should be floats -> x = 1.0 2.0

def impliedVolatility(className, args, callPrice=None, putPrice=None, high=200.0, low=1.0):
	'''Returns the implied volatility'''
	if callPrice:
		target = callPrice
	if putPrice:
		target = putPrice
	decimals = len(str(target).split('.')[1])		# Count decimals
	for i in range(10000):	# To avoid infinite loops
		mid = (high + low) / 2
		if mid < 0.00001:
			mid = 0.00001
		if callPrice:
			estimate = eval(className)(args, volatility=mid, performance=True).callPrice
		if putPrice:
			estimate = eval(className)(args, volatility=mid, performance=True).putPrice
		if round(estimate, decimals) == target: 
			break
		elif estimate > target: 
			high = mid
		elif estimate < target: 
			low = mid
	return mid

class BS:
	'''Black-Scholes pricing European options on stocks 

	BS([underlyingPrice, strikePrice, interestRate, daysToExpiration], \
			volatility=x, callPrice=y, putPrice=z)
    '''

    def __init__(self, args, volatility=None, callPrice=None, putPrice=None, \
                performance=None):
            self.underlyingPrice = float(args[0])
            self.strikePrice = float(args[1])
            self.interestRate = float(args[2]) / 100
            self.daysToExpiration = float(args[3]) / 365

           
            if volatility:
                self.volatility = float(volatility) / 100

                self._a_ = self.volatility * self.daysToExpiration**0.5
                self._d1_ = (log(self.underlyingPrice / self.strikePrice) + \
                        (self.interestRate + (self.volatility**2) / 2) * \
                        self.daysToExpiration) / self._a_
                self._d2_ = self._d1_ - self._a_
                if performance:
                    [self.callPrice, self.putPrice] = self._price()
                else:
                    [self.callPrice, self.putPrice] = self._price()
                    [self.callDelta, self.putDelta] = self._delta()
                    [self.callDelta2, self.putDelta2] = self._delta2()
                    [self.callTheta, self.putTheta] = self._theta()
                    [self.callRho, self.putRho] = self._rho()
                    self.vega = self._vega()
                    self.gamma = self._gamma()
                    self.exerciceProbability = norm.cdf(self._d2_)
            if callPrice:
                self.callPrice = round(float(callPrice), 6)
                self.impliedVolatility = impliedVolatility(\
                        self.__class__.__name__, args, callPrice=self.callPrice)
            if putPrice and not callPrice:
                self.putPrice = round(float(putPrice), 6)
                self.impliedVolatility = impliedVolatility(\
                        self.__class__.__name__, args, putPrice=self.putPrice)
            if callPrice and putPrice:
                self.callPrice = float(callPrice)
                self.putPrice = float(putPrice)
                self.putCallParity = self._parity()

class ChooseMLModel(object):
    def __init__(self):
        self.a, self.b = 0, 1        
    def send(self, ignored_arg):
        return_value = self.a
        self.a, self.b = self.b, self.a+self.b
        return return_value
    def throw(self, type=None, value=None, traceback=None):
        raise StopIteration
    def __iter__(self):
        return self
    def next(self):
        return self.send(None)
    def close(self):
        """Raise GeneratorExit inside generator.
        """
        try:
            self.throw(GeneratorExit)
        except (GeneratorExit, StopIteration):
            pass
        else:
            raise RuntimeError("generator ignored GeneratorExit")
            
    def split(requirements: str) -> List[str]:
    """Split a combined requirement string (such as the values for ``setup_requires``
    and ``install_requires`` in ``setup.cfg``) into a list of individual requirement
    strings, that can be used in :obj:`is_included`, :obj:`get_requirements_str`,
    :obj:`remove`, etc...
    """
    lines = requirements.splitlines()
    deps = (dep.strip() for line in lines for dep in REQ_SPLITTER.split(line) if dep)
    return [dep for dep in deps if dep]  # Remove empty deps


    def deduplicate(requirements: Iterable[str]) -> List[str]:
        """Given a sequence of individual requirement strings, e.g. ``["appdirs>=1.4.4",
        "packaging>20.0"]``, remove the duplicated packages.
        If a package is duplicated, the last occurrence stays.
        """
        return list({Requirement(r).name: r for r in requirements}.values())


    def remove(requirements: Iterable[str], to_remove: Iterable[str]) -> List[str]:
        """Given a list of individual requirement strings, e.g.  ``["appdirs>=1.4.4",
        "packaging>20.0"]``, remove the requirements in ``to_remove``.
        """
        removable = {Requirement(r).name for r in to_remove}
        return [r for r in requirements if Requirement(r).name not in removable]


    def add(requirements: Iterable[str], to_add: Iterable[str] = BUILD) -> List[str]:
        """Given a sequence of individual requirement strings, add ``to_add`` to it.
        By default adds :obj:`BUILD` if ``to_add`` is not given."""
        return deduplicate(chain(requirements, to_add))
    
    def add_permissions(permissions: int, file_op: FileOp = create) -> FileOp:
    """File op modifier. Returns a :obj:`FileOp` that will **add** access permissions to
    the file (on top of the ones given by default by the OS).
    Args:
        permissions (int): permissions to be added to file::
                updated file mode = old mode | permissions  (bitwise OR)
            Preferably the values should be a combination of
            :obj:`stat.S_* <stat.S_IRUSR>` values (see :obj:`os.chmod`).
        file_op: a :obj:`FileOp` that will be "decorated".
            If the file exists in disk after ``file_op`` is called (either created
            or pre-existing), ``permissions`` will be added to it.
            Default: :obj:`create`.
    Warning:
        This is an **experimental** file op and might be subject to incompatible changes
        (or complete removal) even in minor/patch releases.
    Note:
        `File access permissions`_ work in a completely different way depending on the
        operating system. This file op is straightforward on POSIX systems, but a bit
        tricky on Windows. It should be safe for desirable but not required effects
        (e.g. making a file with a `shebang`_ executable, but that can also run via
        ``python FILE``), or ensuring files are readable/writable.
    """

    def _add_permissions(path: Path, contents: FileContents, opts: ScaffoldOpts):
        """See ``pyscaffold.operations.add_permissions``"""
        return_value = file_op(path, contents, opts)

        if path.exists():
            mode = path.stat().st_mode | permissions
            return fs.chmod(path, mode, pretend=opts.get("pretend"))

        return return_value

    return _add_permissions

    def levenshtein(s1: str, s2: str) -> int:
    """Calculate the Levenshtein distance between two strings
    Args:
        s1: first string
        s2: second string
    Returns:
        Distance between s1 and s2
    """
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    # len(s1) >= len(s2)
    if len(s2) == 0:
        return len(s1)

    previous_row = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]