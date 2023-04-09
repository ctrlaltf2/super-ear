// import logo from './logo.svg';
import './index.css';
import Navbar from "./components/navbar.jsx";
import * as React from 'react';
import { Routes, Route, Outlet } from 'react-router-dom'
import {Oval} from 'react-loader-spinner';

const Dashboard = React.lazy(() => import('./pages/Dashboard'));
const About = React.lazy(() => import('./pages/About'));
const Achievements = React.lazy(() => import('./pages/Achievements'));
const Stats = React.lazy(() => import('./pages/Stats'));
import Play from './pages/Play';

function App() {
  return (
    <div>
    <Navbar/>
    <div>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route 
            index 
            element={
            <React.Suspense fallback={<Loading />}>
            <Dashboard />
            </React.Suspense>
          } />

          <Route path="about" 
            element={<React.Suspense fallback={<Loading />}>
            <About />
            </React.Suspense>
          } />

          <Route path="stats" 
            element={<React.Suspense fallback={<Loading />}>
            <Stats />
            </React.Suspense>} />

          <Route path="achievements" 
            element={<React.Suspense fallback={<Loading />}>
            <Achievements />
            </React.Suspense>} />
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

function Loading(){
  return (
    <div className = "min-h-screen bg-black">
      <div className = "flex min-h-screen justify-center items-center text-8xl text-white">
          <Oval
              color="white"
              secondaryColor="black"
          />
      </div>
    </div>
  )
}
export default App;
