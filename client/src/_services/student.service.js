import axios from "../_config";

async function getStudents() {
  const res = await axios.get(`students/`);
  return res.data;
}

async function updateStudent(student) {
  const res = await axios.put(`students/${student.id}/`, student);
  return res.data;
}

async function createStudent(student) {
  const res = await axios.post(`students/`, student);
  return res.data;
}

export const studentService = {
  getStudents,
  updateStudent,
  createStudent
};
