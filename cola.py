class Queue:

    def __init__(self, limit=None):

        self.items = []  # Lista interna para almacenar los elementos de la cola
        self.limit = limit  # Límite opcional para el número de elementos

    def enqueue(self, item):

        if self.limit is None or len(self.items) < self.limit:
            self.items.append(item)
        else:
            raise Exception("La cola ha alcanzado su límite")

    def dequeue(self):
        """
        Elimina y retorna el primer elemento de la cola.

        Returns:
        item: El primer elemento de la cola.

        Raises:
        Exception: Si la cola está vacía.
        """
        if not self.is_empty():
            return self.items.pop(0)
        raise Exception("La cola está vacía")

    def first(self):
        """
        Retorna el primer elemento de la cola sin eliminarlo.

        Returns:
        item: El primer elemento de la cola, o None si la cola está vacía.
        """
        if not self.is_empty():
            return self.items[0]
        return None

    def is_empty(self):
        """
        Verifica si la cola está vacía.

        Returns:
        bool: True si la cola está vacía, False de lo contrario.
        """
        return len(self.items) == 0

    def size(self):
        """
        Obtiene el tamaño de la cola (número de elementos).

        Returns:
        int: El número de elementos en la cola.
        """
        return len(self.items)
