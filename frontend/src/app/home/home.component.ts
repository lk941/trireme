import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { AppModule } from '../app.module';


@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
  standalone: true,
  imports: [FormsModule, HttpClientModule, CommonModule, AppModule],
})
export class HomeComponent implements OnInit {

  projects: any[] = [];
  newProjectName: string = '';
  isModalOpen: boolean = false;

  constructor(private http: HttpClient, private router: Router) {}

  ngOnInit(): void {
    this.loadProjects();
  }

  loadProjects(): void {
    this.http.get<any[]>('http://localhost:8000/projects').subscribe(data => {
      this.projects = data;
    });
  }

  openModal(): void {
    this.isModalOpen = true;
  }

  closeModal(): void {
    this.isModalOpen = false;
  }

  createProject(): void {
    if (this.newProjectName.trim()) {
      this.http.post('http://localhost:8000/projects', { name: this.newProjectName, description: '' })
        .subscribe(() => {
          this.loadProjects();
          this.closeModal();
          this.newProjectName = '';
        });
    }
  }

  navigateToProject(projectName: String, projectId: number): void {
    this.router.navigate(['/project-page', projectName, projectId]);
  }

  deleteProject(projectId: number): void {
    this.http.delete(`http://localhost:8000/projects/${projectId}`).subscribe({
      next: (response: any) => {
        console.log(response.message); // Log the success message
        // Optionally update local state if needed
        this.projects = this.projects.filter(p => p.id !== projectId);
        console.log('Updated projects:', this.projects);
      },
      error: (error) => {
        console.error('Error deleting project:', error);
      }
    });
  }
  
}