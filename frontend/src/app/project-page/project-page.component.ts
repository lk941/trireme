import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router } from '@angular/router';
import { NavbarService } from '../services/navbar.service';

@Component({
  selector: 'app-preview',
  standalone: true,
  imports: [FormsModule, HttpClientModule, CommonModule],
  templateUrl: './project-page.component.html',
  styleUrl: './project-page.component.scss'
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
  breadcrumb = { projectName: '', module: '' };
  isEditing: boolean = false;
  description: string = '';

  constructor(private navbarService: NavbarService, private route: ActivatedRoute, private http: HttpClient, private router: Router) {}

  ngOnInit(): void {
    
    this.route.paramMap.subscribe(params => {
      this.projectId = Number(params.get('pid')); 
      console.log(this.projectId);
    });

    this.loadProjectDetails();

    const navState = history.state;

    if (navState) {
      this.navbarService.breadcrumb$.subscribe((breadcrumb) => {
        this.breadcrumb = breadcrumb;
      });
    }

    this.loadModules();
  }

  startEditing(): void {
    this.isEditing = true;
  }

  saveDescription(): void {
    this.isEditing = false;
  }

  loadModules(): void {
    console.log(this.projectId)
    this.http.get<any[]>(`http://localhost:8000/modules/${this.projectId}`).subscribe(data => {
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

  navigateToProject(projectId: number, moduleName: String, projectSpecificId: number): void {
    this.router.navigate(['/preview', this.breadcrumb.projectName , projectId, moduleName, projectSpecificId]);
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
