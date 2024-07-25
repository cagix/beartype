#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2014-2024 Beartype authors.
# See "LICENSE" for further details.

'''
Beartype **warning hierarchy** (i.e., public and private warning subclasses
emitted at decoration, call, and usage time by :mod:`beartype`).

This private submodule is *not* intended for importation by downstream callers.
'''

# ....................{ IMPORTS                            }....................
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# WARNING: To avoid polluting the public module namespace, external attributes
# should be locally imported at module scope *ONLY* under alternate private
# names (e.g., "from argparse import ArgumentParser as _ArgumentParser" rather
# than merely "from argparse import ArgumentParser").
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
from abc import ABCMeta as _ABCMeta

# ....................{ SUPERCLASS                         }....................
class BeartypeWarning(UserWarning, metaclass=_ABCMeta):
    '''
    Abstract base class of all **beartype warnings.**

    Instances of subclasses of this warning are emitted either:

    * At decoration time from the :func:`beartype.beartype` decorator.
    * At call time from the new callable generated by the
      :func:`beartype.beartype` decorator to wrap the original callable.
    * At Sphinx-based documentation building time from Python code invoked by
      the ``doc/Makefile`` file.
    '''

    # ..................{ INITIALIZERS                       }..................
    def __init__(self, message: str) -> None:
        '''
        Initialize this exception.

        This constructor (in order):

        #. Passes all passed arguments as is to the superclass constructor.
        #. Sanitizes the fully-qualified module name of this
           exception from the private ``"beartype.roar._roarwarn"`` submodule
           to the public ``"beartype.roar"`` subpackage to both improve the
           readability of exception messages and discourage end users from
           accessing this private submodule.
        '''

        # Defer to the superclass constructor.
        super().__init__(message)

        # Sanitize the fully-qualified module name of the class of this
        # warning. See the docstring for justification.
        self.__class__.__module__ = 'beartype.roar'

# ....................{ CLAW                               }....................
class BeartypeClawWarning(BeartypeWarning):
    '''
    Abstract base class of all **beartype import hook warnings.**

    Instances of subclasses of this warning are emitted at module importation
    time from the import hooks registered by the :func:`beartype.claw`
    subpackage, typically due to the :func:`beartype.beartype` decorator failing
    to decorate callables or classes in modules imported by those hooks.
    '''

    pass


class BeartypeClawDecorWarning(BeartypeClawWarning):
    '''
    **Beartype import hook decoration warning.**

    This warning is emitted at module importation time from the import hooks
    registered by the :func:`beartype.claw` subpackage when the
    :func:`beartype.beartype` decorator fails to decorate a callable or class
    declared in a module imported by those hooks.
    '''

    pass

# ....................{ CONF                               }....................
class BeartypeConfWarning(BeartypeWarning):
    '''
    Abstract base class of all **beartype configuration warnings.**

    Instances of subclasses of this warning are emitted by the
    :class:`beartype.BeartypeConf` class to inform the user of various non-fatal
    edge cases concerning beartype configuration.
    '''

    pass


class BeartypeConfShellVarWarning(BeartypeConfWarning):
    '''
    **Beartype configuration shell environment variable warning.**

    Instances of this warning are emitted at instantiation time of the
    :class:`beartype.BeartypeConf` class when the caller erroneously sets a
    shell environment variable recognized by that class (e.g.,
    ``${BEARTYPE_IS_COLOR}``) to an valid value conflicting with that of a
    corresponding parameter also passed to that class (e.g., ``is_color``).
    '''

    pass

# ....................{ DECORATOR ~ hint                   }....................
class BeartypeDecorHintWarning(BeartypeWarning):
    '''
    Abstract base class of all **beartype decorator type hint warnings.**

    Instances of subclasses of this warning are emitted at decoration time from
    the :func:`beartype.beartype` decorator on receiving a callable annotated
    by a suspicious (but *not* necessarily erroneous) type hint warranting
    non-fatal warnings *without* raising fatal exceptions.
    '''

    pass



