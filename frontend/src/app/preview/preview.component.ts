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
  templateUrl: './preview.component.html',
  styleUrl: './preview.component.css'
})
export class PreviewComponent implements OnInit{
  testCases: any[] = []; // Stores the generated test cases
  editedTestCases: any[] = []; // Stores the edited test cases
  file: File | null = null; // Stores the uploaded file
  isProcessing: boolean = false; // Tracks loading state
  isDataLoaded: boolean = false; // Tracks if data is loaded for table display
  projectId: number | null = null;
  projectName: string = '';

  constructor(private route: ActivatedRoute, private http: HttpClient, private router: Router) {}

  navigateToSetup(projectId: number) {
    this.router.navigate(['/automation-setup', projectId], {
      state: { testData: this.editedTestCases, uploadedFile: this.file }
    });
  }

  ngOnInit() {
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

  loadProjectDetails(): void {
    this.http.get<any>(`http://localhost:8000/projects/${this.projectId}`).subscribe(project => {
      this.projectName = project.name;
    });
  }

  // Handles file selection
  onFileChange(event: Event): void {
    const target = event.target as HTMLInputElement;
    this.file = target.files?.[0] || null;
  }

  // Submits the file to generate test cases
  onSubmit(event: Event): void {
    event.preventDefault();
    if (!this.file) return;

    this.isProcessing = true;

    const formData = new FormData();
    formData.append('file', this.file);

    this.http.post('http://127.0.0.1:8000/generate-test-cases', formData)
      .subscribe(
        (response: any) => {
          this.isProcessing = false;
          this.testCases = response.test_cases;
          this.editedTestCases = [...this.testCases]; // Copy for editing
          this.isDataLoaded = true;  // Set flag to show table after generation
        },
        (error) => {
          this.isProcessing = false;
          console.error('Error generating test cases:', error);
        }
      );
  }

  onDownload(): void {
    this.isProcessing = true;

    const payload = { test_cases: this.editedTestCases };

    console.log('Payload being sent:', JSON.stringify(payload, null, 2));  // Debug payload structure

    this.http.post('http://127.0.0.1:8000/generate-excel', payload, { responseType: 'blob' })
      .subscribe(
        (response: Blob) => {
          this.isProcessing = false;
          const blob = new Blob([response], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = 'test-scripts.xlsx';
          a.click();
          window.URL.revokeObjectURL(url);
        },
        (error) => {
          this.isProcessing = false;
          console.error('Error generating Excel file:', error);
          console.log('Payload causing error:', payload);  // Log payload causing issue
        }
      );
  }
}
