"""
    vars.py
    Shard Core V 0.10
    Copyright (c) 2023 The ShardCoin developers
    Distributed under the MIT software license, see the accompanying
    For copying see http://opensource.org/licenses/mit-license.php.
"""

import mock, yaml

file_paths = mock.Mock()
file_paths.config = "data/config.yaml"
file_paths.peerlist = "data/peerlist.json"
file_paths.database = "data/database.json"
file_paths.privkey = "data/acc.priv"

Web3ChainID = 5151
CoinName = "ShardCoin"
IdealBlockTime = 300
BaseBlockReward = 2048 # base supply reward can't go lower than this
Interval = 105120 # Every two years blocks rewards get halved

try:
    data = yaml.safe_load(open(file_paths.config))
    MOTD = data["config"]["MOTD"]
    VER = "0.10"
except:
    print("No data/config.yaml found!")
    exit(0)