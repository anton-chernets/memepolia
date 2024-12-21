const getTokenList = () => {
    return [
        {
            "_id": "6766d5d643959b8b510fc8a4",
            "name": "Test Token",
            "symbol": "TT",
            "supply": "100000000000000000000",
            "address": "0xdAC17F958D2ee523a2206206994597C12D731ec7"
        },
        {
            "_id": "6766d5f68b900bb453503d01",
            "name": "Test Token",
            "symbol": "TT",
            "supply": "100000000000000000000",
            "address": "0xdAC17F958D2ee523a2106206994597C12D731ec7"
        },
        {
            "_id": "6766d54c777e71a3b4e464fb",
            "name": "Test Token",
            "symbol": "TT",
            "supply": "100000000000000000000",
            "address": "0xdAC17F958D2ee523a2206206994597C13D731ec7"
        },
        {
            "_id": "6766d5ca0775980df1213ee4",
            "name": "Test Token",
            "symbol": "TT",
            "supply": "100000000000000000000",
            "address": "0xdAC17F958D2ee523a2206206994597C13D731ec7"
        },
        {
            "_id": "6766d5ad0775980df1213ee2",
            "name": "Test Token",
            "symbol": "TT",
            "supply": "100000000000000000000",
            "address": "0xdAC17F958D2ee523a2206206994597C13D731ec7"
        },
        {
            "_id": "6766d4ad0c71f624dad2e766",
            "name": "Test Token",
            "symbol": "TT",
            "supply": "100000000000000000000",
            "address": "0xdAC17F958D2ee523a2206206994597C13D831ec7"
        },
        {
            "_id": "6766d4820c71f624dad2e764",
            "name": "Test Token",
            "symbol": "TT",
            "supply": "100000000000000000000",
            "address": "0xdAC17F958D2ee523a2206206994597C13D831ec7"
        },
        {
            "_id": "6766d42acf822dfe189d4683",
            "name": "Test Token",
            "symbol": "TT",
            "supply": "100000000000000000000",
            "address": "0xdAC17F958D2ee523a2206206994597C13D831ec7"
        },
        {
            "_id": "6766d4a60c71f624dad2e765",
            "name": "Test Token",
            "symbol": "TT",
            "supply": "100000000000000000000",
            "address": "0xdAC17F958D2ee523a2206206994597C13D831ec7"
        },
        {
            "_id": "6766d5b00775980df1213ee3",
            "name": "Test Token",
            "symbol": "TT",
            "supply": "100000000000000000000",
            "address": "0xdAC17F958D2ee523a2206206994597C13D731ec7"
        }
    ];
}

const getTokenById = (id) => {
    return getTokenList().find(el => {
        return el._id === id ? el : false
    });
}

const memopolia = { getTokenList, getTokenById };

export { getTokenList, getTokenById };
export default memopolia;