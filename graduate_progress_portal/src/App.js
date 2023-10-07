import './assets/styling/App.css';
import { BrowserRouter, Routes, Route } from "react-router-dom";

import MainLayout from './layouts/mainLayout';
import Login from './pages/login';
import AdvisorView from './pages/advisorView';
import StudentLayout from './layouts/studentLayout';
import StudentProgress from './pages/studentProgress';
import StudentProfile from './pages/studentProfile';
import NotFound from './pages/notFound';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<MainLayout/>}>
          <Route index element={<Login/>}/>
          <Route path="advisor" element={<AdvisorView/>}/>
          <Route path="student" element={<StudentLayout/>}>
            <Route index element={<StudentProgress/>}/> {/* should this be index, '/', or '/progress' */}
            <Route path="profile" element={<StudentProfile/>}/>
            <Route path="*" element={<NotFound/>}/>
          </Route>
          <Route path="*" element={<NotFound/>}/>
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
