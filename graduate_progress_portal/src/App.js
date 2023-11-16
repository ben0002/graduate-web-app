import { BrowserRouter, Routes, Route } from "react-router-dom";

import MainLayout from './layouts/mainLayout';
import Login from './shared/pages/login.js';
import AdvisorView from './advisor/advisorView.js';
import StudentLayout from './layouts/studentLayout';
import StudentProgress from './student/pages/StudentProgress.js';
import StudentProfile from './student/pages/StudentProfile.js';
import NotFound from './shared/pages/notFound.js';

import { studentData } from './student/studentData.jsx';

function App() { 
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<MainLayout/>}>
          <Route index element={<Login/>}/>
          <Route path="advisor" element={<AdvisorView/>}/>
          <Route path="student" element={<StudentLayout/>}>
            <Route path="progress" element={<StudentProgress student={studentData}/>} /> 
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
