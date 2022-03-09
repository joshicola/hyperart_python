from .element import Element
from .transformation import Transformation


class Pattern:
    def __init__(self) -> None:
        self._elems = {}
        self._frame = {}
        self._patId = 0

    def addElement(self, m: Element, tran=None, cloneId=True, frame=False):
        """_summary_

        Args:
            m (Element): _description_
            tran (_type_, optional): _description_. Defaults to None.
            cloneId (bool, optional): _description_. Defaults to True.
            frame (bool, optional): _description_. Defaults to False.

        Returns:
            _type_: _description_
        """
        clone = m.clone()
        if tran:
            clone.transform(tran)  # transform the clone
        # whether to use clone's id or original's id
        elemId = clone.id() if cloneId else m.id()
        if not frame:
            self._elems[elemId] = clone
        else:
            self._frame[elemId] = clone
        return elemId
