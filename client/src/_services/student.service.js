import axios from "axios";
import config from "../_config";

async function getStudents() {
  const res = await axios.get(`${config.apiUrl}students/`);
  return res.data;
}

async function updateStudent(student) {
  const res = await axios.put(
    `${config.apiUrl}students/${student.id}/`,
    student
  );
  return res.data;
}

async function createStudent(student) {
  const res = await axios.post(`${config.apiUrl}students/`, student);
  return res.data;
}

export const studentService = {
  getStudents,
  updateStudent,
  createStudent
};
