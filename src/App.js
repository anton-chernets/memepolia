import logo from './logo.svg';
import './App.css';
import { TokenList } from './components/TokenList';
import { Route, Routes } from 'react-router-dom';
import TokenPage from './components/TokenPage';

function App() {
  return (
    <div className="App">
      <Routes>
        <Route path="/" element={<TokenList />}></Route>
        <Route path="/tokens/:uuid" element={<TokenPage />}></Route>
      </Routes>
    </div>
  );
}

export default App;
