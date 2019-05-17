import { studentService } from "../_services";

export const students = {
  namespaced: true,
  state: {
    students: []
  },
  actions: {
    async getStudents({ commit }) {
      const students = await studentService.getStudents();
      commit("getStudentsSuccess", students);
      return students;
    },
    async updateStudent({ commit }, student) {
      const updatedStudent = await studentService.updateStudent(student);
      commit("updateStudentSuccess", updatedStudent);
      return updatedStudent;
    },
    async createStudent({ commit }, student) {
      const newStudent = await studentService.createStudent(student);
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
      state.students.push(student);
    },
    reset(state) {
      state.students = [];
    }
  }
};
