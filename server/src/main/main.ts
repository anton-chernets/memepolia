import { TokenService } from "./../services/tokenService";
import * as config from "../config/config";
import { Api } from "../api";
import { Database } from "../database";
import { BlockchainFetcher } from "../services/blockchainFetcher";

async function main() {
	const db = await Database.connect(config.DB_URL, config.DB_NAME);

	const tokenService = new TokenService(db);
	const fetcher = new BlockchainFetcher(
		config.AGENT_ADDRESS,
		config.PROVIDER_URL,
		db
	);

	const api = await Api.create(tokenService);

	await Promise.all([api.serve(+config.API_PORT)]);
	await fetcher.listen();
}

main();
