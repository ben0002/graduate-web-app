# FRONTEND README 

## Technology 
Below is a list, a brief explanation of it's uses, and it's documentation link.

### React 
 * React is a JS library for building UIs. Allows you to create reusable UI components that update as data changes.
 * Documentation Link: [https://legacy.reactjs.org/docs](https://react.dev/reference/react)

### Material UI 
 * MUI is a React UI framwork that provides a set of pre-designed customizable UI component. Our front-end uses MUI heavily to create pre-designed UI which is then customized to fit our specifications.
 * Documentation Link: https://mui.com/material-ui/getting-started/

### CSS
 * Cascading Style Sheets is a styling language which will allow for control over the visual appearance of elements.
 * Our project uses both CSS with MUI styling
 * Documentation Link: https://devdocs.io/css/

### Redux 
 * Redux is a predictable state management library for JS applications, normally used with React. In our project, it will help manage the application state in a centralized store located in /graduate_progress_portal/src/assets/redux
* Documentation Link: https://redux.js.org/

### NPM 
 * NPM is a package manager for JS, which will allow for managing, installing, and sharing pakages from the Node.js ecosystem. Used to install dependecies.
 * Documentation Link: https://docs.npmjs.com/

### Node.js
  * JS runtime environemnt that will allow you to execute code outside of the web browser. 
  * Documentation Link: https://nodejs.org/en/docs/

# FrontEnd Structure
Below will be a brief explanation of the directories and what each file is specifically for. **Everything frontend will be located in the src directory in graduate_progress_portal** 

## Advisor 
 * This directory will be where the next capstone team will come in an implement. Read down further for what needs to be implemented. 

## Assets

## Layouts
 * Contains files where any design or component is applied globally
 ### mainLayout.js
   * Global to all users
 ### studentLayout.js
   * Only global to all users that return the 'student' role
     
## Pages
* Contains the files for the pages that currently exist
### /advisor
### /student
#### StudentProfile.js
#### StudentProgress.js 
 ### login.js 
  * React component that will handle user authentication with VT CAS. Uses a useEffect hook to initiate an API request to retrieve current user's information from the CAS server. It will then redirect a user to the CAS login page if they are not logged in, once succesfull it will redirect the user to their default page.

 ### notFound.js 
  * Standard notFound page.

## Shared

## Student
