import { Database } from "../database";

export class TokenService {
	constructor(private db: Database) {}

	async saveTokenToDB(tokenData: {
		name: string;
		symbol: string;
		supply: string;
		address: string;
	}) {
		console.log("serv");
		return await this.db.createToken(tokenData);
	}

	async getTokensFromDB(data: {
		name?: string;
		page?: number;
		limit?: number;
		sort?: string;
	}) {
		const tokens = await this.db.getTokens(data);
		return tokens;
	}

	async getTokenByAddress(address: string) {
		return await this.db.getTokenByAddress(address);
	}
}
