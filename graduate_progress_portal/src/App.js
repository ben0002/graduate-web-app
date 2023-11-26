import { BrowserRouter, Routes, Route } from "react-router-dom";
import { LocalizationProvider } from '@mui/x-date-pickers';
import { AdapterDayjs } from '@mui/x-date-pickers/AdapterDayjs'

import MainLayout from './layouts/mainLayout';
import Login from './pages/login.js';
import AdvisorView from './pages/advisor/advisorView.js';
import StudentLayout from './layouts/studentLayout';
import StudentProgress from './pages/student/StudentProgress.js';
import StudentProfile from './pages/student/StudentProfile.js';
import NotFound from './pages/notFound.js';

import { studentData } from './assets/data/SampleStudentData.jsx';

function App() { 
  return (
    <LocalizationProvider dateAdapter={AdapterDayjs}>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<MainLayout/>}>
            <Route index element={<Login/>}/>
            <Route path="advisor" element={<AdvisorView/>}/>
            <Route path="student" element={<StudentLayout/>}>
              <Route path="progress" element={<StudentProgress/>} /> 
              <Route path="profile" element={<StudentProfile/>}/>
              <Route path="*" element={<NotFound/>}/>
            </Route>
            <Route path="*" element={<NotFound/>}/>
          </Route>
        </Routes>
      </BrowserRouter>
    </LocalizationProvider>
  );
}

export default App;
