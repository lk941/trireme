import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
  standalone: true,
  imports: [FormsModule, HttpClientModule, CommonModule],
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
}