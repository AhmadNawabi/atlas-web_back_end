const fs = require('fs');

function countStudents(path) {
    try {
        const data = fs.readFileSync(path, 'utf8');
        const lines = data.split('\n').filter(line => line.trim() !== '' && !line.startsWith('firstname'));
        
        console.log(`Number of students: ${lines.length}`);
        
        const fields = {};
        
        lines.forEach(line => {
            const [firstname, field] = line.split(',').map(item => item.trim());
            if (firstname && field) {
                if (!fields[field]) {
                    fields[field] = [];
                }
                fields[field].push(firstname);
            }
        });
        
        for (const [field, students] of Object.entries(fields)) {
            console.log(`Number of students in ${field}: ${students.length}. List: ${students.join(', ')}`);
        }
    } catch (error) {
        throw new Error('Cannot load the database');
    }
}

module.exports = countStudents;
