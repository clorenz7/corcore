from math import floor

class Node(object):

    def __init__(self, value, parent=None, left=None, right=None):
        self.parent = parent
        self.left = left
        self.right = right
        self.value = value


class Heap(object):

    """
    A heap is a data structure where the parent node > all children
    """

    def __init__(self):
        self.data = []
        self.n_pts = 0

    def __len__(self):
        return self.n_pts

    @staticmethod
    def parent_idx(idx):
        return int(floor((idx+1)/2)-1)

    @staticmethod
    def left_idx(idx):
        return int(2*(idx+1)-1)

    @staticmethod
    def right_idx(idx):
        return int(2*(idx+1))

    # def add_node(self, value):
    #     self.data.append(value)
    #     new_idx = len(self)
    #     self.n_pts += 1
    #     self.heapify(new_idx)

    # def heapify(self, idx):
    #     if idx == 0:
    #         return
    #     p_idx = self.parent_idx(idx)
    #     p_val = self.data[p_idx]
    #     new_val = self.data[idx]
    #     if p_val < new_val and p_val is not None:
    #         self.data[p_idx] = new_val
    #         self.data[idx] = p_val
    #         self.heapify(p_idx)

    def add_node(self, value):
        self.data.insert(0, value)
        self.n_pts += 1
        self.heapify(0)

    def heapify(self, idx):
        p_val = self.data[idx]
        l_idx = self.left_idx(idx)
        if l_idx >= len(self):
            l_val = None
        else:
            l_val = self.data[l_idx]
        r_idx = self.right_idx(idx)
        if r_idx >= len(self):
            r_val = None
        else:
            r_val = self.data[r_idx]

        if r_val is None and l_val is None:
            return

        if l_val > p_val and l_val > r_val:
            self.data[idx] = l_val
            self.data[l_idx] = p_val
            self.heapify(l_idx)
        elif r_val > p_val:
            self.data[idx] = r_val
            self.data[r_idx] = p_val
            self.heapify(r_idx)


    def remove_node(self, idx):
        val = self.data[idx]
        swap_data = self.data.pop()
        self.n_pts -= 1
        if self.n_pts > 0:
            self.data[idx] = swap_data
            self.heapify(idx)
        return val

        # l_idx = self.left_idx(idx)
        # val = self.data[idx]
        # self.data[idx] = None
        # if l_idx >= len(self):
        #     l_val = None
        # else:
        #     l_val = self.data[l_idx]
        # r_idx = self.right_idx(idx)
        # if r_idx >= len(self):
        #     r_val = None
        # else:
        #     r_val = self.data[r_idx]

        # if r_val is None and l_val is None:
        #     self.n_pts -= 1
        #     return

        # if l_val > r_val:
        #     if l_val is None:
        #         import ipdb
        #         ipdb.set_trace()
        #     self.data[idx] = l_val
        #     self.remove_node(l_idx)
        # else:
        #     if r_val is None:
        #         import ipdb
        #         ipdb.set_trace()
        #     self.data[idx] = r_val
        #     self.remove_node(r_idx)

    def swap_with_child(self, idx):
        p_val = self.data[idx]
        l_idx = self.left_idx(idx)
        if l_idx >= len(self):
            l_val = None
        else:
            l_val = self.data[l_idx]
        r_idx = self.right_idx(idx)
        if r_idx >= len(self):
            r_val = None
        else:
            r_val = self.data[r_idx]

        if r_val is None and l_val is None:
            return

        if l_val > r_val:
            if l_val is None:
                import ipdb
                ipdb.set_trace()
            self.data[idx] = l_val
            self.data[l_idx] = p_val
            if 2 not in self.data:
                import ipdb
                ipdb.set_trace()
            self.swap_with_child(l_idx)
        else:
            if r_val is None:
                import ipdb
                ipdb.set_trace()
            self.data[idx] = r_val
            self.data[r_idx] = p_val
            if 2 not in self.data:
                import ipdb
                ipdb.set_trace()
            self.swap_with_child(r_idx)


def heapsort(data):
    heap = Heap()

    for pt in data:
        heap.add_node(pt)
    sorted_data = []

    for pt in xrange(len(heap)):
        val = heap.data[0]
        heap.remove_node(0)
        sorted_data.append(val)

    return sorted_data, heap





