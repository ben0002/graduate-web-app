// import axios from 'axios';


// {/* Student Service will house all student API calls*/}
// const STUDENT_API_BASE_URL = "http://localhost:8080/api/v1/students";

// export const fetchStudentById = async (studentId) => {
//     try {
//         const response = await axios.get(`${STUDENT_API_BASE_URL}/${studentId}`);
//         return response.data;
//     } catch (error) {
//         console.log("Error in fetchStudentById: ", error);
//         throw error;
//     }
// };

// export const fetchStudentNameById = async (studentId) => {
//     try {
//         const response = await axios.get(`${STUDENT_API_BASE_URL}/${studentId}/name`);
//         return response.data;
//     } catch (error) {
//         console.log("Error in fetchStudentNameById: ", error);
//         throw error;
//     }
// }