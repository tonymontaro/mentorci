import axios from "../_config";
import router from "../router";

export const students = {
  namespaced: true,
  state: {
    students: [],
    feedback: []
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
    },
    async createFeedback({ commit }, feedback) {
      const newFeedback = (await axios.post("feedback/", feedback)).data;
      commit("createFeedbackSuccess", newFeedback);
      return newFeedback;
    },
    async getFeedback({ commit }, studentId) {
      const feedback = (await axios.get(`student/${studentId}/feedback/`)).data;
      commit("getFeedbackSuccess", feedback);
      return feedback;
    },
    async deleteFeedback({ commit }, feedbackId) {
      await axios.delete(`feedback/${feedbackId}/`);
      commit("deleteFeedbackSuccess", feedbackId);
      return;
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
    createFeedbackSuccess(state, feedback) {
      state.feedback.unshift(feedback);
    },
    getFeedbackSuccess(state, feedback) {
      state.feedback = feedback;
    },
    deleteFeedbackSuccess(state, feedbackId) {
      state.feedback = state.feedback.filter(fd => fd.id != feedbackId);
    },
    reset(state) {
      state.students = [];
    }
  }
};
