import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-preview',
  standalone: true,
  imports: [FormsModule, HttpClientModule, CommonModule],
  templateUrl: './project-page.component.html',
  styleUrl: './project-page.component.css'
})
export class ProjectPageComponent implements OnInit{
  testCases: any[] = []; // Stores the generated test cases
  editedTestCases: any[] = []; // Stores the edited test cases
  file: File | null = null; // Stores the uploaded file
  isProcessing: boolean = false; // Tracks loading state
  isDataLoaded: boolean = false; // Tracks if data is loaded for table display
  projectId: number | null = null;
  projectName: string = '';
  modules: any[] = [];
  newModuleName: string = '';
  isModalOpen: boolean = false;
  isModalMandOpen: boolean = false;

  constructor(private route: ActivatedRoute, private http: HttpClient, private router: Router) {}

  ngOnInit(): void {
    this.loadModules();
    this.projectId = Number(this.route.snapshot.paramMap.get('id'));
    this.loadProjectDetails();

    const navState = history.state;

    if (navState) {
      if (navState.editedTestCases && navState.editedTestCases.length > 0) {
        this.editedTestCases = navState.editedTestCases;
        this.isDataLoaded = true;  // Set flag to show table
      }
      if (navState.file) {
        this.file = navState.file;
      } else if (navState.uploadedFile) {
        this.file = navState.uploadedFile;
      }
    }
  }

  loadModules(): void {
    this.http.get<any[]>('http://localhost:8000/modules').subscribe(data => {
      this.modules = data;
    });
  }

  openModal(): void {
    this.isModalOpen = true;
  }

  closeModal(): void {
    this.isModalOpen = false;
  }

  openMandModal(): void {
    this.isModalMandOpen = true;
  }

  closeMandModal(): void {
    this.isModalMandOpen = false;
  }

  createModule(): void {
    if (this.newModuleName.trim()) {
      this.http.post('http://localhost:8000/modules', { project_id: this.projectId, name: this.newModuleName, description: '' })
        .subscribe(() => {
          this.loadModules();
          this.closeModal();
          this.newModuleName = '';
        });
    }
  }

  navigateToProject(projectId: number, projectSpecificId: number): void {
    this.router.navigate(['/preview', projectId, projectSpecificId]);
  }

  navigateToSetup(projectId: number) {
    this.router.navigate(['/automation-setup', projectId], {
      state: { testData: this.editedTestCases, uploadedFile: this.file }
    });
  }


  loadProjectDetails(): void {
    this.http.get<any>(`http://localhost:8000/projects/${this.projectId}`).subscribe(project => {
      this.projectName = project.name;
    });
  }

}
