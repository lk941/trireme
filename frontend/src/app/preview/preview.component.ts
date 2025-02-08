import { Component } from '@angular/core';
import { ApiService } from '../api.service';
import { HttpClient } from '@angular/common/http';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';

@Component({
  selector: 'app-preview',
  standalone: true,
  imports: [FormsModule, HttpClientModule, CommonModule],
  templateUrl: './preview.component.html',
  styleUrl: './preview.component.css'
})
export class PreviewComponent {
  testCases: any[] = []; // Stores the generated test cases
  editedTestCases: any[] = []; // Stores the edited test cases
  file: File | null = null; // Stores the uploaded file
  isProcessing: boolean = false; // Tracks loading state

  constructor(private http: HttpClient, private router: Router) {}

  navigateToSetup() {
    this.router.navigate(['/automation-setup'], {
      state: { testData: this.editedTestCases, uploadedFile: this.file }
    });
  }

  ngOnInit() {
    const navState = history.state;

    if (navState && navState.editedTestCases && navState.file) {
      this.editedTestCases = navState.editedTestCases;
      this.file = navState.file;
    }
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
        },
        (error) => {
          this.isProcessing = false;
          console.error('Error generating test cases:', error);
        }
      );
  }

  // // Handles editing of a test case
  // onEdit(testCase: any, index: number): void {
  //   this.editedTestCases[index] = testCase;
  // }


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
