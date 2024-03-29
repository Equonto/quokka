

from types import SimpleNamespace
from typing import List


class Utils:

    @staticmethod
    def attribute_exists(object, attribute_name: str) -> bool:
        return attribute_name in object
    
    @staticmethod
    def make_objects_in_list_unique(list: List[SimpleNamespace]) -> List[SimpleNamespace]:
        unique_list = []
        for item in list:
            if item not in unique_list:
                unique_list.append(item)
        return unique_list