class Bridge(object):
    """
    Create class to send info between threads.
    """

    def __init__(self):
        """
        Create the empty list.
        """
        self.item = []

    def __repr__(self):
        """
        :return:
        return items like text.
        """
        return f"{self.item}"

    def __str__(self):
        """
        :return:
        return items like string.
        """
        return f"{self.item}"

    def send(self, add):
        """
        Use to send data.
        :param add:
        Data to add in Bridge.
        :return:
        True
        """
        self.item.insert(0, add)
        return True

    def size(self):
        """
        Get the item list length.
        :return:
        List item count.
        """
        return len(self.item)

    def is_empty(self):
        """
        Check is there any data.
        :return:
        True if there is any data.
        """
        return self.size() == 0

    def receive(self):
        """
        Get data from bridge and empty the space.
        :return:
        data if it exists.
        """
        if self.size() == 0:
            return None
        else:
            return self.item.pop()
