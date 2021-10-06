# Introduction

xLux is a one-stop shop for limited and exclusive techniques, strategies, and experiences with the best in the world.

## Reset Wallets

All API requests interact with wallets that are currently stored in memory. They are automatically generated as needed throughout the demo. However, if there's any type of glitch/bug, you can force reset the wallets and it might fix your issues.

```http
POST 127.0.0.1:8080/resetwallets
```

| Parameter | Type | Description |
| :--- | :--- | :--- |
| ---- | ---- | ---- |


## Response

```javascript
{'status':'OK'}
```


## Get Current Wallets

This endpoint gets the current address for the NFT issuer, distributor, and buyer for visual purposes. You will only use this API if you are interested in showing wallet addresses.

```http
POST 127.0.0.1:8080/getwallets
```

| Parameter | Type | Description |
| :--- | :--- | :--- |
| ---- | ---- | ---- |

## Response

```javascript
{'issuer':'rBtjVaE8pXaXCgiExAQfMaZCVEzSR7qCms', 'distributor':'rXCgiExAQfMaZCVEzSR7qCmsBtjVaE8pXa', 'buyer':'rVEzSR7qCmXCgiExAQfMaZCsBtjVaE8pXa'}
```

## Get All NFTs that are for sale

This endpoint gets all NFTs that are for sale on xLux. It will only return the NFTs that were minted through our platform.

```http
POST 127.0.0.1:8080/nftsforsale
```

| Parameter | Type | Description |
| :--- | :--- | :--- |
| ---- | ---- | ---- |

## Response

```javascript
{
    "data": [
        {
            "amount": 1,
            "currencycode": "47726561744E6174650000000000000000000000",
            "description": "Showing how to satisfy Nate",
            "issuer": "rBtjVaE8pXaXCgiExAQfMaZCVEzSR7qCms",
            "memodata": "53686f77696e6720686f7720746f2073617469736679204e6174650a75726c3a2068747470733a2f2f746573742e636f6d",
            "memotype": "74657874",
            "name": "GreatNate",
            "scientificamount": "1000000000000000e-96",
            "sellprice": "100",
            "transactionhash": "8B2FB02625ACEFBBF10570D55AD55DA42BBF12BE13668C4B66A039B94A4B6019",
            "url": "https://test.com"
        },
        ...
        ...
        ...
    ]
}
```

## Mint a NFT and Create an Offer to buy it

This endpoint will first mint the NFT using the built-in issuer and distribution accounts and then it will open a 'selling' position on the XRP Ledger. The transaction will be added to the database so it can be used on the endpoint that lists nfts for sale.

```http
POST 127.0.0.1:8080/mint
```

Form-Data
| Parameter | Type | Description |
| :--- | :--- | :--- |
| `name` | `string` | `NFT name` |
| `description` | `string` | `NFT description` |
| `sellprice` | `string` | `Price in XRP for 1 token. If you sell more than 1 tokens, we calculate that automatically.` |
| `url` | `string` | `url of the xLux NFT` |


## Response
Will return the address of the NFT owner and the URL transactions on the XRP Ledger. (the saleTransaction shows that NFTOwnerAccount has the NFT they minted)

```javascript
res = {'mintingTransaction':'https://explorer-testnet.xrplf.org/tx/6C669098CE3402595B1F2ED1F5BCDCBD0C7DF09CC4E2F763998A87960A7DB68C', 'NFTOwnerAccount': 'rXCgiExAQfMaZCVEzSR7qCmsBtjVaE8pXa', 'saleTransaction':'https://explorer-testnet.xrplf.org/tx/6C669098CE3402595B1F2ED1F5BCDCBD0C7DF09CC4E2F763998A87960A7DB68C'}
```


## Buy an NFT that was listed on xLux

This endpoint is the most complicated because it depends on the data that you request from `/nftsforsale`. It will use the built-in buyer wallet to fulfill the order from someone selling the NFT.

My recommendation is that you first get all data from `/nftsforsale` and then you will send the data for 1 specific NFT that someone is trying to buy as shown below:

```http
POST 127.0.0.1:8080/buy
```

| Parameter | Type | Description |
| :--- | :--- | :--- |
| `transactionhash` | `string` | `comes from /nftsforsale -> data[i].transactionhash` |
| `issueraddress` | `string` | `comes from /nftsforsale -> data[i].issuer` |
| `currencycode` | `string` | `comes from /nftsforsale -> data[i].currencycode` |
| `amount` | `string` | `comes from /nftsforsale -> data[i].scientificamount` **SUPER IMPORTANT THAT YOU USE data[i].scientificamount** |
| `sellprice` | `string` | `comes from /nftsforsale -> data[i].sellprice`|
| `memodata` | `string` | `comes from /nftsforsale -> data[i].memodata`|
| `memotype` | `string` | `comes from /nftsforsale -> data[i].memotype`|

## Response
Returns the address of the buyer as well as the URL transaction on the XRP Ledger

```javascript
{
    "buyerAddress": "rnFLos8BHxLksEYkWSnJqYiWahGFDeatUh",
    "buyingTransaction": "https://explorer-testnet.xrplf.org/tx/696582D9641E4C5882C141ED278DFE9BF64C8984304DCBF19C72E99F45CC422B"
}
```