class BeartypeDecorHintParamDefaultForwardRefWarning(BeartypeDecorHintWarning):
    '''
    **Beartyped decorator optional parameter default value type-checking
    forward reference warning.**

    This exception is raised at decoration time by the :func:`beartype.beartype`
    decorator when the default value of an optional parameter of a decorated
    callable is *not* type-checkable against the type hint annotating that
    parameter, due to that type hint containing a forward reference to a
    user-defined object that is undefined at that decoration time.
    '''

    pass

# ....................{ DECORATOR ~ hint : pep             }....................
class BeartypeDecorHintPepWarning(BeartypeDecorHintWarning):
    '''
    Abstract base class of all **beartype decorator PEP-compliant type hint
    warnings.**

    Instances of subclasses of this warning are emitted at decoration time from
    the :func:`beartype.beartype` decorator on receiving a callable annotated
    by a suspicious (but *not* necessarily erroneous) PEP-compliant type hint
    warranting non-fatal warnings *without* raising fatal exceptions.
    '''

    pass


#FIXME: Consider removal.
# class BeartypeDecorHintPepIgnorableDeepWarning(BeartypeDecorHintPepWarning):
#     '''
#     **Beartype decorator deeply ignorable PEP-compliant type hint warning.**
#
#     This warning is emitted at decoration time from the
#     :func:`beartype.beartype` decorator on receiving a callable annotated by
#     one or more **deeply ignorable PEP-compliant type hints** (i.e., instances or classes declared
#     by the stdlib :mod:`typing` module) currently unsupported by this
#     decorator.
#     '''
#
#     pass


#FIXME: Consider removal.
# class BeartypeDecorHintPepUnsupportedWarning(BeartypeWarning):
#     '''
#     **Beartype decorator unsupported PEP-compliant type hint warning.**
#
#     This warning is emitted at decoration time from the
#     :func:`beartype.beartype` decorator on receiving a callable annotated with
#     one or more PEP-compliant type hints (e.g., instances or classes declared
#     by the stdlib :mod:`typing` module) currently unsupported by this
#     decorator.
#     '''
#
#     pass

# ....................{ DECORATOR ~ hint : pep : deprecate }....................
class BeartypeDecorHintPepDeprecationWarning(
    BeartypeDecorHintPepWarning, DeprecationWarning):
    '''
    **Beartype decorator PEP-compliant type hint deprecation warning.**

    This warning is emitted at decoration time from the
    :func:`beartype.beartype` decorator on receiving a callable annotated by one
    or more **deprecated PEP-compliant type hints** (i.e., type hints compliant
    with outdated PEPs that have since been obsoleted by recent PEPs),
    including:

    * If the active Python interpreter targets at least Python >= 3.9 and thus
      supports :pep:`585`, outdated :pep:`484`-compliant type hints (e.g.,
      ``typing.List[int]``) that have since been obsoleted by the equivalent
      :pep:`585`-compliant type hints (e.g., ``list[int]``).
    '''

    pass


#FIXME: This should *REALLY* have been called
#"BeartypeDecorHintPep484DeprecationWarning". Oh well. Let's preserve backward
#compatibility by just accepting this as is. This goes away in 2026, anyway.
class BeartypeDecorHintPep585DeprecationWarning(
    BeartypeDecorHintPepDeprecationWarning):
    '''
    **Beartype decorator** :pep:`585`-mandated **deprecation of**
    :pep:`484`-compliant **type hint warning.**

    This warning is emitted at decoration time from the
    :func:`beartype.beartype` decorator on receiving a callable annotated by
    one or more outdated :pep:`484`-compliant type hints (e.g.,
    ``typing.List[int]``) that have since been obsoleted by the equivalent
    :pep:`585`-compliant type hints (e.g., ``list[int]``) if the active Python
    interpreter targets at least Python >= 3.9 and thus supports :pep:`585`.

    See Also
    --------
    https://github.com/beartype/beartype#pep-585-deprecations
        Further discussion
    '''

    pass


