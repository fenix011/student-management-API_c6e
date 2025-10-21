// Functional programming approach with minimal state
const API_BASE = 'http://localhost:5000/api';

// Pure functions for API calls
const api = {
    async get(endpoint) {
        const response = await fetch(`${API_BASE}${endpoint}`);
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        return response.json();
    },

    async post(endpoint, data) {
        const response = await fetch(`${API_BASE}${endpoint}`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        return response.json();
    },

    async put(endpoint, data) {
        const response = await fetch(`${API_BASE}${endpoint}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        return response.json();
    },

    async delete(endpoint) {
        const response = await fetch(`${API_BASE}${endpoint}`, {
            method: 'DELETE'
        });
        if (!response.ok) throw new Error(`HTTP ${response.status}`);
        return response.json();
    }
};

// Student App Module (Revealing Module Pattern)
const StudentApp = (function() {

    // Private functions
    const renderStudent = (student) => `
        <div class="student-card">
            <h3>${student.name}</h3>
            <p>Email: ${student.email}</p>
            <p>Grade: <span class="grade ${getGradeClass(student.grade)}">${student.grade}</span></p>
            <div class="actions">
                <button onclick="StudentApp.editStudent(${student.id})">Edit</button>
                <button onclick="StudentApp.deleteStudent(${student.id})" class="danger">Delete</button>
            </div>
        </div>
    `;

    const getGradeClass = (grade) => {
        if (grade >= 90) return 'excellent';
        if (grade >= 80) return 'good';
        if (grade >= 70) return 'average';
        return 'poor';
    };

    const renderStatistics = (stats) => `
        <div class="stats-grid">
            <div class="stat-card">
                <h3>Total Students</h3>
                <p class="stat-value">${stats.total_students}</p>
            </div>
            <div class="stat-card">
                <h3>Average Grade</h3>
                <p class="stat-value">${stats.average_grade?.toFixed(1) || 'N/A'}</p>
            </div>
            <div class="stat-card">
                <h3>Highest Grade</h3>
                <p class="stat-value">${stats.highest_grade || 'N/A'}</p>
            </div>
            <div class="stat-card">
                <h3>Lowest Grade</h3>
                <p class="stat-value">${stats.lowest_grade || 'N/A'}</p>
            </div>
            <div class="stat-card">
                <h3>Grade Distribution</h3>
                <ul>
                    <li>A (90-100): ${stats.a_students}</li>
                    <li>B (80-89): ${stats.b_students}</li>
                    <li>C (70-79): ${stats.c_students}</li>
                    <li>Below 70: ${stats.failing_students}</li>
                </ul>
            </div>
        </div>
    `;

    const showError = (message) => {
        alert(`Error: ${message}`);
    };

    // Public API
    return {
        async loadStudents() {
            try {
                const students = await api.get('/students');
                const container = document.getElementById('student-list');

                if (students.length === 0) {
                    container.innerHTML = '<p>No students found</p>';
                } else {
                    container.innerHTML = students.map(renderStudent).join('');
                }

                // Also load statistics
                this.loadStatistics();
            } catch (error) {
                showError('Failed to load students');
                console.error(error);
            }
        },

        async loadStatistics() {
            try {
                const stats = await api.get('/statistics');
                document.getElementById('stats-container').innerHTML = renderStatistics(stats);
            } catch (error) {
                console.error('Failed to load statistics:', error);
            }
        },

        async filterByGrade(minGrade) {
            try {
                const endpoint = minGrade ? `/students?min_grade=${minGrade}` : '/students';
                const students = await api.get(endpoint);
                const container = document.getElementById('student-list');

                if (students.length === 0) {
                    container.innerHTML = '<p>No students found with this filter</p>';
                } else {
                    container.innerHTML = students.map(renderStudent).join('');
                }
            } catch (error) {
                showError('Failed to filter students');
            }
        },

        showAddForm() {
            document.getElementById('form-title').textContent = 'Add Student';
            document.getElementById('studentId').value = '';
            document.getElementById('studentName').value = '';
            document.getElementById('studentEmail').value = '';
            document.getElementById('studentGrade').value = '';
            document.getElementById('student-form').classList.remove('hidden');
        },

        async editStudent(id) {
            try {
                const student = await api.get(`/students/${id}`);
                document.getElementById('form-title').textContent = 'Edit Student';
                document.getElementById('studentId').value = student.id;
                document.getElementById('studentName').value = student.name;
                document.getElementById('studentEmail').value = student.email;
                document.getElementById('studentGrade').value = student.grade;
                document.getElementById('student-form').classList.remove('hidden');
            } catch (error) {
                showError('Failed to load student data');
            }
        },

        hideForm() {
            document.getElementById('student-form').classList.add('hidden');
        },

        async saveStudent(event) {
            event.preventDefault();

            const id = document.getElementById('studentId').value;
            const data = {
                name: document.getElementById('studentName').value,
                email: document.getElementById('studentEmail').value,
                grade: parseInt(document.getElementById('studentGrade').value)
            };

            try {
                if (id) {
                    await api.put(`/students/${id}`, data);
                } else {
                    await api.post('/students', data);
                }

                this.hideForm();
                this.loadStudents();
            } catch (error) {
                showError('Failed to save student');
            }
        },

        async deleteStudent(id) {
            if (!confirm('Are you sure you want to delete this student?')) {
                return;
            }

            try {
                await api.delete(`/students/${id}`);
                this.loadStudents();
            } catch (error) {
                showError('Failed to delete student');
            }
        }
    };
})();

// Initialize on page load
document.addEventListener('DOMContentLoaded', () => {
    StudentApp.loadStudents();
});
