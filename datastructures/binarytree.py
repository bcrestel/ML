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
        print('ID={}'.format(self.ID))

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
    tt.preordertraversal()


if __name__ == "__main__":
    test_binarytree()
    test_sortedbinarytree()
