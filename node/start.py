"""
    start.py
    Shard Core V 0.10
    Copyright (c) 2023 The ShardCoin developers
    Distributed under the MIT software license, see the accompanying
    For copying see http://opensource.org/licenses/mit-license.php.
"""

import threading

from src.core import rgbPrint
from src.web import runNode
from src.gui import runapp

rgbPrint("Starting Node...", "green")

if __name__ == "__main__":
    t1 = threading.Thread(target=runNode)
    t2 = threading.Thread(target=runapp)
    t1.start()
    t2.start()
