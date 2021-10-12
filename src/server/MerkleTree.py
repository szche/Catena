import hashlib
import copy

class MerkleTree(object):
    def __init__(self):
        self.tree = [ [] ]

    def __str__(self):
        msg = '-' * 50 + \
                f'\nMerkle tree root: {self.tree[-1][0]}\n'  + \
                f'Number of tree leaves: {len(self.tree[0])}\n' + \
                '-' * 10 + '\n' +  \
                '\n'.join([item for item in self.tree[0]]) + \
                '\n' + '-' * 50
        return msg 
    
    def sha256(self, data):
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    def add_child(self, child):
        self.tree[0].append(child)
        #self.calculate_root()

    def calculate_root(self):
        tree = copy.deepcopy(self.tree)
        if len(tree[0])%2 != 0:
            tree[0].append(tree[0][-1])
        for x, level in enumerate(tree):
            #print('Level: ', x)
            if len(level) % 2 != 0: break
            for y, a in enumerate(level[::2]):
                b = level[y+1]
                #print('Hashing: ', a, b)
                c = self.sha256(a+b)
                if x+1 >= len(tree): 
                    tree.append([])
                    self.tree.append([])
                #print(f'Pushing hash {c} to level {x+1}')
                tree[x+1].append(c)
                self.tree[x+1].append(c)
        #self.tree = tree
        return self.tree[-1][0]
                
    def get_proof(self, item):
        # Can only return proof for leaves in the tree
        if item not in self.tree[0]: return None
        searched = item
        proof = []
        for x, level in enumerate(self.tree):
            is_right = level.index(item) % 2
            if is_right == 0:
                proof.append('1')
        

    def clear_tree(self):
        self.tree = []
        self.root = None


if __name__ == "__main__":
    tree = MerkleTree()
    tree.add_child('a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3')
    tree.add_child('5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cacfc5')
    tree.add_child('ef797c8118f02dfb649607dd5d3f8c7623048c9c063d532cc95c5ed7a898a64f')
    print(tree.calculate_root())
    print(tree)
    #print(tree.tree)



