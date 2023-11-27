import { createStore } from 'redux';

// Define an initial state
const initialState = {
    user: undefined
};

// Create a reducer
const studentReducer = (state = initialState, action) => {
  // Handle actions here - example
  switch (action.type) {
    // Add case for each action type
    case 'populate_user':
      return {...state, user: action.payload}
    default:
      return state;
  }
};

// Create the store
const store = createStore(studentReducer);

export default store;