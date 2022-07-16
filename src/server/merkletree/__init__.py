import hashlib
import copy
import math
import pickle
import typing
import os
from typing import List

EMPTY_LEAF = "EMPTY"


class MerkleTree(object):
    def __init__(self):
        self.tree = [ [] ]
        # height is also number of required leaves to structure a merkle tree
        # 2 ** (height-1) = required leaves 
        self._height = 0
        

    def __str__(self) -> str:

        msg = '-' * 50 + \
                f'\nMerkle tree root: {self.tree[-1][0]}\n'  + \
                f'Number of tree leaves: {len(self.tree[0])}\n' + \
                '-' * 10 + '\n' +  \
                '\n'.join([item for item in self.tree[0]]) + \
                '\n' + '-' * 50
        return msg

    def sha256(self, data: str) -> str:
        """
        Calculate hash, using sha256 algorithm

        :param str data: String that we want to hash
        :return str: hash

        """
        return hashlib.sha256(data.encode('utf-8')).hexdigest()

    def _add_empty_leaves(self):
        """
        Scale up and down the tree by adding special type of leaf - EMPTY_LEAF.
        Function calculates the height of tree by incrementing integer part of logarithm of number of leaves
        """

        if len(self.tree[0]) == 1:
            #special case
            self.tree[0].append(EMPTY_LEAF)
            self.tree.append([])
            self.tree[1].append(self.tree[0][0])
            self._height = 2
        elif len(self.tree[0]) == (2 ** (self._height - 1)):
            pass
        else:
            self.tree.append([])
            self._height += 1

            current_length_of_leaves = len(self.tree[0])
            required_leaves_power = int(math.log2(current_length_of_leaves)) + 1 # bo nastepna potega 2jki
            required_levels = required_leaves_power + 1 # bo jak mamy np 4 (2 ** 2) liscie to wysokosc bedzie 3

            for i in range(required_levels-1, -1, -1):
                required_elements = 2 ** i

                which_level = (-1 * i) - 1
                missing = required_elements - len(self.tree[which_level]) 
                for j in range( missing ):
                    self.tree[which_level].append(EMPTY_LEAF)


    def add_child(self, child: str):
        """
        Add new leaf to tree. If there is an EMPTY_LEAF then function replace it with new child.
        Then we execure _add_empty_leaves() to scale the tree.
        Then we execute calculate_root() to recount the tree to potentially obtain new root

        :param str child: new leaf -- hash
        """
        if EMPTY_LEAF in self.tree[0]:
            index = self.tree[0].index(EMPTY_LEAF) # first element
            self.tree[0][index] = child
        else:
            self.tree[0].append(child)

        self._add_empty_leaves()
        self.calculate_root()

    def calculate_root(self):
        """
        Calculate the tree with merkle tree rules.

        """
        tree = copy.deepcopy(self.tree)

        for index, level in enumerate(tree):

            if len(level) == 1: break # LEVEL with root

            for index_in_level in range(0, len(level), 2):
                left_element_in_level = level[index_in_level]
                right_element_in_level = level[index_in_level+1]

                if left_element_in_level == EMPTY_LEAF:
                    new = EMPTY_LEAF
                else:
                    if right_element_in_level == EMPTY_LEAF:
                        new = left_element_in_level
                    else:
                        new = self.sha256(left_element_in_level+right_element_in_level)

                level_up_hash_index = int(index_in_level / 2)
                tree[index+1][level_up_hash_index] = new
                self.tree[index+1][level_up_hash_index] = new
        self.tree = tree

    def get_root(self) -> str:
        """
        Return the root of the tree

        :return str: root of the tree
        """
        return self.tree[-1][0]

    def get_proof(self, item: str) -> List[List[str]]:
        """
        Find a path of item to root. Function creates 2D array, in which there is a list of [place, another hash] arrays,
        where place is one of right, left, up. 
        In case of EMPTY_LEAF, the place = up.

        :param str item: item to check
        :return List[List[str]]: the proof object
        """

        if item not in self.tree[0]: return None
        
        tree = copy.deepcopy(self.tree)
        searched = item
        proof = []

        for index, level in enumerate(tree):
            if index+1 == len(tree): break
            is_right = True if level.index(searched) % 2 == 1 else False 

            if is_right:
                if level[level.index(searched) - 1] == EMPTY_LEAF:
                    proof.append( ['up', level[level.index(searched)]])
                else:
                    proof.append( ['right', level[level.index(searched) - 1] ])
                    searched = self.sha256(level[level.index(searched) - 1] + searched)
            else:
                if level[level.index(searched) + 1] == EMPTY_LEAF:
                    proof.append( ['up', level[level.index(searched)]])
                else:
                    proof.append( ['left', level[level.index(searched) + 1] ])
                    searched = self.sha256(searched + level[level.index(searched) + 1])

        #self.verify_proof(item, proof)
        return proof
    
    def verify_proof(self, item: str, proof: List[List[str]]) -> bool:
        """
        Verify if leaf belongs to merkle tree
        
        :param str item: an item to check
        :param List[List[str]]: a proof - path to the root
        :return bool: response if leaf belongs to tree
        """
        final_hash = item
        for step in proof:
            direction, hashed_data = step[0], step[1]
            if direction == 'left':
                final_hash = self.sha256(final_hash+hashed_data)
            elif direction == 'right':
                final_hash = self.sha256(hashed_data+final_hash)
            elif direction == 'up':
                continue
            print("Jestem final hash " + final_hash)
        assert final_hash == self.get_root()
        return final_hash == self.get_root()

    def save_tree(self, path: str):
        """
        Save tree to a file in serialized format

        :param str path: path to a file
        """
        cwd = os.getcwd()
        path = f'{cwd}/merkletree/tree_archive/{path}'
        with open(path, "wb+") as f:
            f.write( pickle.dumps(self.tree, protocol=4) )

    def load_tree(self, path: str):
        """
        Load a tree from a file

        :param str path: a path to a file
        """
        cwd = os.getcwd()
        path = f'{cwd}/merkletree/tree_archive/{path}'
        with open(path, "rb") as f:
            data = f.read()
            self.tree = pickle.loads(data)

    def clear_tree(self):
        """ 
        Clear a tree.
        """
        self.tree = [ [] ]
  
if __name__ == "__main__":
    tree = MerkleTree()
    tree.add_child('a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3')
    tree.add_child('5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cacfc5')
    tree.add_child('ef797c8118f02dfb649607dd5d3f8c7623048c9c063d532cc95c5ed7a898a64f')
    tree.add_child('asdfasdfasdfasdfasdfasdfa5d3f8c7623048c9c063d532cc95c5edasdasdad')
    tree.add_child('hgyuinghuingynuisdfa5d3f8c7623048c9c063d532cc95c5gynuigynuigynigni')

    tree.save_tree(tree.get_root())
    """
    tree.add_child('rty6bfybnuisdfa5d3f8c7623048c9c063d532cc95c5gynuigynuigynigni')
    print(tree)
    proof = tree.get_proof('ef797c8118f02dfb649607dd5d3f8c7623048c9c063d532cc95c5ed7a898a64f')
    print(proof)
    print(tree.verify_proof('ef797c8118f02dfb649607dd5d3f8c7623048c9c063d532cc95c5ed7a898a64f', proof))
    """