import Web3 from "web3";
import { Database } from "../database";
import * as config from "../config/config";

export class BlockchainFetcher {
	private web3: Web3;
	private address: string;

	constructor(address: string, providerUrl: string, private db: Database) {
		this.web3 = new Web3(providerUrl);
		this.address = address;
	}

	public async listen(): Promise<void> {
		console.log(`Listening for new blocks...`);

		const sub = await this.web3.eth.subscribe("newBlockHeaders");
		sub.on("data", async (blockHeader) => {
			console.log(`New block received: ${blockHeader.number}`);

			try {
				const block = await this.web3.eth.getBlock(
					blockHeader.number,
					true
				);
				if (block && block.transactions) {
					block.transactions.forEach(async (tx: any) => {
						if (
							tx.from.toLowerCase() ===
								this.address.toLowerCase() &&
							tx.to === null
						) {
							const receipt =
								await this.web3.eth.getTransactionReceipt(
									tx.hash
								);
							if (receipt && receipt.contractAddress) {
								console.log(
									`Contract deployed at: ${receipt.contractAddress} in block ${blockHeader.number}`
								);
								const contract = new this.web3.eth.Contract(
									config.ABI,
									receipt.contractAddress
								);

								const name: string = await contract.methods
									.name()
									.call();
								const symbol: string = await contract.methods
									.symbol()
									.call();
								const supply: string = await contract.methods
									.totalSupply()
									.call();

								await this.db.createToken({
									name,
									symbol,
									supply,
									address: receipt.contractAddress,
								});
							} else {
								console.error(
									`Failed to fetch contract address for tx: ${tx.hash}`
								);
							}
						}
					});
				}
			} catch (error) {
				console.error("Error fetching block details:", error);
			}
		});
	}
}
