class Networks:
    ethereum = {
        "name": "ethereum",
        "rpc": [
            "https://eth.llamarpc.com",
            "wss://ethereum.publicnode.com",
            "https://rpc.mevblocker.io",
        ],
        "scan": "https://etherscan.io/",
        "eip1559": True,
        "token": "ETH",
        "check_gas": True,
    }

    arbitrum = {
        "name": "arbitrum",
        "rpc": [
            "https://arbitrum.llamarpc.com",
            "wss://arbitrum-one.publicnode.com",
            "https://endpoints.omniatech.io/v1/arbitrum/one/public",
        ],
        "scan": "https://arbiscan.io/",
        "eip1559": True,
        "token": "ETH",
        "check_gas": True,
    }

    optimism = {
        "name": "optimism",
        "rpc": [
            "https://optimism.llamarpc.com",
            "wss://optimism.publicnode.com",
            "https://mainnet.optimism.io",
        ],
        "scan": "https://optimistic.etherscan.io/",
        "eip1559": True,
        "token": "ETH",
        "check_gas": False,
    }

    base = {
        "name": "base",
        "rpc": ["https://base.llamarpc.com"],
        "scan": "https://basescan.org/",
        "eip1559": True,
        "token": "ETH",
        "check_gas": False,
    }

    zksync = {
        "name": "zkera",
        "rpc": [
            "https://mainnet.era.zksync.io",
            "https://zksync-era.blockpi.network/v1/rpc/public",
        ],
        "scan": "https://explorer.zksync.io/",
        "eip1559": False,
        "token": "ETH",
        "check_gas": True,
    }

    avalanche = {
        "name": "avalanche",
        "rpc": [
            "https://avalanche.drpc.org",
        ],
        "scan": "https://snowtrace.io/",
        "eip1559": True,
        "token": "AVAX",
        "check_gas": False,
    }

    polygon = {
        "name": "polygon",
        "rpc": [
            "https://rpc.ankr.com/polygon/6eb719a8acb9be4873e5616d579ee1dd2f1f20cd08be5f76cd50a2ce3753e260",
        ],
        "scan": "https://polygonscan.com/",
        "eip1559": True,
        "token": "MATIC",
        "check_gas": False,
    }

    scroll = {
        "name": "scroll",
        "rpc": [
            "https://scroll.blockpi.network/v1/rpc/public",
            "https://rpc-scroll.icecreamswap.com",
            "https://rpc.ankr.com/scroll",
        ],
        "scan": "https://scrollscan.com/",
        "eip1559": False,
        "token": "ETH",
        "check_gas": False,
    }

    linea = {
        "name": "linea",
        "rpc": [
            "https://linea.blockpi.network/v1/rpc/public",
            "https://rpc.linea.build",
        ],
        "scan": "https://lineascan.build/",
        "eip1559": False,
        "token": "ETH",
        "check_gas": True,
    }
