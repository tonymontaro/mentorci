import axios from "../_config";
import router from "../router";

export const students = {
  namespaced: true,
  state: {
    students: []
  },
  actions: {
    async getStudents({ commit }) {
      const students = (await axios.get(`students/`)).data;
      commit("getStudentsSuccess", students);
      return students;
    },
    async updateStudent({ commit }, student) {
      const updatedStudent = (await axios.put(
        `students/${student.id}/`,
        student
      )).data;
      commit("updateStudentSuccess", updatedStudent);
      return updatedStudent;
    },
    async deleteStudent({ commit }, student) {
      await axios.delete(`students/${student.id}`);
      commit("deleteStudentSuccess", student);
      router.push("/");
    },
    async createStudent({ commit }, student) {
      const newStudent = (await axios.post(`students/`, student)).data;
      commit("createStudentSuccess", newStudent);
      return newStudent;
    }
  },
  mutations: {
    getStudentsSuccess(state, students) {
      state.students = students;
    },
    updateStudentSuccess(state, student) {
      state.students = state.students.map(st =>
        st.id == student.id ? student : st
      );
    },
    createStudentSuccess(state, student) {
      state.students.unshift(student);
    },
    deleteStudentSuccess(state, student) {
      state.students = state.students.filter(st => st.id != student.id);
    },
    reset(state) {
      state.students = [];
    }
  }
};
