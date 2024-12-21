import { FastifyReply, FastifyRequest } from "fastify";

export async function createToken(
	this: any,
	req: FastifyRequest,
	res: FastifyReply
) {
	try {
		const { name, symbol, supply, address } = req.body as any;
		const newToken = await this.tokens.saveTokenToDB({
			name,
			symbol,
			supply,
			address,
		});

		res.status(201).send(newToken);
	} catch (error) {
		res.status(500).send({ error: "Failed to create token" });
	}
}

export async function getTokens(
	this: any,
	req: FastifyRequest,
	res: FastifyReply
) {
	try {
		const { page = 1, limit = 10, sort = "createdAt" } = req.query as any;
		const tokens = await this.tokens.getTokensFromDB(
			Number(page),
			Number(limit),
			sort.toString()
		);
		res.send(tokens);
	} catch (error) {
		res.status(500).send({ error: "Failed to fetch tokens" });
	}
}

export async function getTokenByAddress(
	this: any,
	req: FastifyRequest,
	res: FastifyReply
) {
	try {
		const { address } = req.params as any;
		const token = await this.tokens.getTokenByAddress(address);
		res.send(token);
	} catch (error) {
		res.status(500).send({ error: "Failed to fetch tokens" });
	}
}
