import unittest
from io import BytesIO

from bip32 import (
    Bip32PrivateNode, Bip32PublicNode, correct_entropy_bits_value,
    mnemonic_sentence_length, mnemonic_from_entropy_bits, mnemonic_from_entropy,
    checksum_length
)
from helper import decode_base58_checksum


class TestMnemonic(unittest.TestCase):
    def test_correct_entropy_bits_value(self):
        for i in [128, 160, 192, 224, 256]:
            self.assertIsNone(correct_entropy_bits_value(i))
        self.assertRaises(
            ValueError,
            correct_entropy_bits_value, 45
        )
        self.assertRaises(
            ValueError,
            correct_entropy_bits_value, 1948
        )

    def test_checksum_length(self):
        self.assertEqual(checksum_length(entropy_bits=128), 4)
        self.assertEqual(checksum_length(entropy_bits=160), 5)
        self.assertEqual(checksum_length(entropy_bits=192), 6)
        self.assertEqual(checksum_length(entropy_bits=224), 7)
        self.assertEqual(checksum_length(entropy_bits=256), 8)

    def test_mnemonic_sentence_length(self):
        self.assertEqual(mnemonic_sentence_length(128), 12)
        self.assertEqual(mnemonic_sentence_length(160), 15)
        self.assertEqual(mnemonic_sentence_length(192), 18)
        self.assertEqual(mnemonic_sentence_length(224), 21)
        self.assertEqual(mnemonic_sentence_length(256), 24)

    def test_mnemonic_from_entropy(self):
        data = [
            (
                "551bf03d054209b3d512dc4090a5067ae4bd41e487d9f14e5f709551d23564fe",
                "fence test aunt appear calm supreme february fortune dog lunch dose volume envelope path must will vanish indicate switch click brush boy negative skate"
            ),
            (
                "2debf1019b6e9f94c23236c1f481491cfdd684ad2ababa759025273c508fa83f",
                "combine garbage document cycle try skill angle egg sea piano false delay talent drastic regret firm risk prosper announce example shallow elephant path toddler"
            ),
            (
                "690a5584effb0b696ed901454cf88ce5aaa0785b5e00c1e859a10f4d0e0e06f7",
                "harbor famous gentle that radar regret rocket cage earn guitar case slender present destroy hope scale sea drift hair burden special alpha bridge valid"
            ),
            (
                "bdfd931e398288992f60945db9e4e28a",
                "sadness uncle shy indoor chuckle erode rural barely frozen song december bicycle"
            ),
            (
                "96d646b36079d8c1197da69188b54388",
                "nothing rate proud science outside gauge grass regular muscle east extend axis"
            ),
            (
                "4518092f3642140265588ca4ca7e7029f0c39276",
                "eagle scare envelope hold candy abuse nice bag pill fault orchard fault around since sudden"
            ),
            (
                "f4206826684e9fbe32385374b7ede6b945331277",
                "vintage addict another spatial try tenant similar apology input satoshi keen income farm matrix teach"
            ),
            (
                "f01d7798f0a0af1febb296dda4292339fc575be6a439146f",
                "useless two tower throw april morning put fan tank candy emotion initial shell pupil once mango behave kitten"
            ),
            (
                "391022cbc6635d7c5940c61c7875e09c95a8fe1d0650424a",
                "decorate library real mimic cupboard sail govern boat broccoli senior join decrease fold lecture inject skate drastic feel"
            ),
            (
                "2ff28320dd4a0a4c42be5dff27e30388baa8d44e2ed3a65e493f14de",
                "copper neglect sight ritual pass change april slight you disease science badge pride health december surprise play venture exist claim topic"
            ),
            (
                "304ab49c9e033e22c7914ea51b298aad0152be2039372f5e0f9ada5a",
                "core fiber cheese despair crop badge bundle clap pink sun glance foam benefit gallery liberty cheap consider vacant trade regret police"
            )
        ]
        for entropy_hex, target_mnemonic in data:
            self.assertEqual(
                mnemonic_from_entropy(entropy=entropy_hex),
                target_mnemonic
            )

    def test_mnemonic_from_entropy_bits(self):
        self.assertEqual(
            len(mnemonic_from_entropy_bits(entropy_bits=128).split()),
            12
        )
        self.assertEqual(
            len(mnemonic_from_entropy_bits(entropy_bits=160).split()),
            15
        )
        self.assertEqual(
            len(mnemonic_from_entropy_bits(entropy_bits=192).split()),
            18
        )
        self.assertEqual(
            len(mnemonic_from_entropy_bits(entropy_bits=224).split()),
            21
        )
        self.assertEqual(
            len(mnemonic_from_entropy_bits(entropy_bits=256).split()),
            24
        )


