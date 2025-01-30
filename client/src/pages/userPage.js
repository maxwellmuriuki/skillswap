import React, { useState, useEffect } from 'react';
import axios from 'axios';

const UserPage = () => {
  const [users, setUsers] = useState([]);  // Store the list of users
  const [skills, setSkills] = useState([]); // Store all available skills
  const [selectedUser, setSelectedUser] = useState(null);  // Track which user is selected for adding skills
  const [selectedSkill, setSelectedSkill] = useState('');  // Store selected skill ID
  const [proficiency, setProficiency] = useState('');  // Store proficiency level

  // Fetch users and skills when the component mounts
  useEffect(() => {
    const fetchData = async () => {
      try {
        const usersResponse = await axios.get('http://localhost:5000/users');
        setUsers(usersResponse.data);

        const skillsResponse = await axios.get('http://localhost:5000/skills');
        setSkills(skillsResponse.data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
  }, []);

  // Handle adding a skill
  const handleAddSkill = async () => {
    if (!selectedUser || !selectedSkill || !proficiency) return;

    try {
      const response = await axios.post('http://localhost:5000/skill-user', {
        user_id: selectedUser.id,
        skill_id: selectedSkill,
        proficiency: parseInt(proficiency),
      });

     
      setUsers((prevUsers) =>
        prevUsers.map((user) =>
          user.id === selectedUser.id
            ? {
                ...user,
                skills: [...(Array.isArray(user.skills) ? user.skills : []), response.data],
              }
            : user
        )
      );

      // Reset input fields
      setSelectedSkill('');
      setProficiency('');
    } catch (error) {
      console.error('Error adding skill:', error);
    }
  };

  return (
    <div className="user-page">
      <div className="left-half">
        <h2>All Users</h2>
        <ul>
          {users.map((user) => (
            <li key={user.id}>
              <div>
                <strong>{user.username}</strong> ({user.email})
                <ul>
                  {Array.isArray(user.skills) && user.skills.length > 0 ? (
                    user.skills.map((skill, index) => (
                      <li key={index}>
                        {skill.skill_name} (Proficiency: {skill.proficiency || 'N/A'})
                      </li>
                    ))
                  ) : (
                    <li>No skills added</li>
                  )}
                </ul>
                <button onClick={() => setSelectedUser(user)}>Edit Skills</button>
              </div>
            </li>
          ))}
        </ul>
      </div>

      <div className="right-half">
        {selectedUser ? (
          <>
            <h2>Edit Skills for: {selectedUser.username}</h2>

            <div>
              <label>Skill</label>
              <select value={selectedSkill} onChange={(e) => setSelectedSkill(e.target.value)}>
                <option value="">Select a Skill</option>
                {skills.map((skill) => (
                  <option key={skill.id} value={skill.id}>
                    {skill.skill_name}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label>Proficiency (1-5)</label>
              <input
                type="number"
                value={proficiency}
                onChange={(e) => setProficiency(e.target.value)}
                placeholder="Enter proficiency level"
                min="1"
                max="5"
              />
            </div>

            <button onClick={handleAddSkill}>Add Skill</button>
          </>
        ) : (
          <p>Select a user to add skills.</p>
        )}
      </div>
    </div>
  );
};

export default UserPage;
