import { createStore } from 'redux';

// Define an initial state
const initialState = {
    user: undefined,
    student: {
        info: {},
        advisors: [],
        programs: [],
        campus: {},
        pos: {},
        tasks: [],
        milestones: [],
        requirements: [],
        funding: [],
        employment: [],
        courses: [],
        labs: [],
        messages: []
    }
};

// Create a reducer
const studentReducer = (state = initialState, action) => {
  // Handle actions here - example
  switch (action.type) {
    // Add case for each action type
    case 'pop_user':
      if(action.payload.type == 'student'){
        return {...state, 
          user: action.payload.type,
          student: {...state.student, 
            info: action.payload.data.student, 
            advisors: action.payload.data.advisors, 
            programs: action.payload.data.programs, 
            campus: action.payload.data.campus, 
            pos: action.payload.data.POS_info
          }
        }
      }
      else{
        return {...state}
      }
    case 'pop_stu_prog':
      return {...state, 
        student: { ...state.student,
          tasks: action.payload.events, 
          milestones: action.payload.milestones, 
          requirements: action.payload.requirements, 
          funding: action.payload.funding, 
          employment: action.payload.employment, 
          courses: action.payload.courses
        }
      }
    case 'pop_stu_profile':
      return {...state,
        student: { ...state.student, 
          labs: action.payload.labs, 
          messages: action.payload.messages
        }
      }
    case 'add_task':
      return {...state,
        student: { ...state.student,
          tasks: [...state.student.tasks, action.payload]
        }
      }
    case 'update_task':
        return {...state,
            student: { ...state.student,
                tasks: state.student.tasks.map(task => task.id == action.payload.id ? action.payload.data : task )
            }
        }
    case 'delete_task':
        return {...state,
            student: { ...state.student,
                tasks: state.student.tasks.filter(task => task.id != action.payload.id)
            }
        }
    case 'add_funding':
        return {...state,
            student: { ...state.student,
                funding: [...state.student.funding, action.payload]
            }
        }
    case 'update_funding':
        return {...state,
            student: { ...state.student,
                funding: state.student.funding.map(fund => fund.id == action.payload.id ? action.payload.data : fund )
            }
        }
    case 'delete_funding':
        return {...state,
            student: { ...state.student,
                funding: state.student.funding.filter(fund => fund.id != action.payload.id)
            }
        }
    case 'add_employment':
        return {...state,
            student: { ...state.student,
                employment: [...state.student.employment, action.payload]
            }
        }
    case 'update_employment':
        return {...state,
            student: { ...state.student,
                employment: state.student.employment.map(empl => empl.id == action.payload.id ? action.payload.data : empl )
            }
        }
    case 'delete_employment':
        return {...state,
            student: { ...state.student,
                employment: state.student.employment.filter(empl => empl.id != action.payload.id)
            }
        }
    case 'add_course':
        return {...state,
            student: { ...state.student,
                courses: [...state.student.courses, action.payload]
        }
    }
    case 'delete_course':
        return {...state,
            student: { ...state.student,
                courses: state.student.courses.filter(course => course.id != action.payload.id)
            }
        }
    case 'add_lab':
        return {...state,
            student: { ...state.student,
                labs: [...state.student.labs, action.payload]
        }
    }
    case 'delete_lab':
        return {...state,
            student: { ...state.student,
                labs: state.student.labs.filter(lab => lab.id != action.payload.id)
            }
        }
    default:
      return state;
  }
};

// Create the store
const store = createStore(studentReducer);

export default store;