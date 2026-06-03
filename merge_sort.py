from typing import List, TypeVar

T = TypeVar("T", int, float, str)


def merge_sort(arr: List[T]) -> List[T]:
    """Ordena una lista usando el algoritmo merge sort.

    Args:
        arr: Lista de elementos comparables (int, float, str).

    Returns:
        Nueva lista con los elementos ordenados ascendentemente.
    """
    if len(arr) <= 1:
        return arr[:]

    mid: int = len(arr) // 2
    left: List[T] = merge_sort(arr[:mid])
    right: List[T] = merge_sort(arr[mid:])

    return _merge(left, right)


def _merge(left: List[T], right: List[T]) -> List[T]:
    """Fusiona dos listas ordenadas en una sola lista ordenada."""
    result: List[T] = []
    i: int = 0
    j: int = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


if __name__ == "__main__":
    datos: List[int] = [38, 27, 43, 3, 9, 82, 10]
    print(f"Original: {datos}")
    print(f"Ordenado: {merge_sort(datos)}")
