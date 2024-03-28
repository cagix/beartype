#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2014-2024 Beartype authors.
# See "LICENSE" for further details.

'''
Project-wide :pep:`563` **resolver** data submodule.

This submodule defines callables annotated by :pep:`563`-postponed type hints
under the ``from __future__ import annotations`` pragma, intended to be
externally imported and called from unit tests elsewhere in this test suite.

Caveats
-------
**Callables and classes defined below are intentionally not decorated by the**
:func:`beartype.beartype` **decorator.** Why? Because that decorator internally
calls the :func:`beartype.peps.resolve_pep563` resolver. However, the whole
point of this submodule is to explicitly call and thus exercise that resolver!
'''

# ....................{ IMPORTS                            }....................
from __future__ import annotations
from beartype.door import die_if_unbearable
from beartype.typing import Generic
from beartype._data.hint.datahinttyping import T

# ....................{ CLASSES                            }....................
class ToAvariceOrPride(Generic[T]):
    '''
    Arbitrary generic.
    '''

    pass


class FrequentWith(object):
    '''
    Arbitrary class defining various problematic methods.
    '''

    # ....................{ CLASS METHODS                  }....................
    @classmethod
    def until_the_doves(
        cls, and_squirrels_would_partake: ExpandAbove) -> ExpandAbove:
        '''
        Arbitrary **annotated class method** (i.e., class method annotated by
        one or more type hints), exercising an edge case in the
        :func:`beartype.peps.resolve_pep563` resolver.
        '''

        # Subscripted generic type alias, resolved to this global attribute that
        # has yet to be defined by the resolve_pep563() function called by the
        # caller.
        ExpandAbove_resolved = (
            FrequentWith.until_the_doves.__func__.__annotations__[
                'and_squirrels_would_partake'])

        # If this parameter violates this type, raise an exception.
        die_if_unbearable(and_squirrels_would_partake, ExpandAbove_resolved)

        # Return this parameter as is.
        return and_squirrels_would_partake

    # ....................{ METHODS                        }....................
    def crystal_column(self, and_clear_shrines: OfPearl) -> OfPearl:
        '''
        Arbitrary method both accepting and returning a value annotated as a
        **missing forward reference** (i.e., :pep:`563`-postponed type hint
        referring to a global attribute that is guaranteed to *never* be defined
        by this submodule), exercising an edge case in the
        :func:`beartype.peps.resolve_pep563` resolver.

        Raises
        ------
        BeartypeCallHintForwardRefException
            Unconditionally.
        '''

        # Missing forward reference, defined merely as a placeholder forward
        # reference proxy after the caller passes this method to the
        # resolve_pep563() function.
        OfPearl_resolved = FrequentWith.crystal_column.__annotations__[
            'and_clear_shrines']

        # Raise an exception. Since this forward reference is guaranteed to be
        # missing, this call is guaranteed to fail.
        die_if_unbearable(and_clear_shrines, OfPearl_resolved)

        # Return this parameter as is.
        return and_clear_shrines

# ....................{ FUNCTIONS                          }....................
def their_starry_domes(of_diamond_and_of_gold: ExpandAbove) -> ExpandAbove:
    '''
    Arbitrary function both accepting and returning a value annotated as a
    **subscripted generic type alias forward reference** (i.e.,
    :pep:`563`-postponed type hint referring to a global attribute that has yet
    to be defined whose value is a subscripted generic that *has* been defined),
    exercising an edge case in the :func:`beartype.peps.resolve_pep563`
    resolver.

    Raises
    ------
    BeartypeDecorHintForwardRefException
        If this function has yet to be passed to the
        :func:`beartype.peps.resolve_pep563` resolver.
    '''

    # Subscripted generic type alias, resolved to this global attribute that has
    # yet to be defined by the resolve_pep563() function called by the caller.
    ExpandAbove_resolved = their_starry_domes.__annotations__[
        'of_diamond_and_of_gold']

    # If this parameter violates this subscripted generic, raise an exception.
    die_if_unbearable(of_diamond_and_of_gold, ExpandAbove_resolved)

    # Return this parameter as is.
    return of_diamond_and_of_gold

# ....................{ HINTS                              }....................
ExpandAbove = ToAvariceOrPride[str]
'''
Arbitrary **subscripted generic type alias forward reference** (i.e.,
:pep:`563`-postponed type hint referring to a global attribute that has yet to
be defined whose value is a subscripted generic that *has* been defined),
'''
