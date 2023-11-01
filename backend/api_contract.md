`#students`

* Student object
```
{
    id: integer
    first_name: string
    middle_name: string
    last_name: string
    residency: string (Enum)
    student_type: string (Enum)
    status: string (Enum)
    admit_type: string (Enum)
    campus_id: integer
    email: string
    phone_number: integer
    citizenship: string
    gender: string
    ethnicity: string
    committee_members: string
    prelim_exam_date: string
    prelim_exam_passed: bool
    profile_picture: string
    first_term: integer (Enum)
}
```

# GET /students
---------------------------------
  Returns all the students in the system
* **Path Params**
  None 
* **Query Params**
  *Optional*
    * admit_type
    * residency
    * student_type
    * prelim_exam_date
    * prelim_exam_passed
    * first_term
    * status
    * campus_id
* **Success Response:**
* **Code: 200**
  **Content:**
  ```
  {
    students: [
                {<student_object>},
                {<student_object>},
                {<student_object>}
              ]
   }
  ```

# GET /students/:id
---------------------------------
  Returns a single student with the id provided if the student exists.
* **Path Params**
  *Required*: `id=[integer]`
* **Query Params** (implement if we have time, think about later)
  * fields
    * name
    * email
    * PID
* **Success Response:**
  * **Code: 200**
  * **Content:**```{ student: <student_object> }```
* **Error Response:**
  * **Code**: 404
  * **Content:** `{ error: "Student does not exist" }` 
---

* Student Advisor Object

```
{
    advisor: <advisor.object>
    advisor_role: string
}
```


# GET /students/:id/advisors
---------------------------------
  Returns all the advisors of the student
* **Path Params**
  *Required:* `id: [integer]` 
* **Query Params**
  *Optional*
    * advisor_role
* **Success Response:**
* **Code: 200**
  **Content:**
  ```
  {
    students: [
                {<student_advisor_object>},
                {<student_advisor_object>},
                {<student_advisor_object>}
              ]
   }
  ```
---

* Visa Object

```
{
    citizenship: string
    visa_name: string
    expiration_date: string
}
```


# GET /students/:id/visa
---------------------------------
  Returns the visa of the student if it exists.
* **Path Params**
  *Required:* `id: [integer]` 
* **Query Params**
None
* **Success Response:**
  * **Code: 200**
  * **Content:** `visa: <visa_object>`
* **Error Response**
  * **Code:** 404
  * **Content:** `{ "error": "Visa information for this student does not exist. This could be due to the student being a U.S. citizen.}`
---

`#advisors`
* Advisor object
```
{
    id: integer
    first_name: integer
    middle_name: string
    last_name: string
    dept_code: integer
}
```
# GET /advisors
---------------------------------
  Returns all the advisors in the system
* **Path Params**
  None 
* **Query Params**
  *Optional*
    * dept_code
* **Success Response:**
* **Code: 200**
  **Content:**
  ```
  {
    students: [
                {<advisor_object>},
                {<advisor_object>},
                {<advisor_object>}
              ]
   }
  ```

  # GET /advisors/:id
---------------------------------
  Returns a single advisor with the id provided if the student exists.
* **Path Params**
  *Required*: `id=[integer]`
* **Query Params** 
None
* **Success Response:**
  * **Code: 200**
  * **Content:**```{ advisor: <advisor_object> }```
* **Error Response:**
  * **Code**: 404
  * **Content:** `{ error: "Advisor does not exist" }` 














