#!/usr/bin/env python3
# --------------------( LICENSE                            )--------------------
# Copyright (c) 2014-2024 Beartype authors.
# See "LICENSE" for further details.

'''
Beartype **Decidedly Object-Oriented Runtime-checking (DOOR) fixtures** (i.e.,
:mod:`pytest`-specific context managers passed as parameters to unit tests
exercising the :mod:`beartype.door` subpackage).
'''

# ....................{ IMPORTS                            }....................
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# WARNING: To raise human-readable test errors, avoid importing from
# package-specific submodules at module scope.
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
from pytest import fixture

# ....................{ FIXTURES ~ equality                }....................
@fixture(scope='session')
def door_cases_equality() -> 'Iterable[Tuple[object, object, bool]]':
    '''
    Session-scoped fixture returning an iterable of **hint equality cases**
    (i.e., 3-tuples ``(hint_a, hint_b, is_equal)`` describing the equality
    relations between two PEP-compliant type hints), efficiently cached across
    all tests requiring this fixture.

    This iterable is intentionally defined by the return of this fixture rather
    than as a global constant of this submodule. Why? Because the former safely
    defers all heavyweight imports required to define this iterable to the call
    of the first unit test requiring this fixture, whereas the latter unsafely
    performs those imports at pytest test collection time.

    Returns
    -------
    Iterable[Tuple[object, object, bool]]
        Iterable of one or more 3-tuples ``(hint_a, hint_b, is_equal)``,
        where:

        * ``hint_a`` is the PEP-compliant type hint to be passed as the first
          parameter to the :meth:`beartype.door.TypeHint.__equals__` tester.
        * ``hint_b`` is the PEP-compliant type hint to be passed as the second
          parameter to the :meth:`beartype.door.TypeHint.__equals__` tester.
        * ``is_equal`` is ``True`` only if these hints are equal according to
          that tester.
    '''

    # ..................{ IMPORTS                            }..................
    # Defer fixture-specific imports.
    from beartype._util.py.utilpyversion import IS_PYTHON_AT_LEAST_3_9
    from numbers import Number

    # Intentionally import from "typing" rather than "beartype.typing" to
    # guarantee PEP 484-compliant type hints.
    from typing import (
        Any,
        List,
        Tuple,
        Union,
    )

    # ..................{ LISTS                              }..................
    HINT_EQUALITY_CASES = [
        # ..................{ HINTS ~ argless : bare         }..................
        # PEP 484-compliant unsubscripted type hints, which are necessarily
        # equal to themselves.
        (tuple, Tuple, True),
        (list, list, True),
        (list, List, True),

        # ..................{ HINTS ~ arg : sequence         }..................
        # PEP 484-compliant sequence type hints.
        (list, List[Any], True),
        (tuple, Tuple[Any, ...], True),

        # ..................{ HINTS ~ arg : union            }..................
        # PEP 484-compliant union type hints.
        (Union[int, str], Union[str, list], False),
        (Union[Number, int], Union[Number, float], True),

        # Test that union equality ignores order.
        (Union[int, str], Union[str, int], True),

        # Test that union equality compares child type hints collectively rather
        # than individually.
        #
        # Note that this pair of cases tests numerous edge cases, including:
        # * Equality comparison of non-unions against unions. Although
        #   "Union[int]" superficially appears to be a union, Python reduces
        #   "Union[int]" to simply "int" at runtime.
        (Union[bool, int], Union[int], True),
        (Union[int], Union[bool, int], True),
    ]

    # If the active Python interpreter targets Python >= 3.9 and thus supports
    # both PEP 585 and 593...
    if IS_PYTHON_AT_LEAST_3_9:
        from beartype.typing import Annotated
        from collections.abc import (
            Awaitable as AwaitableABC,
            Sequence as SequenceABC,
        )

        # Append cases exercising version-specific relations.
        HINT_EQUALITY_CASES.extend((
            # PEP 585-compliant type hints.
            (tuple[str, ...], Tuple[str, ...], True),
            (list[str], List[str], True),
            (AwaitableABC[SequenceABC[int]], AwaitableABC[SequenceABC[int]], True),

            # PEP 593-compliant type hints.
            (Annotated[int, "hi"], Annotated[int, "hi"], True),
            (Annotated[int, "hi"], Annotated[int, "low"], False),
            (Annotated[int, "hi"], Annotated[int, "low"], False),
        ))

    # Return this mutable list coerced into an immutable tuple for safety.
    return tuple(HINT_EQUALITY_CASES)

