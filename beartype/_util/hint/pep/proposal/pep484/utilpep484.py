#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2014-2024 Beartype authors.
# See "LICENSE" for further details.

'''
Project-wide :pep:`484`-compliant type hint utilities.

This private submodule is *not* intended for importation by downstream callers.
'''

# ....................{ IMPORTS                            }....................
from beartype.meta import URL_PEP585_DEPRECATIONS
from beartype.roar import BeartypeDecorHintPep585DeprecationWarning
from beartype._cave._cavefast import NoneType
from beartype._data.hint.pep.datapeprepr import (
    HINTS_PEP484_REPR_PREFIX_DEPRECATED)
from beartype._util.error.utilerrwarn import issue_warning

# Intentionally import PEP 484-compliant "typing" type hint factories rather
# than possibly PEP 585-compliant "beartype.typing" type hint factories.
from typing import Tuple

# ....................{ HINTS                              }....................
HINT_PEP484_TUPLE_EMPTY = Tuple[()]
'''
:pep:`484`-compliant empty fixed-length tuple type hint.
'''

# ....................{ TESTERS                            }....................
#FIXME: Remove this *AFTER* properly supporting type variables. For now,
#ignoring type variables is required ta at least shallowly support generics
#parametrized by one or more type variables.
def is_hint_pep484_typevar_ignorable(hint: object) -> bool:
    '''
    :data:`True` unconditionally.

    This tester currently unconditionally ignores *all* :pep:`484`-compliant
    type variables, which require non-trivial and currently unimplemented
    code generation support.

    This tester is intentionally *not* memoized (e.g., by the
    ``callable_cached`` decorator), as this tester is only safely callable by
    the memoized parent
    :func:`beartype._util.hint.utilhinttest.is_hint_ignorable` tester.

    Parameters
    ----------
    hint : object
        Type hint to be inspected.

    Returns
    -------
    bool
        :data:`True` only if this :pep:`484`-compliant type hint is ignorable.
    '''

    # Ignore *ALL* PEP 484-compliant type variables.
    return True

# ....................{ REDUCERS                           }....................
def reduce_hint_pep484_deprecated(
    hint: object, exception_prefix : str, *args, **kwargs) -> object:
    '''
    Preserve the passed :pep:`484`-compliant type hint as is while emitting one
    non-fatal deprecation warning for this type hint if **deprecated** (i.e.,
    obsoleted by an equivalent :pep:`585`-compliant type hint *and* the active
    Python interpreter targets Python >= 3.9).

    While *not* explicitly defined by the :mod:`typing` module, :pep:`484`
    explicitly supports this singleton:

        When used in a type hint, the expression :data:`None` is considered
        equivalent to ``type(None)``.

    This reducer is intentionally *not* memoized (e.g., by the
    ``callable_cached`` decorator), as the implementation trivially reduces
    to an efficient one-liner.

    Parameters
    ----------
    hint : object
        Type hint to be reduced.
    exception_prefix : str, optional
        Human-readable label prefixing the representation of this object in the
        warning message. Defaults to the empty string.

    All remaining passed arguments are silently ignored.

    Returns
    -------
    object
        This hint unmodified.

    Warns
    -----
    BeartypeDecorHintPep585DeprecationWarning
        If this :pep:`484`-compliant type hint is deprecated by :pep:`585` *and*
        the active Python interpreter targets Python >= 3.9.
    '''
    assert isinstance(exception_prefix, str), (
        f'{repr(exception_prefix)} not string.')
    # print(f'Testing PEP 484 type hint {repr(hint)} for PEP 585 deprecation...')
    # print(f'{HINTS_PEP484_REPR_PREFIX_DEPRECATED}')

    # Avoid circular import dependencies.
    from beartype._util.hint.utilhintget import get_hint_repr

    # Machine-readable representation of this hint.
    hint_repr = get_hint_repr(hint)

    # Substring of the machine-readable representation of this hint preceding
    # the first "[" delimiter if this representation contains that delimiter
    # *OR* this representation as is otherwise.
    #
    # Note that the str.partition() method has been profiled to be the optimally
    # efficient means of parsing trivial prefixes.
    hint_repr_bare, _, _ = hint_repr.partition('[')

    # If this hint is a PEP 484-compliant type hint originating from an origin
    # type (e.g., "typing.List[int]"), this hint has been deprecated by the
    # equivalent PEP 585-compliant type hint (e.g., "list[int]"). In this case,
    # emit a non-fatal PEP 585-specific deprecation warning.
    if hint_repr_bare in HINTS_PEP484_REPR_PREFIX_DEPRECATED:
        issue_warning(
            cls=BeartypeDecorHintPep585DeprecationWarning,
            message=(
                f'{exception_prefix}PEP 484 type hint {repr(hint)} '
                f'deprecated by PEP 585. '
                f'This hint is scheduled for removal in the first Python '
                f'version released after October 5th, 2025. To resolve this, '
                f'import this hint from "beartype.typing" rather than "typing". '
                f'For further commentary and alternatives, see also:\n'
                f'    {URL_PEP585_DEPRECATIONS}'
            ),
        )
    # Else, this hint is *NOT* deprecated. In this case, reduce to a noop.

    # Preserve this hint as is, regardless of deprecation.
    return hint


# Note that this reducer is intentionally typed as returning "type" rather than
# "NoneType". While the former would certainly be preferable, mypy erroneously
# emits false positives when this reducer is typed as returning "NoneType":
#     beartype/_util/hint/pep/proposal/pep484/utilpep484.py:190: error: Variable
#     "beartype._cave._cavefast.NoneType" is not valid as a type [valid-type]
def reduce_hint_pep484_none(hint: object, *args, **kwargs) -> type:
    '''
    Reduce the passed :pep:`484`-compliant :data:`None` type hint to the type of
    that type hint (i.e., the builtin :class:`types.NoneType` class).

    While *not* explicitly defined by the :mod:`typing` module, :pep:`484`
    explicitly supports this singleton:

        When used in a type hint, the expression :data:`None` is considered
        equivalent to ``type(None)``.

    This reducer is intentionally *not* memoized (e.g., by the
    ``callable_cached`` decorator), as the implementation trivially reduces
    to an efficient one-liner.

    Parameters
    ----------
    hint : object
        Type variable to be reduced.

    All remaining passed arguments are silently ignored.

    Returns
    -------
    NoneType
        Type of the :data:`None` singleton.
    '''
    assert hint is None, f'Type hint {hint} not "None" singleton.'

    # Unconditionally return the type of the "None" singleton.
    return NoneType
