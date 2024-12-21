import { useParams } from "react-router-dom";
import { getTokenById } from "../api/memepolia/requests";

const TokenPage = (props) => {
    const params = useParams();

    const token = getTokenById(params.uuid);

    return <div id="token-content">
        <div className="info">
            <h3>{token.name}</h3>
                    
            <div className="symbol">Symbol: {token.symbol}</div>
            <div className="supply">Supply: {token.supply}</div>
            <div className="price">Price: {token.supply}</div>
            <div className="address">Address: {token.address}</div>
        </div>
    </div>;
}

export { TokenPage };
export default TokenPage;