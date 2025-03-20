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
  templateUrl: './preview.component.html',
  styleUrl: './preview.component.scss'
})
export class PreviewComponent implements OnInit{
  testCases: any[] = []; // Stores the generated test cases
  editedTestCases: any[] = [
    {
      Test_Case_ID: '',
      Test_Case_Name: '',
      Test_Case_Type: '',
      Pre_Condition: '',
      Actor_s: '',
      Test_Data: '',
      Step_Description: '',
      Expected_Result: ''
    }
  ];
  file: File | null = null; // Stores the uploaded file
  isProcessing: boolean = false; // Tracks loading state
  isDataLoaded: boolean = false; // Tracks if data is loaded for table display
  projectId: number | null = null;
  moduleId: number | null = null;
  breadcrumb = { projectName: '', module: '' };
  moduleTC: String | null = null; // Returns either name of file or no existing module test cases

  constructor(private navbarService: NavbarService, private route: ActivatedRoute, private http: HttpClient, private router: Router) {}

  ngOnInit() {
    this.projectId = Number(this.route.snapshot.paramMap.get('pid'));
    this.moduleId = Number(this.route.snapshot.paramMap.get('mid'));

    this.loadExistingTestCases()

    const navState = history.state;

    if (navState) {
      this.navbarService.breadcrumb$.subscribe((breadcrumb) => {
        this.breadcrumb = breadcrumb;
      });

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

  loadExistingTestCases(): void {
    this.http.get<any>(`http://localhost:8000/modules/${this.projectId}/${this.moduleId}`).subscribe(data => {
      console.log(data.scr_update)
      this.testCases = JSON.parse(data.scr_update) ?? []; 
      this.editedTestCases = [...this.testCases];
      console.log(this.editedTestCases);
    });
  }

  navigateToSetup(projectId: number) {
    this.router.navigate(['/automation-setup', projectId], {
      state: { testData: this.editedTestCases, uploadedFile: this.file }
    });
  }

  navigateToMandatory() {
    this.router.navigate(['/module-mandatory', this.breadcrumb.projectName , this.projectId, this.breadcrumb.module, this.moduleId]);
  }


  // Handles file selection
  onFileChange(event: Event): void {
    const target = event.target as HTMLInputElement;
    this.file = target.files?.[0] || null;
  }

  addRow(): void {
    const newTestCase = {
      Test_Case_ID: '',
      Test_Case_Name: '',
      Test_Case_Type: '',
      Pre_Condition: '',
      Actor_s: '',
      Test_Data: '',
      Step_Description: '',
      Expected_Result: ''
    };
    this.editedTestCases.push(newTestCase);
  }
  
  deleteRow(index: number): void {
    this.editedTestCases.splice(index, 1);
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

  updateTestCases(): void {
    const updatedData = { script_content: this.editedTestCases };

    this.http.put(`http://localhost:8000/modules/${this.projectId}/${this.moduleId}/update_ttc`, updatedData)
      .subscribe(
        response => {
          console.log("Test cases updated successfully!", response);
          alert("Test cases updated successfully!");
        },
        error => {
          console.error("Error updating module test cases:", error);
          alert("Failed to update module test cases.");
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
