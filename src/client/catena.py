


class Catena(object):
    def __init__(self, genesis_tx):
        self.genesis_tx = genesis_tx
        self.statements = []

    def verifyTx(self, tx, chainTip):
        print(tx)

        # Verify that tx is confirmed
        assert tx['status']['confirmed'] == True, 'Tx is not confirmed'

        # Verify that tx is confirmed with at least 6 confirmations
        assert chainTip-tx['status']['block_height'] >=6, 'Tx has less than 6 confirmations'
        
        pass

    def verifyBlock(self, block):
        pass

    def verifyStatement(self, statement):
        pass


    
