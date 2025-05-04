import './App.css';
import Home from './pages/Home';
import { useEffect } from 'react';

function App() {

  useEffect(() => {
    const fetchData = async () => {


    };

    fetchData();
    const interval = setInterval(fetchData, 5000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="App">
      <Home />
    </div>
  );
}

export default App;