# ....................{ FIXTURES ~ infer                   }....................
#FIXME: Actually leverage this in a unit test, please. *sigh*
@fixture(scope='session')
def door_cases_infer_hint() -> 'Iterable[Tuple[object, object]]':
    '''
    Session-scoped fixture returning an iterable of **type hint inference
    cases** (i.e., 2-tuples ``(obj, hint)`` describing the type hint matching an
    arbitrary object), efficiently cached across all tests requiring this
    fixture.

    This iterable is intentionally defined by the return of this fixture rather
    than as a global constant of this submodule. Why? Because the former safely
    defers all heavyweight imports required to define this iterable to the call
    of the first unit test requiring this fixture, whereas the latter unsafely
    performs those imports at pytest test collection time.

    Returns
    -------
    Iterable[Tuple[object, object]]
        Iterable of one or more 2-tuples ``(obj, hint)``, where:

        * ``obj`` is an arbitrary object to be passed as the first parameter to
          the :func:`beartype.door.infer_hint` function.
        * ``hint`` is the type hint returned by that function when passed that
          object.
    '''

    # ..................{ IMPORTS                            }..................
    # Defer fixture-specific imports.
    # from beartype._util.py.utilpyversion import IS_PYTHON_AT_LEAST_3_9
    from beartype.typing import (
        Deque,
        FrozenSet,
        KeysView,
        List,
        MutableSequence,
        Set,
        Tuple,
        Type,
        Union,
        ValuesView,
    )
    from beartype_test.a00_unit.data.data_type import (
        Class,
        ClassMutableSequence,
    )
    from beartype._util.py.utilpyversion import IS_PYTHON_AT_LEAST_3_10
    from collections import (
        deque,
    )

    # ..................{ LISTS ~ cases                      }..................
    # List of all type hint inference cases (i.e., 2-tuples "(obj, hint)"
    # describing the type hint matching an arbitrary object) to be returned by
    # this fixture.
    INFER_HINT_CASES = [
        # ..................{ NON-PEP                        }..................
        # A builtin scalar is annotated as the builtin type of that scalar.
        ('Of his frail exultation shall be spent', str),

        # An instance of a PEP-noncompliant class (i.e., a class *NOT* covered
        # by an existing PEP standard) satisfying no broader type hint is
        # annotated simply as that class.
        (Class(), Class),

        # ..................{ NON-PEP : collections.abc      }..................
        # An instance of a PEP-noncompliant class (i.e., a class *NOT* covered
        # by an existing PEP standard) satisfying a standard "collections.abc"
        # protocol is annotated as the narrowest such protocol. Moreover, for
        # each instance that is a container (i.e., satisfies the standard
        # "collections.abc.Container" protocol), that annotation is subscripted
        # by a child type hint annotating the items of that container.
        (
            ClassMutableSequence((
                'Forgetful of the grave', 'where', 'when the flame')),
            MutableSequence[str],
        ),

        # ..................{ PEP 484                        }..................
        # The "None" singleton is annotated as itself under PEP 484.
        (None, None),

        # ..................{ PEP [484|585]                  }..................
        # A class is annotated as the PEP 484- or 585-compliant "type" supertype
        # subscripted by that class.
        (Class, Type[Class]),

        # ..................{ PEP [484|585] ~ deque          }..................
        # A deque of items all of the same class is annotated as the PEP 484- or
        # 585-compliant "deque" type subscripted by that class.
        (
            deque(('On the green moss his tremulous step,', 'that caught',)),
            Deque[str],
        ),

        # ..................{ PEP [484|585] ~ frozenset      }..................
        # A frozen set of items all of the same class is annotated as the PEP
        # 484- or 585-compliant "frozenset" type subscripted by that class.
        (
            frozenset({"I' the passing wind!", 'Beside the grassy shore',}),
            FrozenSet[str],
        ),

        # ..................{ PEP [484|585] ~ keysview       }..................
        # A keys view of keys all of the same class is annotated as the PEP 484-
        # or 585-compliant "KeysView" type subscripted by that class.
        ({
            b'What oozy cavern': 'or what wandering cloud expose',
            b'Contains thy waters,': 'as the universe',
        }.keys(), KeysView[bytes]),

        # ..................{ PEP [484|585] ~ list           }..................
        # A list of items all of the same class is annotated as the PEP 484- or
        # 585-compliant "list" type subscripted by that class.
        (['expose', 'extreme', 'explosions!',], List[str]),

        # A list of items all of differing classes is annotated as the PEP 484-
        # and 585-compliant "list" type subscripted by a PEP 604- or
        # 484-compliant union type hint of those classes -- including...
        ([
            # A string.
            'Thy dazzling waves, thy loud and hollow gulfs,',
            # A byte string.
            b'Thy searchless fountain, and invisible course',
            # An integer.
            len('Have each their type in me: and the wide sky,'),
            # A list of strings.
            ['And measureless ocean', 'may declare', 'as soon',],
        ], List[
            # If the active Python interpreter targets Python >= 3.10 and thus
            # supports PEP 604-compliant new-style unions, this kind of union;
            str | bytes | int | List[str]
            if IS_PYTHON_AT_LEAST_3_10 else
            # Else, the active Python interpreter targets Python < 3.10 and thus
            # fails to support PEP 604-compliant new-style unions. In this case,
            # fallback to a PEP 484-compliant old-style union.
            Union[str, bytes, int, List[str]]
        ]),

        # ..................{ PEP [484|585] ~ set            }..................
        # A set of items all of the same class is annotated as the PEP 484- or
        # 585-compliant "set" type subscripted by that class.
        ({'Of the small stream he went;', 'he did impress',}, Set[str]),

        # ..................{ PEP [484|585] ~ tuple          }..................
        # # A 2-tuple of items of differing classes (one of which is a nested list
        # # of is annotated as the PEP 484-
        # # and 585-compliant "tuple" type subscripted in a fixed-length manner
        # # by type hints matching those classes.
        # ((b'heh', [0xBEEEEEEEF, 'ohnoyoudont',], (
        #     (b'heh', [0xBEEEEEEEF, 'ohnoyoudont',]).
        #     .
        # )),

        # ..................{ PEP [484|585] ~ valuesview     }..................
        # A values view of values all of the same class is annotated as the PEP
        # 484- or 585-compliant "ValuesView" type subscripted by that class.
        ({
            'Tell where these living thoughts reside,': b'when stretched',
            'Upon thy flowers': b'my bloodless limbs shall waste',
        }.values(), ValuesView[bytes]),
    ]

    # Return this mutable list coerced into an immutable tuple for safety.
    return tuple(INFER_HINT_CASES)

