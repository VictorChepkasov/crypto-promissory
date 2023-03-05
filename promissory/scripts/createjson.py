import json

def createMetadata(promissoryInfoArr):
    dict = {
    "name": "NFT id - promissory number",
    "attributes": [
        {
            "trait_type": "holder address",
            "value": promissoryInfoArr[0]
        },
        {
            "trait_type": "debtor address",
            "value": promissoryInfoArr[1]
        },
        {
            "trait_type": "holder name",
            "value": promissoryInfoArr[2]
        },
        {
            "trait_type": "debtor name",
            "value": promissoryInfoArr[3]
        },
        {
            "trait_type": "commission in percents",
            "value": promissoryInfoArr[4]
        },
        {
            "trait_type": "amount",
            "value": promissoryInfoArr[5]
        },
        {
            "trait_type": "date of registration",
            "value": promissoryInfoArr[6]
        },
        {
            "trait_type": "date of close",
            "value": promissoryInfoArr[7]
        },
        {
            "trait_type": "date of holder consent",
            "value": promissoryInfoArr[8]
        },
        {
            "trait_type": "date of debtor consent",
            "value": promissoryInfoArr[9]
        },
        {
            "trait_type": "holder consent",
            "value": promissoryInfoArr[10]
        },
        {
            "trait_type": "debtor consent",
            "value": promissoryInfoArr[11]
        }
        ]
    }

    promissory_metadata = json.dumps(dict, indent=4)

    with open("promissory_metadata.json", "w") as outfile:
        outfile.write(promissory_metadata)
