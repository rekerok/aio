WETH_CONTRACTS = {
    "ethereum": "0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",
    "optimism": "0x4200000000000000000000000000000000000006",
    "arbitrum": "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1",
    "nova": "0x722E8BdD2ce80A4422E880164f2079488e115365",
    "base": "0x4200000000000000000000000000000000000006",
    "zkera": "0x5AEa5775959fBC2557Cc8789bC1bf90A239D9a91",
    "linea": "0xe5d7c2a44ffddf6b295a15c148167daaaf5cf34f",
    "bsc": "0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c",  # WBNB
    "polygon": "0x0d500B1d8E8eF31E21C99d1Db9A6444d3ADf1270",  # WMATIC
    "avalanche": "0xb31f66aa3c1e785363f0875a1b74e27b85fd66c7",  # WAVAX
}
SUSHI_ROUTERS = {
    "ethereum": "0xd9e1cE17f2641f24aE83637ab66a2cca9C378B9F",
    "arbitrum": "0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506",
    "nova": "0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506",
    "base": "0x6BDED42c6DA8FBf0d2bA55B2fa120C5e0c8D7891",
    "bsc": "0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506",
    "polygon": "0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506",
    "avalanche": "0x1b02dA8Cb0d097eB8D57A175b88c7D8b47997506",
}

WOOFI_SWAP = {
    "optimism": "0xEAf1Ac8E89EA0aE13E0f03634A4FF23502527024",
    "arbitrum": "0x9aEd3A8896A85FE9a8CAc52C9B402D092B629a30",
    "linea": "0x39d361E66798155813b907A70D6c2e3FdaFB0877",
    "base": "0x27425e9FB6A9A625E8484CFD9620851D1Fa322E5",
    "bsc": "0x4f4Fd4290c9bB49764701803AF6445c5b03E8f06",
    "polygon": "0x817Eb46D60762442Da3D931Ff51a30334CA39B74",
    "polygon_zk": "0x39d361E66798155813b907A70D6c2e3FdaFB0877",
    "avalanche": "0xC22FBb3133dF781E6C25ea6acebe2D2Bb8CeA2f9",
    "zkera": "0xfd505702b37Ae9b626952Eb2DD736d9045876417",
}

ODOS_SWAP = {
    "optimism": "0xCa423977156BB05b13A2BA3b76Bc5419E2fE9680",
    "arbitrum": "0xa669e7A0d4b3e4Fa48af2dE86BD4CD7126Be4e13",
    "base": "0x19cEeAd7105607Cd444F5ad10dd51356436095a1",
    "bsc": "0x89b8AA89FDd0507a99d334CBe3C808fAFC7d850E",
    "polygon": "0x4E3288c9ca110bCC82bf38F09A7b425c095d92Bf",
    "polygon_zk": "0x2b8B3f0949dfB616602109D2AAbBA11311ec7aEC",
    "avalanche": "0x88de50B233052e4Fb783d4F6db78Cc34fEa3e9FC",
    "zkera": "0x4bBa932E9792A2b917D47830C93a9BC79320E4f7",
}

# https://syncswap.gitbook.io/syncswap/smart-contracts/smart-contracts
SYNCSWAP = {
    "zkera": {
        "pool_factory": "0xf2DAd89f2788a8CD54625C60b55cD3d2D0ACa7Cb",
        "router": "0x2da10A1e27bF85cEdD8FFb1AbBe97e53391C0295",
    },
    "linea": {
        "pool_factory": "0x37BAc764494c8db4e54BDE72f6965beA9fa0AC2d",
        "router": "0x80e38291e06339d10AAB483C65695D004dBD5C69",
    },
    "scroll": {
        "pool_factory": "0x37BAc764494c8db4e54BDE72f6965beA9fa0AC2d",
        "router": "0x80e38291e06339d10AAB483C65695D004dBD5C69",
    },
}

IZUMI_SWAP = {
    "bsc": "0xedf2021f41AbCfE2dEA4427E1B61f4d0AA5aA4b8",
    "arbitrum": "0x01fDea353849cA29F778B2663BcaCA1D191bED0e",
    "polygon": "0x032b241De86a8660f1Ae0691a4760B426EA246d7",
    "zkera": "0x943ac2310D9BC703d6AB5e5e76876e212100f894",
    "linea": "0x032b241De86a8660f1Ae0691a4760B426EA246d7",
    "base": "0x02F55D53DcE23B4AA962CC68b0f685f26143Bdb2",
    "scroll": "0x2db0AFD0045F3518c77eC6591a542e326Befd3D7",
}

# https://minter.merkly.com/why
MERKLY = {
    "zkera": "0x5673B6e6e51dE3479B8deB22dF46B12308db5E1e",
    "optimism": "0xD7bA4057f43a7C4d4A34634b2A3151a60BF78f0d",
    "avalanche": "0x5C9BBE51F7F19f8c77DF7a3ADa35aB434aAA86c5",
    "nova": "0xB6789dACf323d60F650628dC1da344d502bC41E3",
    "bsc": "0xeF1eAE0457e8D56A003d781569489Bc5466E574b",
    "arbitrum": "0x4Ae8CEBcCD7027820ba83188DFD73CCAD0A92806",
    "polygon": "0x0E1f20075C90Ab31FC2Dd91E536e6990262CF76d",
    "base": "0x6bf98654205B1AC38645880Ae20fc00B0bB9FFCA",
    "linea": "0xc9B753d73B17DDb5E87093ff04A9e31845a43af0",
}

LAYERZERO_CHAINS_ID = {
    "ethereum": 101,
    "bsc": 102,
    "avalanche": 106,
    "polygon": 109,
    "arbitrum": 110,
    "optimism": 111,
    "fantom": 112,
    "dfk": 115,
    "harmony": 116,
    "dexalot": 118,
    "celo": 125,
    "moonbeam": 126,
    "fuse": 138,
    "gnosis": 145,
    "dos": 149,
    "klaytn": 150,
    "metis": 151,
    "core": 153,
    "polygon_zk": 158,
    "canto": 159,
    "zkera": 165,
    "moonriver": 167,
    "tenet": 173,
    "nova": 175,
    "meter": 176,
    "kava": 177,
    "mantle": 181,
    "linea": 183,
    "base": 184,
    "zora": 195,
    "viction": 196,
    "loot": 197,
    "beam": 198,
    "telos": 199,
    "opbnb": 202,
    "astar": 210,
    "aurora": 211,
    "conflux": 212,
    "orderly": 213,
    "scroll": 214,
    "horizen": 215,
    "xpla": 216,
    "manta": 217,
    "shimmerEVM": 230,
}

NATIVE_TOKEN = "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"
ZERO_ADDRESS = "0x0000000000000000000000000000000000000000"
