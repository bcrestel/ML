class Node():

    def __init__(self, ID, coord):
        self.ID = ID
        self.xy = coord
        self.children = []
        self.parent = None

    def addchild(self, node):
        self.children.append(node)
        node.addparent(self)

    def addparent(self, node):
        self.parent = node

    def print(self):
        print('ID={}'.format(self.ID))

    def preorder(self):
        self.print()
        for cc in self.children:
            cc.preorder()



class Tree():

    def __init__(self, root):
        self.root = root

    def preordertraversal(self):
        self.root.preorder()


if __name__ == "__main__":
    """
                    0
            1               2
        3       4       5       6
        7       8       9
    """
    nodes = []
    for ii in range(10):
        nodes.append(Node(ii,None))
    nodes[0].addchild(nodes[1])
    nodes[0].addchild(nodes[2])
    nodes[1].addchild(nodes[3])
    nodes[1].addchild(nodes[4])
    nodes[2].addchild(nodes[5])
    nodes[2].addchild(nodes[6])
    nodes[3].addchild(nodes[7])
    nodes[4].addchild(nodes[8])
    nodes[5].addchild(nodes[9])
    tt = Tree(nodes[0])
    tt.preordertraversal()
