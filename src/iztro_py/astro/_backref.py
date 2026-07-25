"""Deep-copy support for the Functional* back-references.

`FunctionalStar._palace` and `FunctionalPalace._astrolabe` are plain attributes
living in the model's ``__dict__`` (they are not pydantic fields), so they form
star -> palace -> astrolabe -> star reference cycles.

Pydantic's ``BaseModel.__deepcopy__`` copies ``self.__dict__`` *without* first
registering the new instance in ``memo``, so a cycle does not converge: each
traversal yields a fresh object. The result was a copied chart whose palaces
pointed at a third, stale astrolabe, silently making
``star.surrounded_palaces()`` and ``opposite_palace()`` query the wrong chart.

These back-references are derived state, so the fix is to keep them out of the
copy entirely and let the owner re-wire them afterwards.
"""

from typing import Any, ClassVar, Dict, Optional, TypeVar

T = TypeVar("T", bound="BackRefDeepCopyMixin")


class BackRefDeepCopyMixin:
    """Excludes ``_BACKREF_ATTR`` from deep copies and blanks it on the copy."""

    #: Name of the back-reference attribute to omit when deep-copying.
    #: Must be ClassVar: pydantic turns any other underscore-prefixed class
    #: attribute into a private *instance* attribute, which would silently
    #: shadow this with the empty default and disable the whole mechanism.
    _BACKREF_ATTR: ClassVar[str] = ""

    def __deepcopy__(self: T, memo: Optional[Dict[int, Any]] = None) -> T:
        if memo is None:
            memo = {}

        attr = self._BACKREF_ATTR
        state: Dict[str, Any] = self.__dict__
        detached = attr in state
        saved = state.pop(attr, None) if detached else None
        try:
            copied = super().__deepcopy__(memo)  # type: ignore[misc]
        finally:
            if detached:
                state[attr] = saved

        # The owner re-wires this immediately; None is the correct interim value
        # for a copy that has not been attached to anything yet.
        object.__setattr__(copied, attr, None)
        return copied
