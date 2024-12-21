import { getTokenList } from "../api/memepolia/requests";

const TokenList = () => {
    const tokenList = getTokenList();
    const currentOrigin = window.location.origin; 

    return <div id="token-list">
        {tokenList.map(item => {
            return <a href={`${currentOrigin}/tokens/${item._id}`} className="token">
                <div className="info">
                    <h3>{item.name}</h3>
                    
                    <div className="symbol">Symbol: {item.symbol}</div>
                    <div className="supply">Supply: {item.supply}</div>
                    <div className="price">Price: {item.supply}</div>
                    <div className="address">Address: {item.address}</div>
                </div>
            </a>
        })}
    </div>
};

export { TokenList };
export default TokenList;