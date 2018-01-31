class BinaryNode():

    def __init__(self, ID, coord):
        self.ID = ID
        self.xy = coord
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

    def __init__(self, root):
        self.root = root

    def preordertraversal(self):
        self.root.preorder()

    def postordertraversal(self):
        self.root.postorder()

    def inordertraversal(self):
        self.root.inorder()


if __name__ == "__main__":
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

    print("Pre-order traversal")
    tt.preordertraversal()
    print("Post-order traversal")
    tt.postordertraversal()
    print("In-order traversal")
    tt.inordertraversal()