class BeartypeDecorHintPep613DeprecationWarning(
    BeartypeDecorHintPepDeprecationWarning):
    '''
    **Beartype decorator** :pep:`613`-compliant **type hint warning.**

    This warning is emitted at decoration time from the
    :func:`beartype.beartype` decorator on receiving a callable annotated by
    one or more outdated :pep:`613`-compliant **type aliases** (i.e.,
    :obj:`typing.TypeAlias` type hint singletons) that have since been obsoleted
    by the equivalent :pep:`695`-compliant type aliases (e.g., ``type alias =
    list[int]``) if the active Python interpreter targets at least Python >=
    3.10 and thus supports :pep:`613`.
    '''

    pass

# ....................{ DECORATOR ~ hint : non-pep         }....................
class BeartypeDecorHintNonpepWarning(BeartypeWarning):
    '''
    Abstract base class of all **beartype decorator PEP-noncompliant type hint
    warnings.**

    Instances of subclasses of this warning are emitted at decoration time from
    the :func:`beartype.beartype` decorator on receiving a callable annotated
    by a suspicious (but *not* necessarily erroneous) PEP-noncompliant type
    hint warranting non-fatal warnings *without* raising fatal exceptions.
    '''

    pass


class BeartypeDecorHintNonpepNumpyWarning(BeartypeDecorHintNonpepWarning):
    '''
    **Beartype decorator PEP-noncompliant NumPy type hint warning.**

    This exception is raised at decoration time from the
    :func:`beartype.beartype` decorator on receiving a callable annotated by an
    suspicious NumPy type hint, including:

    * **Typed NumPy arrays** (i.e., ``numpy.typed.NDArray[...]`` type hints)
      under Python < 3.8, which this decorator currently reduces to
      **untyped NumPy arrays** (i.e., :class:`numpy.ndarray`).
    '''

    pass

# ....................{ MODULE                             }....................
class BeartypeModuleWarning(BeartypeWarning):
    '''
    Abstract base class of all **beartype module warnings.**

    Instances of subclasses of this warning are emitted at various times
    (including at decoration time from the :func:`beartype.beartype` decorator)
    on failing to import optional third-party modules, packages, or C
    extensions warranting non-fatal warnings *without* raising fatal
    exceptions.
    '''

    pass


class BeartypeModuleNotFoundWarning(BeartypeModuleWarning):
    '''
    **Beartype missing optional dependency warning.**

    This warning is emitted at various times to inform the user of a **missing
    recommended optional dependency** (i.e., third-party Python package *not*
    installed under the active Python interpreter whose installation is
    technically optional but recommended).
    '''

    pass


class BeartypeModuleAttributeNotFoundWarning(BeartypeModuleWarning):
    '''
    **Beartype missing optional dependency attribute warning.**

    This warning is emitted at various times to inform the user of a **missing
    recommended optional dependency attribute** (i.e., attribute *not* defined
    by a third-party Python package installed under the active Python
    interpreter whose installation is technically optional but recommended,
    typically due to the currently installed version of that package being
    unexpectedly old and thus failing to define an attribute defined by modern
    versions of that package).
    '''

    pass


class BeartypeModuleUnimportableWarning(BeartypeModuleWarning):
    '''
    **Beartype unimportable optional dependency warning.**

    This warning is emitted at various times to inform the user of an
    **unimportable optional dependency** (i.e., third-party Python package
    installed under the active Python interpreter but which raises unexpected
    exceptions from module scope when imported).
    '''

    pass

# ....................{ DOOR                               }....................
class BeartypeDoorWarning(BeartypeWarning):
    '''
    Abstract base class of all **beartype Decidedly Object-Oriented
    Runtime-checking (DOOR) warnings.**

    Instances of subclasses of this warning are emitted at usage (e.g.,
    instantiation, method call) time from functionality published by the
    :func:`beartype.door` subpackage, typically due to suspicious (but *not*
    necessarily erroneous) PEP-compliant type hints warranting non-fatal
    warnings *without* raising fatal exceptions.
    '''

    pass


class BeartypeDoorInferHintWarning(BeartypeDoorWarning):
    '''
    Abstract base class of all **beartype Decidedly Object-Oriented
    Runtime-checking (DOOR) type hint inference warnings.**

    Instances of subclasses of this warning are emitted at usage (e.g.,
    instantiation, method call) time from the public
    :func:`beartype.door.infer_hint` function, typically due to suspicious (but
    *not* necessarily erroneous) PEP-compliant type hints warranting non-fatal
    warnings *without* raising fatal exceptions.
    '''

    pass


