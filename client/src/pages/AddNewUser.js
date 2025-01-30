import React, { useState, useEffect } from 'react';
import { Formik, Field, Form, ErrorMessage } from 'formik';
import axios from 'axios';
import '../App.css';  // Ensure correct path to your CSS file

const AddNewUser = () => {
  const [userDetails, setUserDetails] = useState(null); // Store user data after registration or login
  const [error, setError] = useState(null);
  const [isEditing, setIsEditing] = useState(false); // Track if we're editing the user

  // Handle form submission for both new user registration and updating user profile
  const handleSubmit = async (values) => {
    try {
      let response;

      // If we are editing an existing user, send a PUT request
      if (isEditing && userDetails) {
        response = await axios.put(`http://localhost:5000/users/${userDetails.id}`, values);
      } else {
        // Otherwise, send a POST request to create a new user
        response = await axios.post('http://localhost:5000/users', values);
      }

      // Set the user details after successful registration or update
      setUserDetails(response.data);
      setIsEditing(false); // Disable editing mode after successful operation
    } catch (err) {
      setError(err.response ? err.response.data.message : 'Error occurred');
    }
  };

  // Validation schema for Formik
  const validate = (values) => {
    const errors = {};
    if (!values.username) {
      errors.username = 'Required';
    }
    if (!values.email) {
      errors.email = 'Required';
    } else if (!/\S+@\S+\.\S+/.test(values.email)) {
      errors.email = 'Invalid email address';
    }
    if (!values.password) {
      errors.password = 'Required';
    }
    return errors;
  };

  // Handle delete user action
  const handleDelete = async () => {
    try {
      await axios.delete(`http://localhost:5000/users/${userDetails.id}`);
      setUserDetails(null); // Clear the user details from the state
      setIsEditing(false); // Reset editing state
    } catch (err) {
      setError(err.response ? err.response.data.message : 'Error occurred during deletion');
    }
  };

  useEffect(() => {
    if (userDetails) {
      // If user details are available, pre-populate the form fields
    }
  }, [userDetails]);

  return (
    <div className="add-user-container">
      <h2>{isEditing ? 'Edit Profile' : 'Add New User'}</h2>
      {error && <div className="error-message">{error}</div>}

      <Formik
        initialValues={{
          username: userDetails ? userDetails.username : '', // Default to existing data if editing
          email: userDetails ? userDetails.email : '',         // Default to existing data if editing
          password: '',                                        // Empty password for new users
        }}
        enableReinitialize={true}  // Ensure the form gets reinitialized when userDetails change
        validate={validate}
        onSubmit={handleSubmit}
      >
        <Form className="add-user-form">
          <div className="form-field">
            <label htmlFor="username">Username</label>
            <Field type="text" id="username" name="username" />
            <ErrorMessage name="username" component="div" className="error-text" />
          </div>
          
          <div className="form-field">
            <label htmlFor="email">Email</label>
            <Field type="email" id="email" name="email" />
            <ErrorMessage name="email" component="div" className="error-text" />
          </div>

          <div className="form-field">
            <label htmlFor="password">Password</label>
            <Field type="password" id="password" name="password" />
            <ErrorMessage name="password" component="div" className="error-text" />
          </div>

          <button type="submit" className="submit-btn">
            {isEditing ? 'Update Profile' : 'Add User'}
          </button>
        </Form>
      </Formik>

      {/* Displaying user profile details after adding a user */}
      {userDetails && !isEditing && (
        <div className="user-details">
          <h3>User Details</h3>
          <p><strong>Username:</strong> {userDetails.username}</p>
          <p><strong>Email:</strong> {userDetails.email}</p>
          <button onClick={() => setIsEditing(true)}>Edit Profile</button>
          
          <button onClick={handleDelete} className="delete-btn">
            Delete Profile
          </button>
        </div>
      )}
    </div>
  );
};

export default AddNewUser;