# ....................{ FIXTURES ~ subhint                 }....................
#FIXME: Rename to door_cases_is_subhint() for orthogonality.
@fixture(scope='session')
def door_cases_is_subhint() -> 'Iterable[Tuple[object, object, bool]]':
    '''
    Session-scoped fixture returning an iterable of **type subhint cases**
    (i.e., 3-tuples ``(subhint, superhint, is_subhint)`` describing the subhint
    relations between two type hints), efficiently cached across all tests
    requiring this fixture.

    This iterable is intentionally defined by the return of this fixture rather
    than as a global constant of this submodule. Why? Because the former safely
    defers all heavyweight imports required to define this iterable to the call
    of the first unit test requiring this fixture, whereas the latter unsafely
    performs those imports at pytest test collection time.

    Returns
    -------
    Iterable[Tuple[object, object, bool]]
        Iterable of one or more 3-tuples ``(subhint, superhint, is_subhint)``,
        where:

        * ``subhint`` is the type hint to be passed as the first parameter to
          the :func:`beartype.door.is_subhint` tester.
        * ``superhint`` is the type hint to be passed as the second parameter to
          the :func:`beartype.door.is_subhint` tester.
        * ``is_subhint`` is :data:`True` only if that subhint is actually a
          subhint of that superhint according to that tester.
    '''

    # ..................{ IMPORTS                            }..................
    # Defer fixture-specific imports.
    import collections.abc
    import typing
    from beartype._data.hint.datahinttyping import S, T
    from beartype._util.hint.pep.utilpepget import get_hint_pep_typevars
    from beartype._util.py.utilpyversion import IS_PYTHON_AT_LEAST_3_9
    from collections.abc import (
        Collection as CollectionABC,
        Sequence as SequenceABC,
    )

    # Intentionally import from "beartype.typing" rather than "typing" to
    # guarantee PEP 544-compliant caching protocol type hints.
    from beartype.typing import (
        Literal,
        Protocol,
        TypedDict,
    )

    # Intentionally import from "typing" rather than "beartype.typing" to
    # guarantee PEP 484-compliant type hints.
    from typing import (
        Any,
        Awaitable,
        ByteString,
        Callable,
        Collection,
        DefaultDict,
        Dict,
        Generic,
        Hashable,
        Iterable,
        List,
        Mapping,
        NamedTuple,
        NewType,
        Optional,
        Reversible,
        Sequence,
        Sized,
        Tuple,
        Type,
        TypeVar,
        Union,
    )

    # ..................{ NEWTYPES                           }..................
    NewStr = NewType('NewStr', str)

    # ..................{ TYPEVARS                           }..................
    # Arbitrary constrained type variables.
    T_sequence = TypeVar('T_sequence', bound=SequenceABC)
    T_int_or_str = TypeVar('T_int_or_str', int, str)

    # ..................{ CLASSES                            }..................
    class MuhThing:
        def muh_method(self):
            pass

    class MuhSubThing(MuhThing):
        pass

    class MuhNutherThing:
        def __len__(self) -> int:
            pass


    class MuhDict(TypedDict):
        '''
        Arbitrary typed dictionary.
        '''

        thing_one: str
        thing_two: int


    class MuhThingP(Protocol):
        '''
        Arbitrary caching @beartype protocol.
        '''

        def muh_method(self):
            ...


    class MuhTuple(NamedTuple):
        '''
        Arbitrary named tuple.
        '''

        thing_one: str
        thing_two: int

    # ..................{ CLASSES ~ generics                 }..................
    class MuhGeneric(Generic[T]):
        '''
        Arbitrary generic parametrized by one unconstrained type variable.
        '''

        pass


    class MuhGenericTwo(Generic[S, T]):
        '''
        Arbitrary generic parametrized by two unconstrained type variables.
        '''

        pass


    class MuhGenericTwoIntInt(MuhGenericTwo[int, int]):
        '''
        Arbitrary concrete generic subclass inheriting the
        :class:`.MuhGenericTwo` generic superclass subscripted twice by the
        builtin :class:`int` type.
        '''

        pass

    # ..................{ LISTS ~ cases                      }..................
    # List of all hint subhint cases (i.e., 3-tuples "(subhint, superhint,
    # is_subhint)" describing the subhint relations between two PEP-compliant
    # type hints) to be returned by this fixture.
    HINT_SUBHINT_CASES = [
        # ..................{ PEP 484 ~ argless : any        }..................
        # PEP 484-compliant catch-all type hint.
        (MuhThing, Any, True),
        (Tuple[object, ...], Any, True),
        (Union[int, MuhThing], Any, True),

        # Although *ALL* type hints are subhints of "Any", "Any" is only a
        # subhint of itself.
        (Any, Any, True),
        (Any, object, False),

        # ..................{ PEP 484 ~ argless : bare       }..................
        # PEP 484-compliant unsubscripted type hints, which are necessarily
        # subhints of themselves.
        (list, list, True),
        (list, List, True),

        # PEP 484-compliant unsubscripted sequence type hints.
        (Sequence, List, False),
        (Sequence, list, False),
        (List, Sequence, True),
        (list, Sequence, True),
        (list, SequenceABC, True),
        (list, CollectionABC, True),

        # ..................{ PEP 484 ~ argless : type       }..................
        # PEP 484-compliant argumentless abstract base classes (ABCs).
        (bytes, ByteString, True),
        (str, Hashable, True),
        (MuhNutherThing, Sized, True),
        (MuhTuple, tuple, True),  # not really types

        # PEP 484-compliant new type type hints.
        (NewStr, NewStr, True),
        (NewStr, int, False),
        (NewStr, str, True),
        (int, NewStr, False),
        (str, NewStr, False),  # NewType act like subtypes

        # ..................{ PEP 484 ~ argless : typevar    }..................
        # PEP 484-compliant type variables.
        (list, T_sequence, True),
        (T_sequence, list, False),
        (int, T_int_or_str, True),
        (str, T_int_or_str, True),
        (list, T_int_or_str, False),
        (Union[int, str], T_int_or_str, True),
        (Union[int, str, None], T_int_or_str, False),
        (T, T_sequence, False),
        (T_sequence, T, True),
        (T_sequence, Any, True),
        (Any, T, True),  # Any is compatible with an unconstrained TypeVar
        (Any, T_sequence, False),  # but not vice versa

        # ..................{ PEP 484 ~ argless : number     }..................
        # Blame Guido.
        (bool, int, True),

        # PEP 484-compliant implicit numeric tower, which we explicitly and
        # intentionally do *NOT* comply with. Floats are not integers. Notably,
        # floats *CANNOT* losslessly represent many integers and are thus
        # incompatible in general.
        (float, int, False),
        (complex, int, False),
        (complex, float, False),
        (int, float, False),
        (float, complex, False),

        # ..................{ PEP 484 ~ arg : callable       }..................
        # PEP 484-compliant callable type hints.
        (Callable, Callable[..., Any], True),
        (Callable[[], int], Callable[..., Any], True),
        (Callable[[int, str], List[int]], Callable, True),
        (Callable[[int, str], List[int]], Callable, True),
        (
            Callable[[float, List[str]], int],
            Callable[[int, Sequence[str]], int],
            True,
        ),
        (Callable[[Sequence], int], Callable[[list], int], False),
        (Callable[[], int], Callable[..., None], False),
        (Callable[..., Any], Callable[..., None], False),
        (Callable[[float], None], Callable[[float, int], None], False),
        (Callable[[], int], Sequence[int], False),
        (Callable[[int, str], int], Callable[[int, str], Any], True),
        # (types.FunctionType, Callable, True),  # FIXME

        # ..................{ PEP 484 ~ arg : generic        }..................
        # PEP 484-compliant generics parametrized by one type variable.
        (MuhGeneric, MuhGeneric, True),
        (MuhGeneric, MuhGeneric[int], False),
        (MuhGeneric[int], MuhGeneric, True),
        (MuhGeneric[int], MuhGeneric[T_sequence], False),
        (MuhGeneric[list], MuhGeneric[T_sequence], True),
        (MuhGeneric[list], MuhGeneric[Sequence], True),
        (MuhGeneric[str], MuhGeneric[T_sequence], True),
        (MuhGeneric[Sequence], MuhGeneric[list], False),
        (MuhGeneric[T_sequence], MuhGeneric, True),

        #FIXME: Uncomment after resolving open issue #271, please.
        # PEP 484-compliant generics parametrized by two type variables.
        # (MuhGenericTwoIntInt, MuhGenericTwo[int, int], True),

        # ..................{ PEP 484 ~ arg : mapping        }..................
        # PEP 484-compliant mapping type hints.
        (dict, Dict, True),
        (Dict[str, int], Dict, True),
        (dict, Dict[str, int], False),
        (
            DefaultDict[str, Sequence[int]],
            Mapping[Union[str, int], Iterable[Union[int, str]]],
            True,
        ),

        # ..................{ PEP 484 ~ arg : sequence       }..................
        # PEP 484-compliant sequence type hints.
        (List[int], List[int], True),
        (List[int], Sequence[int], True),
        (Sequence[int], Iterable[int], True),
        (Iterable[int], Sequence[int], False),
        (Sequence[int], Reversible[int], True),
        (Sequence[int], Reversible[str], False),
        (Collection[int], Sized, True),
        (List[int], List, True),  # if the super is un-subscripted, assume Any
        (List[int], List[Any], True),
        (Awaitable, Awaitable[str], False),
        (List[int], List[str], False),

        # PEP 484-compliant tuple type hints.
        (tuple, Tuple, True),
        (Tuple, Tuple, True),
        (tuple, Tuple[Any, ...], True),
        (tuple, Tuple[()], False),
        (Tuple[()], tuple, True),
        (Tuple[int, str], Tuple[int, str], True),
        (Tuple[int, str], Tuple[int, str, int], False),
        (Tuple[int, str], Tuple[int, Union[int, list]], False),
        (Tuple[Union[int, str], ...], Tuple[int, str], False),
        (Tuple[int, str], Tuple[str, ...], False),
        (Tuple[int, str], Tuple[Union[int, str], ...], True),
        (Tuple[Union[int, str], ...], Tuple[Union[int, str], ...], True),
        (Tuple[int], Dict[str, int], False),
        (Tuple[Any, ...], Tuple[str, int], False),

        # PEP 484-compliant nested sequence type hints.
        (List[int], Union[str, List[Union[int, str]]], True),

        # ..................{ PEP 484 ~ arg : subclass       }..................
        # PEP 484-compliant subclass type hints.
        (Type[int], Type[int], True),
        (Type[int], Type[str], False),
        (Type[MuhSubThing], Type[MuhThing], True),
        (Type[MuhThing], Type[MuhSubThing], False),
        (MuhThing, Type[MuhThing], False),

        # ..................{ PEP 484 ~ arg : union          }..................
        # PEP 484-compliant unions.
        (int, Union[int, str], True),
        (Union[int, str], Union[list, int, str], True),
        (Union[str, int], Union[int, str, list], True),  # order doesn't matter
        (Union[str, list], Union[str, int], False),
        (Union[int, str, list], list, False),
        (Union[int, str, list], Union[int, str], False),
        (int, Optional[int], True),
        (Optional[int], int, False),
        (list, Optional[Sequence], True),

        # ..................{ PEP 544                        }..................
        # PEP 544-compliant type hints.
        (MuhThing, MuhThingP, True),
        (MuhNutherThing, MuhThingP, False),
        (MuhThingP, MuhThing, False),

        # ..................{ PEP 586                        }..................
        # PEP 586-compliant type hints.
        (Literal[7], int, True),
        (Literal["a"], str, True),
        (Literal[7, 8, "3"], Union[int, str], True),
        (Literal[7, 8, "3"], Union[list, int], False),
        (Literal[True], Union[Literal[True], Literal[False]], True),
        (Literal[7, 8], Literal[7, 8, 9], True),
        (int, Literal[7], False),
        (Union[Literal[True], Literal[False]], Literal[True], False),

        # ..................{ PEP 589                        }..................
        # PEP 589-compliant type hints.
        (MuhDict, dict, True),
    ]

    # ..................{ LISTS ~ typing                     }..................
    # List of the unqualified basenames of all standard ABCs published by
    # the standard "collections.abc" module, defined as...
    COLLECTIONS_ABC_BASENAMES = [
        # For the unqualified basename of each attribute defined by the standard
        # "collections.abc" module...
        COLLECTIONS_ABC_BASENAME
        for COLLECTIONS_ABC_BASENAME in dir(collections.abc)
        # If this basename is *NOT* prefixed by an underscore, this attribute is
        # public and thus an actual ABC. In this case, include this ABC.
        if not COLLECTIONS_ABC_BASENAME.startswith('_')
        # Else, this is an unrelated private attribute. In this case, silently
        # ignore this attribute and continue to the next.
    ]

    # List of the unqualified basenames of all standard abstract base classes
    # (ABCs) supported by the standard "typing" module, defined as the
    # concatenation of...
    TYPING_ABC_BASENAMES = (
        # List of the unqualified basenames of all standard ABCs published by
        # the standard "collections.abc" module *PLUS*...
        COLLECTIONS_ABC_BASENAMES +
        # List of the unqualified basenames of all ancillary ABCs *NOT*
        # published by the standard "collections.abc" module but nonetheless
        # supported by the standard "typing" module.
        ['Deque']
    )

    # ..................{ HINTS ~ abcs                       }..................
    # For the unqualified basename of each standard ABCs supported by the
    # standard "typing" module...
    #
    # Note this also constitutes a smoke test (i.e., high-level test validating
    # core functionality) for whether the DOOR API supports standard abstract
    # base classes (ABCs). Smoke out those API inconsistencies, pytest!
    for TYPING_ABC_BASENAME in TYPING_ABC_BASENAMES:
        #FIXME: This logic is likely to fail under a future Python release.
        # Type hint factory published by the "typing" module corresponding to
        # this ABC if any *OR* "None" otherwise (i.e., if "typing" publishes
        # *NO* such type hint factory).
        TypingABC = getattr(typing, TYPING_ABC_BASENAME, None)

        # If "typing" publishes *NO* such type hint factory, silently ignore
        # this ABC and continue to the next.
        if TypingABC is None:
            continue
        # Else, "typing" publishes this type hint factory.

        # Number of type variables parametrizing this ABC, defined as either...
        TYPING_ABC_TYPEVARS_LEN = (
            # If the active Python interpreter targets Python >= 3.9, a private
            # instance variable of this type hint factory yielding this
            # metadata. Under Python >= 3.9, unsubscripted type hint factories
            # are *NOT* parametrized by type variables.
            TypingABC._nparams
            if IS_PYTHON_AT_LEAST_3_9 else
            # Else, the active Python interpreter targets Python < 3.9. In this
            # case, the number of type variables directly parametrizing this
            # ABC.
            len(get_hint_pep_typevars(TypingABC))
        )

        # If this ABC is parametrized by one or more type variables, exercise
        # that this ABC subscripted by one or more arbitrary concrete types is a
        # non-trivial subhint of this same ABC subscripted by one or more
        # arbitrary different ABCs of those concrete types.
        if TYPING_ABC_TYPEVARS_LEN:
            subhint =   TypingABC[(list,)     * TYPING_ABC_TYPEVARS_LEN]
            superhint = TypingABC[(Sequence,) * TYPING_ABC_TYPEVARS_LEN]
        # Else, this ABC is parametrized by *NO* type variables. In this case,
        # fallback to exercising that this ABC is a trivial subhint of itself.
        else:
            subhint =   TypingABC
            superhint = TypingABC

        # Append a new hint subhint case exercising that this subhint is
        # actually a subhint of this superhint.
        HINT_SUBHINT_CASES.append((subhint, superhint, True))

    # ..................{ HINTS ~ version                    }..................
    # If the active Python interpreter targets Python >= 3.9 and thus supports
    # both PEP 585 and 593...
    if IS_PYTHON_AT_LEAST_3_9:
        # Defer version-specific imports.
        from beartype.typing import Annotated

        # Append cases exercising version-specific relations.
        HINT_SUBHINT_CASES.extend((
            # PEP 585-compliant type hints.
            (tuple, Tuple, True),
            (tuple[()], Tuple[()], True),

            # PEP 593-compliant type hints.
            (Annotated[int, "a note"], int, True),  # annotated is subtype of unannotated
            (int, Annotated[int, "a note"], False),  # but not vice versa
            (Annotated[list, True], Annotated[Sequence, True], True),
            (Annotated[list, False], Annotated[Sequence, True], False),
            (Annotated[list, 0, 0], Annotated[list, 0], False),  # must have same num args
            (Annotated[List[int], "metadata"], List[int], True),
        ))

    # Return this mutable list coerced into an immutable tuple for safety.
    return tuple(HINT_SUBHINT_CASES)
