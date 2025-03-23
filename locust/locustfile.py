from asyncio import events
import uuid
from locust import HttpUser, task, between, events

class TriremeUser(HttpUser):
    wait_time = between(1, 3)  # Users wait 1-3 seconds between tasks
    
    def on_start(self):
        self.project_id = self.create_project()

        if not self.project_id:
            # Fallback to a safe default or disable tasks
            self.project_id = 1  # Or set to None and check in tasks

    @task
    def get_homepage(self):
        self.client.get("/")  # Adjust based on your API routes

    @task
    def get_projects(self):
        self.client.get("/projects") 

    @task
    def create_project(self):
        response = self.client.post("/projects", json={"name": "Test", "description": "test description"})

        try:
            response_data = response.json()  # Ensure it's parsed correctly
            project_id = response_data.get("id")  # Extract ID
            if project_id:
                print(f"Created project with ID: {project_id}")
                return project_id
            else:
                print("No 'id' in response:", response_data)
        except Exception as e:
            print(f"Failed to parse response: {e}")

        return None
        
    @task
    def update_project(self):
        payload = {"description": "Updated description via Locust"}
        self.client.put(f"/projects/{self.project_id}", json=payload)
        
    @task
    def delete_project(self):
        # First, create a throwaway project just for deletion
        payload = {
            "name": f"Test Project {uuid.uuid4().hex[:6]}",
            "description": "This project will be deleted immediately"
        }
        create_response = self.client.post("/projects", json=payload)

        if create_response.status_code == 200:
            project_id = create_response.json()["id"]
            delete_response = self.client.delete(f"/projects/{project_id}")
            if delete_response.status_code == 200:
                print(f"Deleted project ID {project_id}")
            else:
                print(f"Failed to delete project ID {project_id}: {delete_response.status_code}")
        else:
            print(f"Failed to create project for deletion: {create_response.status_code}")

        
    @task
    def create_module(self):
        payload = {
            "project_id": self.project_id,
            "name": f"Module {uuid.uuid4().hex[:4]}",
            "description": "Locust test module"
        }
        self.client.post("/modules", json=payload)

    @task
    def read_modules_by_project(self):
        self.client.get(f"/modules/{self.project_id}")

        
    @task
    def create_suite(self):
        payload = {
            "project_id": self.project_id,
            "name": f"Suite {uuid.uuid4().hex[:4]}",
            "description": "Locust test suite"
        }
        self.client.post("/suites", json=payload)
        
    @task
    def upload_mand_simulation(self):
        with open("/mnt/test_files/capstone.xlsx", "rb") as f:
            files = {
                "file": ("capstone.xlsx", f, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            }
            data = {
                "sheet_name": "Homepage"
            }
            response = self.client.post("/generate-test-cases/", files=files, data=data)

        if response.status_code != 200:
            print("Upload failed:", response.status_code, response.text)
        
    @task
    def upload_SCR_simulation(self):
        with open("/mnt/test_files/capstone_SCR.docx", "rb") as f:
            files = {
                "file": ("capstone_SCR.docx", f, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
            }
            response = self.client.post("/generate-test-cases/", files=files)
            
        if response.status_code != 200:
            print("Upload failed:", response.status_code, response.text)
            
            
    @events.test_stop.add_listener
    def on_test_stop(environment, **kwargs):
        print("Test complete. Cleaning up all test projects named 'Task*'...")

        user = TriremeUser(environment)
        client = user.client

        response = client.get("/projects")
        if response.status_code == 200:
            for project in response.json():
                if project["name"].startswith("Test"):
                    del_response = client.delete(f"/projects/{project['id']}")
                    if del_response.status_code == 200:
                        print(f"Deleted project: {project['name']} (ID: {project['id']})")
                    else:
                        print(f"Failed to delete {project['name']}: {del_response.status_code}")
        else:
            print(f"Failed to list projects: {response.status_code}")

        
    # @task
    # def create_module(self):
    #     self.client.post("/modules", json={"project_id": 1,"name": "Test Module", "description": "test description"})
        
    # @task
    # def get_mod(self):
    #     self.client.get("/project-page/Test/1")


