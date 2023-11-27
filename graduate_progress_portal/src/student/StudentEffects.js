import { useEffect } from 'react';
import axios from 'axios';

axios.defaults.baseURL = 'http://127.0.0.1:8000';

export const useFetchStudent = (student_id, setStudent, setAdvisor, setProgram) => {
    useEffect(() => {
        if (!student_id) return;

        const fetchData = async () => {
            try {
                const studentResponse = await axios.get(`/students/${student_id}/`);
                setStudent(studentResponse.data);

                if (setAdvisor) {
                    const advisorsResponse = await axios.get(`/students/${student_id}/advisors`);
                    const mainAdvisor = advisorsResponse.data.find(advisor => advisor.advisor_role === 'main_advisor');
                    setAdvisor(mainAdvisor || null);
                }

                if (setProgram) {
                    const programsResponse = await axios.get(`/students/${student_id}/programs`);
                    setProgram(programsResponse.data[0] || null);
                }
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        };

        fetchData();
    }, [student_id, setStudent, setAdvisor, setProgram]);
};
