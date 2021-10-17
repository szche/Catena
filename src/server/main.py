import threading
from BitcoinRPC import BitcoinRPC
from MerkleTree import MerkleTree
from config import BITCOIN_RPC_USER, BITCOIN_RPC_PASS, BITCOIN_WALLET_LABEL

if __name__ == "__main__":
    # Start Web server thread


    # Create MerkleTree Object
	print("Loading Merkle Tree...")
	merkle_tree = MerkleTree()
	merkle_tree.load_tree('data/tree.ctn')
	print(merkle_tree)
	print("Merkle Tree running")

    # Create BitcoinRPC Object
	print("Loading Bitcoin RPC..")
	bitcoin_rpc = BitcoinRPC(BITCOIN_RPC_USER, BITCOIN_RPC_PASS, BITCOIN_WALLET_LABEL)
	print("Bitcoin RPC running")
