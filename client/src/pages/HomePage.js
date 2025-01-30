import React, { useState, useEffect } from 'react';
import axios from 'axios';

const HomePage = () => {
  const [skills, setSkills] = useState([]); // Store all available skills
  const [newSkill, setNewSkill] = useState({ skill_name: '', description: '' }); // Store new skill input

  // Fetch skills when the component mounts
  useEffect(() => {
    const fetchSkills = async () => {
      try {
        const response = await axios.get('http://localhost:5000/skills');
        setSkills(response.data);
      } catch (error) {
        console.error('Error fetching skills:', error);
      }
    };

    fetchSkills();
  }, []);

  // Handle skill submission
  const handleAddSkill = async (e) => {
    e.preventDefault();

    if (!newSkill.skill_name) return; // Ensure skill name is entered

    try {
      const response = await axios.post('http://localhost:5000/skills', newSkill);

      // Update skill list dynamically
      setSkills([...skills, response.data]);

      // Clear form
      setNewSkill({ skill_name: '', description: '' });
    } catch (error) {
      console.error('Error adding skill:', error);
    }
  };

  return (
    <div className="home-page">
      <h2>Add a New Skill</h2>
      <form onSubmit={handleAddSkill}>
        <div>
          <label>Skill Name:</label>
          <input
            type="text"
            value={newSkill.skill_name}
            onChange={(e) => setNewSkill({ ...newSkill, skill_name: e.target.value })}
            placeholder="Enter skill name"
          />
        </div>
        <div>
          <label>Description:</label>
          <input
            type="text"
            value={newSkill.description}
            onChange={(e) => setNewSkill({ ...newSkill, description: e.target.value })}
            placeholder="Enter skill description"
          />
        </div>
        <button type="submit">Add Skill</button>
      </form>

      <h2>Available Skills</h2>
      <ul>
        {skills.map((skill) => (
          <li key={skill.id}>
            <strong>{skill.skill_name}</strong> - {skill.description || 'No description'}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default HomePage;
