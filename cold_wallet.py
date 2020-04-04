from bip32_hd_wallet import (
    mnemonic_from_entropy, mnemonic_from_entropy_bits, PrivKeyNode, PubKeyNode,
    bip32_seed_from_mnemonic
)
from helper import hash160, h160_to_p2sh_address, p2wpkh_script_serialized

# m/44'/0'/0'/0
from wallet_utils import Bip32Path, Version, Key, Bip

BIP44_PATH = [44 + 2**31, 2**31, 2**31, 0]
# m/49'/0'/0'/0
BIP49_PATH = [49 + 2**31, 2**31, 2**31, 0]
# m/84'/0'/0'/0
BIP84_PATH = [84 + 2**31, 2**31, 2**31, 0]


class ColdWallet(object):

    __slots__ = (
        "mnemonic",
        "testnet",
        "password",
        "master"
    )

    def __init__(self, testnet=False, entropy=None, entropy_bits=256,
                 mnemonic=None, password="", master=None):
        self.testnet = testnet
        if master is None:
            if mnemonic is None:
                if entropy is None:
                    self.mnemonic = mnemonic_from_entropy_bits(
                        entropy_bits=entropy_bits
                    )
                else:
                    self.mnemonic = mnemonic_from_entropy(entropy=entropy)
            else:
                self.mnemonic = mnemonic

            self.password = password
            self.master = PrivKeyNode.master_key(
                bip32_seed=bip32_seed_from_mnemonic(
                    mnemonic=self.mnemonic,
                    password=password
                )
            )
        else:
            self.master = master

    def __eq__(self, other):
        return self.mnemonic == other.mnemonic \
               and self.password == other.password

    @property
    def watch_only(self):
        return False if type(self.master) == PrivKeyNode else True

    @classmethod
    def from_mnemonic(cls, mnemonic: str, password: str = "", testnet=False):
        return cls(
            mnemonic=mnemonic,
            password=password,
            testnet=testnet
        )

    def _from_pub_key(self, children, addr_type):
        return [
            [
                str(child),
                child.public_key.address(
                    testnet=self.testnet,
                    addr_type=addr_type
                ),
                child.public_key.sec().hex(),
                None if self.watch_only else child.private_key.wif(
                    testnet=self.testnet
                )
            ]
            for child in children
        ]

    def _bip44(self, children):
        return self._from_pub_key(children=children, addr_type="p2pkh")

    def bip44(self, interval=(0, 20)):
        res = []
        index_list = BIP44_PATH
        if self.testnet:
            index_list[1] += 1
        node = self.master.derive_path(index_list=index_list)
        for child in node.generate_children(interval=interval):
            res.append([
                str(child),
                child.public_key.address(testnet=self.testnet),
                child.public_key.sec().hex(),
                child.private_key.wif(testnet=self.testnet)
            ])
        return res

    def _bip49(self, children):
        return [
            [
                str(child),
                h160_to_p2sh_address(
                    h160=hash160(
                        p2wpkh_script_serialized(child.public_key.h160())
                    ),
                    testnet=self.testnet
                ),
                child.public_key.sec().hex(),
                None if self.watch_only else child.private_key.wif(
                    testnet=self.testnet
                )
            ]
            for child in children
        ]

    def bip49(self, interval=(0, 20)):
        res = []
        index_list = BIP49_PATH
        if self.testnet:
            index_list[1] += 1
        node = self.master.derive_path(index_list=index_list)
        for child in node.generate_children(interval=interval):
            res.append([
                str(child),
                h160_to_p2sh_address(
                    h160=hash160(
                        p2wpkh_script_serialized(child.public_key.h160())
                    ),
                    testnet=self.testnet
                ),
                child.public_key.sec().hex(),
                child.private_key.wif(testnet=self.testnet),

            ])
        return res

    def _bip84(self, children):
        return self._from_pub_key(children=children, addr_type="p2wpkh")

    def bip84(self, interval=(0, 20)):
        index_list = BIP84_PATH
        if self.testnet:
            index_list[1] += 1
        node = self.master.derive_path(index_list=index_list)
        return self._bip84(children=node.generate_children(interval=interval))

    def generate(self):
        return {
            "bip44": self.bip44(),
            "bip49": self.bip49(),
            "bip84": self.bip84(),
        }

    @classmethod
    def from_extended_key(cls, extended_key: str):
        # just need version, key type does not matter in here
        version_int = PrivKeyNode.parse(s=extended_key)._parsed_version
        version = Version.parse(s=version_int)
        if version.key_type == Key.PRV:
            node = PrivKeyNode.parse(extended_key, testnet=version.testnet)
        else:
            # is this just assuming? or really pub if not priv
            node = PubKeyNode.parse(extended_key, testnet=version.testnet)
        return cls(testnet=version.testnet, master=node)


if __name__ == "__main__":
    w = ColdWallet.from_extended_key(extended_key="vpub5b14oTd3mpWGzbxkqgaESn4Pq1MkbLbzvWZju8Y6LiqsN9JXX7ZzvdCp1qDDxLqeHGr6BUssz2yFmUDm5Fp9jTdz4madyxK6mwgsCvYdK5S")

    import pprint
    pprint.pprint(w._bip84(w.master.generate_children()))
    print(w.watch_only)
    x = 1

