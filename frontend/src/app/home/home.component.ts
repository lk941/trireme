import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css'],
  standalone: true,
  imports: [FormsModule, HttpClientModule, CommonModule],
})
export class HomeComponent {

  isProcessingAnonymize = false;
  isProcessingDeAnonymize = false;
  isProcessingTestCase = false;

  anonymizeFile: File | null = null;
  deanonymizeFile: File | null = null;
  testCaseFile: File | null = null;
  downloadLinkAnonymize: string | null = null;
  downloadLinkDeAnonymize: string | null = null;
  downloadLinkTestCase: string | null = null;

  anonymizeKeywords: string = 'DPP2, PSAC, Terminal, JIT'; // To store keywords entered by the user


  message: string = '';
  responseMessage: string | null = null;

  constructor(private http: HttpClient) {}

  onTestConnection(event: Event): void {
    event.preventDefault();
    this.http.post('http://127.0.0.1:8000/test-connection', { message: this.message })
      .subscribe(
        response => console.log(response),
        error => console.error(error)
      );
  }

  onAnonymizeFileChange(event: Event): void {
    const target = event.target as HTMLInputElement;
    this.anonymizeFile = target.files?.[0] || null;
  }
  
  onAnonymizeSubmit(event: Event): void {
    event.preventDefault();
    if (!this.anonymizeFile || !this.anonymizeKeywords) return;
  
    this.isProcessingAnonymize = true;
    this.downloadLinkAnonymize = null;
  
    const formData = new FormData();
    formData.append('file', this.anonymizeFile);
    formData.append('keywords', this.anonymizeKeywords);
  
    this.http.post('http://127.0.0.1:8000/anonymize/', formData, { responseType: 'blob' })
      .subscribe(
        response => {
          this.isProcessingAnonymize = false;
  
          // Create a Blob and specify the type
          const blob = new Blob([response], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
          
          // Create a download link with a specific filename
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = 'anonymized.xlsx'; // Set the filename here
          a.click();
          
          // Release the object URL after the download
          window.URL.revokeObjectURL(url);
  
          // Optionally update the download link for the UI
          this.downloadLinkAnonymize = url;
        },
        error => {
          this.isProcessingAnonymize = false;
          console.error(error);
        }
      );
  }
  

  onDeAnonymizeFileChange(event: Event): void {
    const target = event.target as HTMLInputElement;
    this.deanonymizeFile = target.files?.[0] || null;
  }

  onDeAnonymizeSubmit(event: Event): void {
    event.preventDefault();
    if (!this.deanonymizeFile) return;
  
    this.isProcessingDeAnonymize = true;
    this.downloadLinkDeAnonymize = null;
  
    const formData = new FormData();
    formData.append('file', this.deanonymizeFile);
  
    this.http.post('http://127.0.0.1:8000/deanonymize/', formData, { responseType: 'blob' })
      .subscribe(
        response => {
          this.isProcessingDeAnonymize = false;
  
          // Create a Blob with the correct MIME type
          const blob = new Blob([response], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
          
          // Create a download link and specify the filename
          const url = window.URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = 'deanonymized.xlsx'; // Specify the filename
          a.click();
  
          // Release the object URL after the download
          window.URL.revokeObjectURL(url);
  
          // Optionally update the download link for the UI
          this.downloadLinkDeAnonymize = url;
        },
        error => {
          this.isProcessingDeAnonymize = false;
          console.error(error);
        }
      );
  }
  

  onTestCaseFileChange(event: Event): void {
    const target = event.target as HTMLInputElement;
    this.testCaseFile = target.files?.[0] || null;
  }

  onTestCaseSubmit(event: Event): void {
    event.preventDefault();
    if (!this.testCaseFile) return;

    this.isProcessingTestCase = true;
    this.downloadLinkTestCase = null;

    const formData = new FormData();
    formData.append('file', this.testCaseFile);

    this.http.post('http://127.0.0.1:8000/upload/', formData, { responseType: 'blob' })
      .subscribe(
        response => {
          this.isProcessingTestCase = false;
          const blob = new Blob([response], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
          const url = window.URL.createObjectURL(blob);
          this.downloadLinkTestCase = url;
        },
        error => {
          this.isProcessingTestCase = false;
          console.error(error);
        }
      );
  }
}