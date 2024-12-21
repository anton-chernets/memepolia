import Fastify, { FastifyInstance } from "fastify";
import cors from "@fastify/cors";
import {
	createToken,
	getTokens,
	getTokenByAddress,
} from "./handlers/tokenHandler";
import { TokenService } from "../services/tokenService";

export class Api {
	protected constructor(private fastify: FastifyInstance) {}

	public static async create(tokens: TokenService) {
		const fastify = Fastify({
			logger: true,
		});

		await fastify.register(cors, { origin: "*" });

		fastify.decorate("tokens", tokens);

		fastify.post("/api/tokens", createToken);
		fastify.get("/api/tokens", getTokens);
		fastify.get("/api/token/:address", getTokenByAddress);

		return new Api(fastify);
	}

	serve(port: number) {
		console.log(`Starting API server on port ${port}`);
		return this.fastify.listen({ host: "0.0.0.0", port });
	}
}
