## Capstone Project: AI-Automated E2E Testing Application

This project focuses on automating Product/User Acceptance Testing (not to be confused with automated unit/functional tests).
It caters to the following stages by design:
1. Test Case Writing (In Progress)
   - AI-generated content based on user uploaded software documentation
2. Test Case Execution (Not Implemented)
   - Integration with third-party execution apps
3. Test Case Reporting (Not Implemented)
   - Integration with third-party management tools, e.g Azure DevOps

## System Prerequisites
- Docker
- Node.js
- Git Bash (Optional)

## Setup and Run Application (Windows)

- in cmd, run npm install 

With Git Bash:
- Run ./start.sh to start application
- ./stop.sh to stop application

Without Git Bash (terminal):
- docker-compose up to start application
- docker-compose down to stop application

Access the application frontend at: http://localhost:4200/
Access application backend: http://localhost:8000/
