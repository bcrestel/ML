import numpy as np
from numpy.random import randint, choice

class BinaryNode():
    """
    Node/Leaf for a binary tree
    """

    def __init__(self, ID, value):
        self.ID = ID
        self.value = value 
        self.left = None
        self.right = None
        self.parent = None

    def addleftchild(self, node):
        self.left = node
        node.addparent(self)

    def addrightchild(self, node):
        self.right = node
        node.addparent(self)

    def addparent(self, node):
        self.parent = node

    def print(self):
        print('ID={}, value={}'.format(self.ID, self.value))

    def preorder(self):
        self.print()
        if self.left is not None:
            self.left.preorder()
        if self.right is not None:
            self.right.preorder()

    def postorder(self):
        if self.left is not None:
            self.left.postorder()
        if self.right is not None:
            self.right.postorder()
        self.print()
        
    def inorder(self):
        if self.left is not None:
            self.left.inorder()
        self.print()
        if self.right is not None:
            self.right.inorder()



class BinaryTree():
    """
    General class for a binary tree (i.e., at most 2 children)
    """

    def __init__(self, root):
        """
        root = BinaryNode
        """
        self.root = root

    def preordertraversal(self):
        self.root.preorder()

    def postordertraversal(self):
        self.root.postorder()

    def inordertraversal(self):
        self.root.inorder()

    def print(self, n=np.inf):
        current = [self.root]
        nextone = []
        ii = 0
        while len(current) > 0:
            for nn in current:
                if nn != None:
                    print('{}({})'.format(nn.ID, nn.value), end="\t")
                    nextone.append(nn.left)
                    nextone.append(nn.right)
                elif nn == None:
                    print('{}({})'.format(nn, nn), end="\t")
            current = nextone
            nextone = []
            print('')
            ii += 1
            if ii > n:
                break



class SortedBinaryTree(BinaryTree):
    """
    Class for a sorted binary tree
    """

    def __init__(self, ll):
        """
        ll = list of objects that can be compared
        """
        self.root = None
        for nn in ll:
            self.insert(BinaryNode(nn, nn))

    def insert(self, node):
        if self.root == None:
            self.root = node
        else:
            nn = self.root
            while True:
                if node.value < nn.value:
                    if nn.left == None:
                        nn.addleftchild(node)
                        return
                    nn = nn.left
                else:
                    if nn.right == None:
                        nn.addrightchild(node)
                        return
                    nn = nn.right



class KDTree(BinaryTree):
    """
    Implement a kd-tree for partition of a multi-dimensional dataset
    """

    def __init__(self, ll, exact=True, samplesize=100):
        """
        ll = list of points
        """
        self.exact = exact
        self.samplesize = samplesize
        self.K = len(ll[0])
        self.ID = -1
        self.root = self.assignchild(ll, 0)
        

    def assignchild(self, ll, dim):
        pivot = self.findpivot(ll, dim)
        self.ID += 1
        pivotnode = BinaryNode(self.ID, pivot)
        left, right = self.split(ll, pivot, dim)
        
        if len(left) > 0:
            pivotnode.addleftchild(self.assignchild(left, (dim+1) % self.K))
        if len(right) > 0:
            pivotnode.addrightchild(self.assignchild(right, (dim+1) % self.K))

        return pivotnode


    def findpivot(self, ll, dim):
        """
        ll = list of points to find a pivot
        dim = dimension along which pivot is searched
        """
        if len(ll) == 1:
            return ll[0]
        else:
            # option 1: use exact median
            if self.exact or len(ll) <= self.samplesize:
                mylist = ll
            # option 2: use approx median
            else:
                mylist = [list(ii) \
                for ii in np.array(ll)[choice(len(ll), self.samplesize, replace=False)]]
            mylist.sort(key=(lambda x : x[dim]))
            return mylist[len(mylist)//2]


    def split(self, ll, pivot, dim):
        """
        split list ll in two groups with dim-coordinates lesser or greater
        than dim-coordinate of the pivot
        """
        lesser = []
        greater = []
        for xy in ll:
            if xy != pivot:
                if xy[dim] < pivot[dim]:
                    lesser.append(xy)
                else:
                    greater.append(xy)
        return lesser, greater
        





##########################################################
def test_binarytree():
    """
                    0
            1               2
        3       4       5       6
              7   8     9
    """
    nodes = []
    for ii in range(10):
        nodes.append(BinaryNode(ii,None))
    nodes[0].addleftchild(nodes[1])
    nodes[0].addrightchild(nodes[2])
    nodes[1].addleftchild(nodes[3])
    nodes[1].addrightchild(nodes[4])
    nodes[2].addleftchild(nodes[5])
    nodes[2].addrightchild(nodes[6])
    nodes[4].addleftchild(nodes[7])
    nodes[4].addrightchild(nodes[8])
    nodes[5].addleftchild(nodes[9])
    tt = BinaryTree(nodes[0])

    print('Testing tree traversals')
    print("Pre-order traversal")
    tt.preordertraversal()
    print("Post-order traversal")
    tt.postordertraversal()
    print("In-order traversal")
    tt.inordertraversal()


def test_sortedbinarytree():
    print('Testing sorted binary tree')
    ll = [5,4,7,9,6,8,1,3]
    print(ll)
    tt = SortedBinaryTree(ll)
    print('Inorder traversal returns sorted list')
    tt.inordertraversal()
    print('Preorder traversal')
    tt.print()


def test_kdtree():
    print('Test kd-tree')
    ll = [[2,3],[5,4],[9,6],[4,7],[8,1],[7,2]] # wikipedia example
    print('ll={}'.format(ll))
    tt = KDTree(ll)
    tt.print()

def test_kdtree_sample():
    print('Test kd-tree sampled')
    ll = [list(ii) for ii in randint(-10,10,200).reshape((-1,5))]
    b=[ii[0] for ii in ll]
    b.sort()
    print(b)
    print('Exact median')
    tt = KDTree(ll)
    tt.print(2)
    print('Sample-based median (5)')
    tt = KDTree(ll, False, 5)
    tt.print(2)
    print('Sample-based median (30)')
    tt = KDTree(ll, False, 30)
    tt.print(2)



if __name__ == "__main__":
    test_binarytree()
    test_sortedbinarytree()
    test_kdtree()
    test_kdtree_sample()
