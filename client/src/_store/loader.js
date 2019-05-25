export const loader = {
  namespaced: true,
  state: {
    asyncCalls: 0
  },
  mutations: {
    increment(state) {
      state.asyncCalls += 1;
    },
    decrement(state) {
      state.asyncCalls -= 1;
    }
  }
};
