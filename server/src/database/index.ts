import { Db, MongoClient } from "mongodb";

export class Database {
	protected constructor(private db: Db) {}

	static async connect(uri: string, databaseName: string): Promise<Database> {
		const client = await MongoClient.connect(uri);
		return new Database(client.db(databaseName));
	}

	async createToken(tokenData: {
		name: string;
		symbol: string;
		supply: string;
		address: string;
	}) {
		const existingToken = await this.db.collection("tokens").findOne({
			address: tokenData.address,
		});

		if (existingToken) {
			console.log(
				`Token with address ${tokenData.address} already exists.`
			);
			throw new Error("token exist");
		}
		return await this.db.collection("tokens").insertOne(tokenData);
	}

	async getTokens({
		page = 1,
		limit = 10,
		orderBy = "createdAt",
	}) {
		const skip = (page - 1) * limit;

		return await this.db
			.collection("tokens")
			.aggregate([
				{
					$sort: { [orderBy]: -1 },
				},
				{
					$skip: skip,
				},
				{
					$limit: limit,
				},
			])
			.toArray();
	}

	async getTokenByAddress(address: string) {
		return await this.db.collection("tokens").findOne({ address: address });
	}
}
