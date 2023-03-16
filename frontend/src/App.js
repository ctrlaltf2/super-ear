// import logo from './logo.svg';
import './index.css';
import Navbar from "./components/navbar.jsx";
import { Routes, Route, Outlet } from 'react-router-dom'
import About from './pages/About';
import Achievements from './pages/Achievements';
import Dashboard from './pages/Dashboard';
import Stats from './pages/Stats';
import Play from './pages/Play';

function App() {
  return (
    <div>
    <Navbar/>
    <div>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="about" element={<About />} />
          <Route path="stats" element={<Stats />} />
          <Route path="achievements" element={<Achievements />} />
          <Route path="play" element={<Play />} />
        </Route>
      </Routes>
    </div>
    </div>
  );
}

function Layout(){
  return (
    <div>
    <Outlet />
    </div>
  );
}
export default App;
