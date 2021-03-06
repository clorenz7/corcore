
class BinarySearchTree(object):
    def __init__(self, root_node):
        self.root_node = root_node

    def query(self, key, node=None):
        node = node or self.root_node

        if node.key == key:
            return node
        elif node.key > key:
            if node.left is None:
                raise KeyError("{} key was not found!".format(key))
            return self.query(key, node.left)
        else:
            if node.right is None:
                raise KeyError("{} key was not found!".format(key))
            return self.query(key, node.right)

    def add_node(self, new_node, base_node=None):

        base_node = base_node or self.root_node
        if base_node is None:
            self.root_node = base_node
            return

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

    def get_deepest_node(self, start_node=None):
        """
        Do a recursive search to get the deepest node in the tree,
        and return its depth.
        :returns: depth, deepest_node
        """

        start_node = start_node or self.root_node

        left_node = start_node.left
        right_node = start_node.right

        if left_node is None and right_node is None:
            return 0, start_node
        elif left_node is None:
            depth, node = self.get_deepest_node(right_node)
        elif right_node is None:
            depth, node = self.get_deepest_node(left_node)
        else:
            right_depth, r_last_node = self.get_deepest_node(right_node)
            left_depth, l_last_node = self.get_deepest_node(left_node)

            if right_depth > left_depth:
                depth = right_depth
                node = r_last_node
            else:
                depth = left_depth
                node = l_last_node

        return depth+1, node

    def rotate_right(self, node):
        """
        Rotates the provided node to be the child of its left child
        """

        # Get the new parent and validate it exists
        new_parent = node.left
        if new_parent is None:
            raise ValueError("Can't rotate: left child is None!")

        # Put the right child of the new parent on the left of the node
        new_left_child = new_parent.right
        if new_left_child is not None:  # if it exists
            new_left_child.parent = node
        node.left = new_left_child

        # Make the node the child of the new parent
        new_parent.right = node

        # Fix pointers to/from grand parent
        grand_parent = node.parent
        new_parent.parent = grand_parent
        if grand_parent is None:  # it is root
            # New parent is the root
            self.root_node = new_parent
        elif grand_parent.right is node:
            grand_parent.right = new_parent
        else:
            grand_parent.left = new_parent

    def rotate_left(self, node):

        # Get the right child
        new_parent = node.right
        if new_parent is None:
            raise ValueError("Can't rotate: right child is None!")

        # Get the grand parent
        grand_parent = node.parent

        # Get the left child of the new parent
        new_right_child = new_parent.left

        # Swap the node and its child
        node.parent = new_parent
        new_parent.left = node

        # Update the grand_parent's child
        new_parent.parent = grand_parent
        # Handle the case where the parent doesn't exist
        if grand_parent is None:
            self.root_node = new_parent
        else:
            if grand_parent.left is node:
                grand_parent.left = new_parent
            else:
                grand_parent.right = new_parent
        # Swap the left child of the new parent to be the right child of node
        node.right = new_right_child
        if new_right_child is not None:
            new_right_child.parent = node

    def successor(self, node):
        """
        Finds and returns the node in the tree with the next highest value.
        If the node is the max value, returns None
        """

        if node.right is None:
            # Need to search for the ancestor who's left child is also an ancestor
            while node is not self.root_node:
                parent = node.parent
                if parent.left is node:
                    return parent
                else:
                    node = parent

            return None  # No successor
        else:
            # If there is a right subtree, find the min value of it.
            node = node.right

            while node.left is not None:
                node = node.left

            return node

    def delete(self, node):
        """
        Deletes a key from the binary search tree, and repairs it to maintain BST properties.
        """

        left_is_none = node.left is None
        right_is_none = node.right is None
        parent = node.parent

        # If node has no children, just null parent's pointer
        if left_is_none and right_is_none:
            if parent is None:
                self.root_node = None
            else:
                if parent.right is node:
                    parent.right = None
                else:
                    parent.left = None
            return

        # If there are children, find the node to splice in
        # If node has 2 children, find the successor
        if not left_is_none and not right_is_none:
            splice_node = self.successor(node)
            splice_node.left = node.left

            if splice_node.parent.left is splice_node:
                splice_node.parent.left = splice_node.right
                splice_node.right = node.right

        else:
            # If node has 1 child, splice in that child
            if left_is_none:
                splice_node = node.right
            else:
                splice_node = node.left

        # Fix the parent pointers
        splice_node.parent = parent
        if parent is not None:
            if parent.left is node:
                parent.left = splice_node
            else:
                parent.right = splice_node

        # If node was root, update root
        if node is self.root_node:
            self.root_node = splice_node



class Node(object):

    def __init__(self, key, parent=None, left=None, right=None):
        self.parent = parent
        self.left = left
        self.right = right
        self._key = key

    def __repr__(self):

        left = getattr(self.left, 'key', None)
        right = getattr(self.right, 'key', None)
        parent = getattr(self.parent, 'key', None)

        repr_str = '{}, l:{}, r:{}, p:{}'.format(
            self.key, left, right, parent
        )

        return repr_str

    @property
    def key(self):
        return self._key


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

