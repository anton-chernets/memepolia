export const DB_URL =
	process.env.DB_URL ?? "mongodb://admin:password@localhost:27017";
export const DB_NAME = "memopolia";

export const API_PORT = process.env.API_PORT ?? 8000;

export const PROVIDER_URL = "wss://base-sepolia-rpc.publicnode.com";

export const AGENT_ADDRESS = "0x74c45F7799760A0839c231551b53872783ac029b";

export const ABI = [
	{
		constant: true,
		inputs: [],
		name: "name",
		outputs: [
			{
				name: "",
				type: "string",
			},
		],
		type: "function",
	},
	{
		constant: true,
		inputs: [],
		name: "symbol",
		outputs: [
			{
				name: "",
				type: "string",
			},
		],
		type: "function",
	},
	{
		constant: true,
		inputs: [],
		name: "decimals",
		outputs: [
			{
				name: "",
				type: "uint8",
			},
		],
		type: "function",
	},
	{
		constant: true,
		inputs: [],
		name: "totalSupply",
		outputs: [
			{
				name: "",
				type: "uint256",
			},
		],
		type: "function",
	},
	{
		constant: true,
		inputs: [
			{
				name: "_owner",
				type: "address",
			},
		],
		name: "balanceOf",
		outputs: [
			{
				name: "balance",
				type: "uint256",
			},
		],
		type: "function",
	},
	{
		constant: true,
		inputs: [
			{
				name: "_spender",
				type: "address",
			},
		],
		name: "allowance",
		outputs: [
			{
				name: "remaining",
				type: "uint256",
			},
		],
		type: "function",
	},
	{
		constant: false,
		inputs: [
			{
				name: "_to",
				type: "address",
			},
			{
				name: "_value",
				type: "uint256",
			},
		],
		name: "transfer",
		outputs: [
			{
				name: "",
				type: "bool",
			},
		],
		type: "function",
	},
	{
		constant: false,
		inputs: [
			{
				name: "_spender",
				type: "address",
			},
			{
				name: "_value",
				type: "uint256",
			},
		],
		name: "approve",
		outputs: [
			{
				name: "",
				type: "bool",
			},
		],
		type: "function",
	},
	{
		constant: false,
		inputs: [
			{
				name: "_from",
				type: "address",
			},
			{
				name: "_to",
				type: "address",
			},
			{
				name: "_value",
				type: "uint256",
			},
		],
		name: "transferFrom",
		outputs: [
			{
				name: "",
				type: "bool",
			},
		],
		type: "function",
	},
	{
		anonymous: false,
		inputs: [
			{
				indexed: true,
				name: "owner",
				type: "address",
			},
			{
				indexed: true,
				name: "spender",
				type: "address",
			},
			{
				indexed: false,
				name: "value",
				type: "uint256",
			},
		],
		name: "Approval",
		type: "event",
	},
	{
		anonymous: false,
		inputs: [
			{
				indexed: true,
				name: "from",
				type: "address",
			},
			{
				indexed: true,
				name: "to",
				type: "address",
			},
			{
				indexed: false,
				name: "value",
				type: "uint256",
			},
		],
		name: "Transfer",
		type: "event",
	},
];
