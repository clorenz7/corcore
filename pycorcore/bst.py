
class Tree(object):
    def __init__(self, root_node):
        self.root_node = root_node

    def query(self, key):
        return self.root_node.query(key)

    def add_node(self, new_node, base_node=None):

        base_node = base_node or self.root_node
        new_key_is_less = new_node.key <= base_node.key
        new_key_is_more = new_node.key >= base_node.key

        if new_key_is_less and base_node.left is None:
            base_node.left = new_node
            new_node.parent = base_node
        elif new_key_is_more and base_node.right is None:
            base_node.right = new_node
            new_node.parent = base_node
        elif new_key_is_less:
            self.add_node(new_node, base_node.left)
        elif new_key_is_more:
            self.add_node(new_node, base_node.right)


class Node(object):

    def __init__(self, key, parent, left=None, right=None):
        self.parent = parent
        self.left = left
        self.right = right
        self.key = key

    def __repr__(self):

        left = getattr(self.left, 'key', None)
        right = getattr(self.right, 'key', None)
        parent = getattr(self.parent, 'key', None)

        repr_str = '{}, l:{}, r:{}, p:{}'.format(
            self.key, left, right, parent
        )

        return repr_str

    def max_child(self):
        if self.right is not None:
            return self.right.max_child()
        else:
            return self.key

    def min_child(self):
        raise NotImplementedError("Node Class Min Child Method!")


    def predecessor(self):

        if self.left is not None:
            return self.left.max_child()
        else:
            prev_node = self
            search_node = self.parent
            while search_node is not None:
                if search_node.right == prev_node:
                    return search_node.key
                else:
                    prev_node = search_node
                    search_node = prev_node.parent
            if search_node is None:
                return None
            else:
                return search_node.key

    def successor(self):
        raise NotImplementedError("Node Class Successor Method!")

    def query(self, key):
        if self.key == key:
            return self
        elif self.key > key:
            if self.left is None:
                raise KeyError("{} key was not found!")
            return self.left.query(key)
        else:
            if self.right is None:
                raise KeyError("{} key was not found!")
            return self.right.query(key)
