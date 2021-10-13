import hashlib
import copy
import pickle

class MerkleTree(object):
    def __init__(self):
        self.tree = [ [] ]

    def __str__(self):
        #return str(self.tree)
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
        tree = copy.deepcopy(self.tree)
        if len(tree[0])%2 != 0:
            tree[0].append(tree[0][-1])
        if item not in tree[0]: return None
        searched = item
        proof = []
        for x, level in enumerate(tree):
            if x+1 == len(tree): break
            #print(level, x)
            is_right = level.index(searched) % 2
            #print(level.index(searched))
            #print("is right:", is_right)
            if is_right == 0:
                #print("Get item to the right")
                #print(level[level.index(searched) + 1])
                proof.append( ['right', level[level.index(searched) + 1]] )
                searched = self.sha256(searched+level[level.index(searched) + 1])
            else:
                #print("Get item to the left")
                #print(level[level.index(searched) - 1])
                proof.append( ['left', level[level.index(searched) - 1]] )
                searched = self.sha256(level[level.index(searched) - 1]+searched)
            #print("Now searching for ", searched, x+1)

        #print(proof)
        self.verify_proof(item, proof)
        print(proof)
        return proof

    def verify_proof(self, item, proof):
        final_hash = item
        for step in proof:
            direction, hashed_data = step[0], step[1]
            if direction == 'right':
                final_hash = self.sha256(final_hash+hashed_data)
            elif direction == 'left':
                final_hash = self.sha256(hashed_data+final_hash)
        assert final_hash == self.tree[-1][0]
        return final_hash == self.tree[-1][0]
                
    def save_tree(self, path):
        with open(path, "wb+") as f:
            f.write( pickle.dumps(self.tree, protocol=4) )

    def load_tree(self, path):
        with open(path, "rb") as f:
            data = f.read()
            self.tree = pickle.loads(data)

    def clear_tree(self):
        self.tree = [ [] ]

if __name__ == "__main__":
    tree = MerkleTree()
    tree.add_child('a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3')
    tree.add_child('5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cacfc5')
    tree.add_child('ef797c8118f02dfb649607dd5d3f8c7623048c9c063d532cc95c5ed7a898a64f')
    print(tree.calculate_root())
    print(tree)
    print()
    proof = tree.get_proof('ef797c8118f02dfb649607dd5d3f8c7623048c9c063d532cc95c5ed7a898a64f')
    print(tree.verify_proof('ef797c8118f02dfb649607dd5d3f8c7623048c9c063d532cc95c5ed7a898a64f', proof))
    #tree.save_tree('data/tree.ctn')
    #tree.load_tree('data/tree.ctn')
    #print(tree)