class TestNode(unittest.TestCase):

    def test_parse(self):
        xpub = "xpub69H7F5d8KSRgmmdJg2KhpAK8SR3DjMwAdkxj3ZuxV27CprR9LgpeyGmXUbC6wb7ERfvrnKZjXoUmmDznezpbZb7ap6r1D3tgFxHmwMkQTPH"
        xpriv = "xprv9vHkqa6EV4sPZHYqZznhT2NPtPCjKuDKGY38FBWLvgaDx45zo9WQRUT3dKYnjwih2yJD9mkrocEZXo1ex8G81dwSM1fwqWpWkeS3v86pgKt"
        pub_node = Bip32PublicNode.parse(s=xpub)
        self.assertEqual(pub_node.extended_public_key(), xpub)
        self.assertEqual(Bip32PrivateNode.parse(s=xpriv).extended_private_key(), xpriv)

    def test_parse_incorrect_type(self):
        xpriv = "xprv9s21ZrQH143K3YFDmG48xQj4BKHUn15if4xsQiMwSKX8bZ6YruYK6mV6oM5Tbodv1pLF7GMdPGaTcZBno3ZejMHbVVvymhsS5GcYC4hSKag"
        self.assertEqual(Bip32PrivateNode.parse(xpriv).extended_private_key(), xpriv)
        self.assertEqual(Bip32PrivateNode.parse(decode_base58_checksum(xpriv)).extended_private_key(), xpriv)
        self.assertEqual(Bip32PrivateNode.parse(BytesIO(decode_base58_checksum(xpriv))).extended_private_key(), xpriv)
        self.assertRaises(ValueError, Bip32PrivateNode.parse, 1584784554)

    def test_check_fingerprint(self):
        xpriv = "xprv9s21ZrQH143K4EK4Fdy4ddWeDMy1x4tg2s292J5ynk23sn3hxSZ9MqqLZCTj2dHPP16CsTdAFeznbnNhSN3v66TtSKzJf4hPZSqDjjp9t42"
        m = Bip32PrivateNode.parse(xpriv)
        self.assertIsNone(m.check_fingerprint())
        m0 = m.ckd(index=0)
        m0._parent_fingerprint = m.fingerprint()
        self.assertTrue(m0.check_fingerprint())