class BeartypeDoorInferHintRecursionWarning(BeartypeDoorInferHintWarning):
    '''
    **Beartype Decidedly Object-Oriented Runtime-checking (DOOR) type hint
    inference recursion warning.**

    This warning is emitted on passing the public
    :func:`beartype.door.infer_hint` function a **recursive object** (i.e., an
    object that self-referentially refers to itself, typically due to being a
    container containing one or more items that self-referentially refer to that
    same container).
    '''

    pass

# ....................{ VALE                               }....................
class BeartypeValeWarning(BeartypeWarning):
    '''
    Abstract base class of all **beartype data validation warnings.**

    Instances of subclasses of this warning are emitted at usage (e.g.,
    instantiation, method call) time from the class hierarchy published by the
    :func:`beartype.vale` subpackage by suspicious (but *not* necessarily
    erroneous) PEP-compliant type hints warranting non-fatal warnings *without*
    raising fatal exceptions.
    '''

    pass


class BeartypeValeLambdaWarning(BeartypeValeWarning):
    '''
    **Beartype data validation lambda function warning.**

    This warning is emitted on passing the :func:`repr` builtin an instance of
    the :class:`beartype.vale.Is` class subscripted by a lambda function whose
    definition is *not* parsable from the script or module file defining that
    lambda.
    '''

    pass

# ....................{ PRIVATE ~ conf                     }....................
class _BeartypeConfReduceDecoratorExceptionToWarningDefault(
    BeartypeConfWarning):
    '''
    Beartype
    :attr:`beartype.BeartypeConf.warning_cls_on_decorator_exception`
    **fake warning default.**

    This warning is *not* actually emitted at all anywhere but instead
    constitutes intentional design abuse of this submodule. Specifically, this
    warning is used as the default value for the public
    :attr:`beartype.BeartypeConf.warning_cls_on_decorator_exception`
    configuration parameter, enabling private functionality elsewhere to
    distinguish between the following two common cases:

    * A user does explicitly sets that parameter to :data:`None`, instructing
      the :func:`beartype.beartype` decorator to raise exceptions rather than
      emit warnings on decoration-time errors.
    * A user does *not* explicitly set that parameter, which then defaults to
      this fake warning category. Private functionality elsewhere then detects
      this default and conditionally sets that parameter to a meaningful default
      depending on the current context. As example, when *not* explicitly set by
      the user:

      * The :mod:`beartype.claw` API defaults that parameter to the public
        :class:`.BeartypeClawDecorWarning` warning category.
      * The :func:`beartype.beartype` decorator defaults that parameter to
        :data:`None`.

    This warning is doing the wrong things, but for the right reasons. Again,
    this warning is a placeholder that should *never* be emitted to end users.
    '''

    pass

# ....................{ PRIVATE ~ util                     }....................
class _BeartypeUtilWarning(BeartypeWarning):
    '''
    Abstract base class of all **beartype private utility warnings.**

    Instances of subclasses of this warning are emitted by *most* (but *not*
    all) private submodules of the private :mod:`beartype._util` subpackage.
    These warnings denote non-critical internal issues and should thus *never*
    be emitted, let alone allowed to percolate up the call stack to end users.
    '''

    pass

# ....................{ PRIVATE ~ util : call              }....................
class _BeartypeUtilCallableWarning(_BeartypeUtilWarning):
    '''
    Beartype **decorator memoization decorator keyword argument** warning.

    This warning is emitted from callables memoized by the
    :func:`beartype._util.cache.utilcachecall.callable_cached` decorator on
    calls receiving one or more keyword arguments. Memoizing keyword arguments
    is substantially more space- and time-intensive than memoizing the
    equivalent positional arguments, partially defeating the purpose of
    memoization in the first place.

    This warning denotes a critical internal issue and should thus *never* be
    emitted to end users.
    '''

    pass
