import hashlib
import json
import time
import os

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        sha = hashlib.sha256()
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash
        }, sort_keys=True).encode()
        sha.update(block_string)
        return sha.hexdigest()

class Blockchain:
    def __init__(self, storage_path="instance/blockchain.json"):
        self.storage_path = storage_path
        self.chain = []
        self._load_chain()
        if not self.chain:
            self._create_genesis_block()

    def _create_genesis_block(self):
        genesis_block = Block(0, time.time(), "Genesis Block - System Initialized", "0")
        self.chain.append(genesis_block)
        self._save_chain()

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, data):
        latest_block = self.get_latest_block()
        new_block = Block(
            index=latest_block.index + 1,
            timestamp=time.time(),
            data=data,
            previous_hash=latest_block.hash
        )
        self.chain.append(new_block)
        self._save_chain()
        return new_block

    def _save_chain(self):
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        chain_data = []
        for block in self.chain:
            chain_data.append({
                "index": block.index,
                "timestamp": block.timestamp,
                "data": block.data,
                "previous_hash": block.previous_hash,
                "hash": block.hash
            })
        with open(self.storage_path, "w") as f:
            json.dump(chain_data, f, indent=4)

    def _load_chain(self):
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r") as f:
                    chain_data = json.load(f)
                    for block_dict in chain_data:
                        block = Block(
                            block_dict["index"],
                            block_dict["timestamp"],
                            block_dict["data"],
                            block_dict["previous_hash"]
                        )
                        block.hash = block_dict["hash"]
                        self.chain.append(block)
            except Exception as e:
                print(f"Error loading blockchain: {e}")
                self.chain = []

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True