class TestBip32(unittest.TestCase):

    def test_ckd_pub_ckd_priv_matches_public_key(self):
        seed = "b4385b54033b047216d71031bd83b3c059d041590f24c666875c980353c9a5d3322f723f74d1f5e893de7af80d80307f51683e13557ad1e4a2fe151b1c7f0d8b"
        m = Bip32PrivateNode.master_key(bip32_seed=bytes.fromhex(seed))
        master_xpub = m.extended_public_key()
        M = Bip32PublicNode.parse(s=master_xpub)
        m44 = m.ckd(index=44)
        M44 = M.ckd(index=44)
        self.assertEqual(m44.extended_public_key(), M44.extended_public_key())
        self.assertEqual(m44.extended_public_key(), "xpub68gENos6i4PQxkSjJB2Ww79EfUVX8J4nrTHYzUWa3q6gMivLymbzHiu1MBoxi3fVDUQVi61Lv7brNs18sHjzdBVgCXocZxDwrsGrAf4GN3T")
        m440 = m44.ckd(index=0)
        M440 = M44.ckd(index=0)
        self.assertEqual(m440.extended_public_key(), M440.extended_public_key())
        self.assertEqual(m440.extended_public_key(), "xpub6AotjNzqVqVCmdvqAsMi2zNEDCobz7s9zit2pfdKPPc9LQ2GwSGybYDKuqDGC7mVhSWNZBNeRwqtjvA7rX4ACKXa8GrnD5XQkGb542RuzZ5")
        m440thousand = m440.ckd(index=1000)
        M440thousand = M440.ckd(index=1000)
        self.assertEqual(
            m440thousand.extended_public_key(),
            M440thousand.extended_public_key()
        )
        self.assertEqual(
            m440thousand.extended_public_key(),
            "xpub6CqqMNRRTuyJNyP6VNCxY1SJWNY4t2QsmsWTsBmiZyUvbYDKMU77DaDJpeqMqNkzwCuTqXghQ58DbhNVpe9r2vtuvPSvwUWNB2Wc6RWh3US"
        )
        m440thousand__ = m440thousand.ckd(index=2**31-1)
        M440thousand__ = M440thousand.ckd(index=2**31-1)
        self.assertEqual(
            m440thousand__.extended_public_key(),
            M440thousand__.extended_public_key()
        )
        self.assertEqual(
            m440thousand__.extended_public_key(),
            "xpub6EtrsXwXdacQ9iDpmqTeYpu8AstEBrwiXbpdoVU4Q1yhjmN5c8Niw2KvJRwSGS4VtndPgCuHH15SstUzENBksqpVP8YxzubWcERugoDafnq"
        )
        m440thousand__0 = m440thousand__.ckd(index=0)
        M440thousand__0 = M440thousand__.ckd(index=0)
        self.assertEqual(
            m440thousand__0.extended_public_key(),
            M440thousand__0.extended_public_key()
        )
        self.assertEqual(
            m440thousand__0.extended_public_key(),
            "xpub6FymQUeMhBdyk57T6P9oAZVcPTniJyXWHYKxzurkT6u729eC8bdtzdP6i4RShvHrnKpiEhhZHY2kQBYxyKJPFUbUzum7w6a3W4JdADuCisC"
        )

    def test_ckd_pub_hardened_failure(self):
        xpub = "xpub6FUwZTpNvcMeHRJGUQoy4WTqXjzmGLUFNe3sUKeWChEbzTJDpBjZjn2cMysV5Ffw874VUVooxmupZeLjrdpM5wXLUxkatTdnayXGy6Ln7kR"
        M = Bip32PublicNode.parse(s=xpub)
        self.assertRaises(RuntimeError, M.ckd, 2**31)
        self.assertRaises(RuntimeError, M.ckd, 2**31 + 256)

    def test_vector_1(self):
        # Chain m
        seed ="000102030405060708090a0b0c0d0e0f"
        xpub = "xpub661MyMwAqRbcFtXgS5sYJABqqG9YLmC4Q1Rdap9gSE8NqtwybGhePY2gZ29ESFjqJoCu1Rupje8YtGqsefD265TMg7usUDFdp6W1EGMcet8"
        xpriv = "xprv9s21ZrQH143K3QTDL4LXw2F7HEK3wJUD2nW2nRk4stbPy6cq3jPPqjiChkVvvNKmPGJxWUtg6LnF5kejMRNNU3TGtRBeJgk33yuGBxrMPHi"
        m = Bip32PrivateNode.master_key(bip32_seed=bytes.fromhex(seed))
        self.assertEqual(m.extended_public_key(), xpub)
        self.assertEqual(m.extended_private_key(), xpriv)
        self.assertEqual(m.__repr__(), "m")

        # chain m/0'
        xpub = "xpub68Gmy5EdvgibQVfPdqkBBCHxA5htiqg55crXYuXoQRKfDBFA1WEjWgP6LHhwBZeNK1VTsfTFUHCdrfp1bgwQ9xv5ski8PX9rL2dZXvgGDnw"
        xpriv = "xprv9uHRZZhk6KAJC1avXpDAp4MDc3sQKNxDiPvvkX8Br5ngLNv1TxvUxt4cV1rGL5hj6KCesnDYUhd7oWgT11eZG7XnxHrnYeSvkzY7d2bhkJ7"
        m0h = m.ckd(index=2**31)
        self.assertEqual(m0h.extended_public_key(), xpub)
        self.assertEqual(m0h.extended_private_key(), xpriv)
        self.assertEqual(m0h.__repr__(), "m/0'")

        # chain M/0'
        M0h = Bip32PublicNode.parse(xpub)
        # chain M/0'/1
        M0h1 = M0h.ckd(index=1)
        public_only_xpub = M0h1.extended_public_key()

        # chain m/0'/1
        xpub = "xpub6ASuArnXKPbfEwhqN6e3mwBcDTgzisQN1wXN9BJcM47sSikHjJf3UFHKkNAWbWMiGj7Wf5uMash7SyYq527Hqck2AxYysAA7xmALppuCkwQ"
        xpriv = "xprv9wTYmMFdV23N2TdNG573QoEsfRrWKQgWeibmLntzniatZvR9BmLnvSxqu53Kw1UmYPxLgboyZQaXwTCg8MSY3H2EU4pWcQDnRnrVA1xe8fs"
        m0h1 = m0h.ckd(index=1)
        self.assertEqual(public_only_xpub, xpub)
        self.assertEqual(m0h1.extended_public_key(), xpub)
        self.assertEqual(m0h1.extended_private_key(), xpriv)
        self.assertEqual(m0h1.__repr__(), "m/0'/1")

        # chain m/0'/1/2'
        xpub = "xpub6D4BDPcP2GT577Vvch3R8wDkScZWzQzMMUm3PWbmWvVJrZwQY4VUNgqFJPMM3No2dFDFGTsxxpG5uJh7n7epu4trkrX7x7DogT5Uv6fcLW5"
        xpriv = "xprv9z4pot5VBttmtdRTWfWQmoH1taj2axGVzFqSb8C9xaxKymcFzXBDptWmT7FwuEzG3ryjH4ktypQSAewRiNMjANTtpgP4mLTj34bhnZX7UiM"
        m0h12h = m0h1.ckd(index=2**31+2)
        self.assertEqual(m0h12h.extended_public_key(), xpub)
        self.assertEqual(m0h12h.extended_private_key(), xpriv)
        self.assertEqual(m0h12h.__repr__(), "m/0'/1/2'")

        # chain m/0'/1/2'/2
        xpub = "xpub6FHa3pjLCk84BayeJxFW2SP4XRrFd1JYnxeLeU8EqN3vDfZmbqBqaGJAyiLjTAwm6ZLRQUMv1ZACTj37sR62cfN7fe5JnJ7dh8zL4fiyLHV"
        xpriv = "xprvA2JDeKCSNNZky6uBCviVfJSKyQ1mDYahRjijr5idH2WwLsEd4Hsb2Tyh8RfQMuPh7f7RtyzTtdrbdqqsunu5Mm3wDvUAKRHSC34sJ7in334"
        m0h12h2 = m0h12h.ckd(index=2)
        self.assertEqual(m0h12h2.extended_public_key(), xpub)
        self.assertEqual(m0h12h2.extended_private_key(), xpriv)
        self.assertEqual(m0h12h2.__repr__(), "m/0'/1/2'/2")

        # chain M/0'/1/2'/2
        M0h12h2 = Bip32PublicNode.parse(xpub)
        # chain M/0'/1/2'/2/1000000000
        M0h12h21000000000 = M0h12h2.ckd(index=1000000000)
        public_only_xpub = M0h12h21000000000.extended_public_key()

        # chain m/0'/1/2'/2/1000000000
        xpub = "xpub6H1LXWLaKsWFhvm6RVpEL9P4KfRZSW7abD2ttkWP3SSQvnyA8FSVqNTEcYFgJS2UaFcxupHiYkro49S8yGasTvXEYBVPamhGW6cFJodrTHy"
        xpriv = "xprvA41z7zogVVwxVSgdKUHDy1SKmdb533PjDz7J6N6mV6uS3ze1ai8FHa8kmHScGpWmj4WggLyQjgPie1rFSruoUihUZREPSL39UNdE3BBDu76"
        m0h12h21000000000 = m0h12h2.ckd(index=1000000000)
        self.assertEqual(m0h12h21000000000.extended_public_key(), xpub)
        self.assertEqual(public_only_xpub, xpub)
        self.assertEqual(m0h12h21000000000.extended_private_key(), xpriv)
        self.assertEqual(m0h12h21000000000.__repr__(), "m/0'/1/2'/2/1000000000")

    def test_vector_2(self):
        # Chain m
        seed = "fffcf9f6f3f0edeae7e4e1dedbd8d5d2cfccc9c6c3c0bdbab7b4b1aeaba8a5a29f9c999693908d8a8784817e7b7875726f6c696663605d5a5754514e4b484542"
        xpub = "xpub661MyMwAqRbcFW31YEwpkMuc5THy2PSt5bDMsktWQcFF8syAmRUapSCGu8ED9W6oDMSgv6Zz8idoc4a6mr8BDzTJY47LJhkJ8UB7WEGuduB"
        xpriv = "xprv9s21ZrQH143K31xYSDQpPDxsXRTUcvj2iNHm5NUtrGiGG5e2DtALGdso3pGz6ssrdK4PFmM8NSpSBHNqPqm55Qn3LqFtT2emdEXVYsCzC2U"
        m = Bip32PrivateNode.master_key(bip32_seed=bytes.fromhex(seed))
        self.assertEqual(m.extended_public_key(), xpub)
        self.assertEqual(m.extended_private_key(), xpriv)
        self.assertEqual(m.__repr__(), "m")

        # Chain m/0
        xpub = "xpub69H7F5d8KSRgmmdJg2KhpAK8SR3DjMwAdkxj3ZuxV27CprR9LgpeyGmXUbC6wb7ERfvrnKZjXoUmmDznezpbZb7ap6r1D3tgFxHmwMkQTPH"
        xpriv = "xprv9vHkqa6EV4sPZHYqZznhT2NPtPCjKuDKGY38FBWLvgaDx45zo9WQRUT3dKYnjwih2yJD9mkrocEZXo1ex8G81dwSM1fwqWpWkeS3v86pgKt"
        m0 = m.ckd(index=0)
        self.assertEqual(m0.extended_public_key(), xpub)
        self.assertEqual(m0.extended_private_key(), xpriv)
        self.assertEqual(m0.__repr__(), "m/0")

        # Chain m/0/2147483647'
        xpub = "xpub6ASAVgeehLbnwdqV6UKMHVzgqAG8Gr6riv3Fxxpj8ksbH9ebxaEyBLZ85ySDhKiLDBrQSARLq1uNRts8RuJiHjaDMBU4Zn9h8LZNnBC5y4a"
        xpriv = "xprv9wSp6B7kry3Vj9m1zSnLvN3xH8RdsPP1Mh7fAaR7aRLcQMKTR2vidYEeEg2mUCTAwCd6vnxVrcjfy2kRgVsFawNzmjuHc2YmYRmagcEPdU9"
        m02147483647h = m0.ckd(index=2**31+2147483647)
        self.assertEqual(m02147483647h.extended_public_key(), xpub)
        self.assertEqual(m02147483647h.extended_private_key(), xpriv)
        self.assertEqual(m02147483647h.__repr__(), "m/0/2147483647'")

        # Chain m/0/2147483647'/1
        xpub = "xpub6DF8uhdarytz3FWdA8TvFSvvAh8dP3283MY7p2V4SeE2wyWmG5mg5EwVvmdMVCQcoNJxGoWaU9DCWh89LojfZ537wTfunKau47EL2dhHKon"
        xpriv = "xprv9zFnWC6h2cLgpmSA46vutJzBcfJ8yaJGg8cX1e5StJh45BBciYTRXSd25UEPVuesF9yog62tGAQtHjXajPPdbRCHuWS6T8XA2ECKADdw4Ef"
        m02147483647h1 = m02147483647h.ckd(index=1)
        self.assertEqual(m02147483647h1.extended_public_key(), xpub)
        self.assertEqual(m02147483647h1.extended_private_key(), xpriv)
        self.assertEqual(m02147483647h1.__repr__(), "m/0/2147483647'/1")

        # Chain m/0/2147483647'/1/2147483646'
        xpub = "xpub6ERApfZwUNrhLCkDtcHTcxd75RbzS1ed54G1LkBUHQVHQKqhMkhgbmJbZRkrgZw4koxb5JaHWkY4ALHY2grBGRjaDMzQLcgJvLJuZZvRcEL"
        xpriv = "xprvA1RpRA33e1JQ7ifknakTFpgNXPmW2YvmhqLQYMmrj4xJXXWYpDPS3xz7iAxn8L39njGVyuoseXzU6rcxFLJ8HFsTjSyQbLYnMpCqE2VbFWc"
        m02147483647h12147483646h = m02147483647h1.ckd(index=2**31+2147483646)
        self.assertEqual(m02147483647h12147483646h.extended_public_key(), xpub)
        self.assertEqual(m02147483647h12147483646h.extended_private_key(), xpriv)
        self.assertEqual(m02147483647h12147483646h.__repr__(), "m/0/2147483647'/1/2147483646'")

        # Chain m/0/2147483647'/1/2147483646'/2
        xpub = "xpub6FnCn6nSzZAw5Tw7cgR9bi15UV96gLZhjDstkXXxvCLsUXBGXPdSnLFbdpq8p9HmGsApME5hQTZ3emM2rnY5agb9rXpVGyy3bdW6EEgAtqt"
        xpriv = "xprvA2nrNbFZABcdryreWet9Ea4LvTJcGsqrMzxHx98MMrotbir7yrKCEXw7nadnHM8Dq38EGfSh6dqA9QWTyefMLEcBYJUuekgW4BYPJcr9E7j"
        m02147483647h12147483646h2 = m02147483647h12147483646h.ckd(index=2)
        self.assertEqual(m02147483647h12147483646h2.extended_public_key(), xpub)
        self.assertEqual(m02147483647h12147483646h2.extended_private_key(), xpriv)
        self.assertEqual(m02147483647h12147483646h2.__repr__(), "m/0/2147483647'/1/2147483646'/2")

    def test_vector_3(self):
        # Chain m
        seed = "4b381541583be4423346c643850da4b320e46a87ae3d2a4e6da11eba819cd4acba45d239319ac14f863b8d5ab5a0d0c64d2e8a1e7d1457df2e5a3c51c73235be"
        xpub = "xpub661MyMwAqRbcEZVB4dScxMAdx6d4nFc9nvyvH3v4gJL378CSRZiYmhRoP7mBy6gSPSCYk6SzXPTf3ND1cZAceL7SfJ1Z3GC8vBgp2epUt13"
        xpriv = "xprv9s21ZrQH143K25QhxbucbDDuQ4naNntJRi4KUfWT7xo4EKsHt2QJDu7KXp1A3u7Bi1j8ph3EGsZ9Xvz9dGuVrtHHs7pXeTzjuxBrCmmhgC6"
        m = Bip32PrivateNode.master_key(bip32_seed=bytes.fromhex(seed))
        self.assertEqual(m.extended_public_key(), xpub)
        self.assertEqual(m.extended_private_key(), xpriv)
        self.assertEqual(m.__repr__(), "m")

        # chain m/0'
        xpub = "xpub68NZiKmJWnxxS6aaHmn81bvJeTESw724CRDs6HbuccFQN9Ku14VQrADWgqbhhTHBaohPX4CjNLf9fq9MYo6oDaPPLPxSb7gwQN3ih19Zm4Y"
        xpriv = "xprv9uPDJpEQgRQfDcW7BkF7eTya6RPxXeJCqCJGHuCJ4GiRVLzkTXBAJMu2qaMWPrS7AANYqdq6vcBcBUdJCVVFceUvJFjaPdGZ2y9WACViL4L"
        m0h = m.ckd(index=2 ** 31)
        self.assertEqual(m0h.extended_public_key(), xpub)
        self.assertEqual(m0h.extended_private_key(), xpriv)
        self.assertEqual(m0h.__repr__(), "m/0'")
