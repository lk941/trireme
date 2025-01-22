import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';


@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css'],
  standalone: true, 
  imports: [FormsModule, HttpClientModule],
})
export class HomeComponent {

  anonymizeFile: File | null = null;
  testCaseFile: File | null = null;
  message: string = '';
  responseMessage: string | null = null;

  constructor(private http: HttpClient) {}

  onTestConnection(event: Event) {
    event.preventDefault();
    console.log("triggered");

    const payload = { message: this.message };

    // Make the POST request to the backend
    this.http.post('http://127.0.0.1:8000/test-connection', payload).subscribe(
      (response: any) => {
        this.responseMessage = response.message;
      },
      (error) => {
        console.error('Error:', error);
        this.responseMessage = 'Failed to connect to the backend.';
      }
    );
  }

  // Handle file selection for anonymization
  onAnonymizeFileChange(event: any): void {
    this.anonymizeFile = event.target.files[0];
  }

  // Handle anonymization form submission
  async onAnonymizeSubmit(event: Event): Promise<void> {
    event.preventDefault();
    console.log("submit triggered")

    if (!this.anonymizeFile) {
      alert('Please select a file for anonymization.');
      return;
    }

    const formData = new FormData();
    formData.append('file', this.anonymizeFile);

    const loading = document.getElementById('anonymizeLoading');
    const preview = document.getElementById('anonymizePreview');
    const contentPreview = document.getElementById('anonymizedContent');
    const downloadLink = document.getElementById('anonymizeDownloadLink');
    const downloadUrl = document.getElementById('anonymizeDownloadUrl') as HTMLAnchorElement;

    loading!.style.display = 'block';
    preview!.style.display = 'none';
    downloadLink!.style.display = 'none';

    try {
      const response = await fetch('http://127.0.0.1:8000/anonymize/', {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        throw new Error('Anonymization failed. Please try again.');
      }

      const result = await response.json();
      loading!.style.display = 'none';

      // Display preview
      contentPreview!.textContent = result.preview;
      preview!.style.display = 'block';

      // Create a downloadable file link
      const blob = new Blob([result.file], { type: result.fileType });
      const url = URL.createObjectURL(blob);
      downloadUrl.href = url;
      downloadUrl.download = 'anonymized-file';
      downloadLink!.style.display = 'block';
    } catch (error) {
      loading!.style.display = 'none';
  
      let errorMessage = 'An unexpected error occurred.';
  
      // Check if the error is an instance of Error
      if (error instanceof Error) {
          errorMessage = error.message;
      }
  
      alert(errorMessage);
    }
  }

  // Handle file selection for test case generation
  onTestCaseFileChange(event: any): void {
    this.testCaseFile = event.target.files[0];
  }

  // Handle test case generation form submission
  async onTestCaseSubmit(event: Event): Promise<void> {
    event.preventDefault();

    if (!this.testCaseFile) {
      alert('Please select a file for test case generation.');
      return;
    }

    const formData = new FormData();
    formData.append('file', this.testCaseFile);

    const loading = document.getElementById('testCaseLoading');
    const downloadLink = document.getElementById('testCaseDownloadLink');
    const downloadUrl = document.getElementById('testCaseDownloadUrl') as HTMLAnchorElement;

    loading!.style.display = 'block';
    downloadLink!.style.display = 'none';

    try {
      const response = await fetch('http://127.0.0.1:8000/upload/', {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        throw new Error('Test case generation failed. Please try again.');
      }

      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      downloadUrl.href = url;
      downloadUrl.download = 'test-scripts.xlsx';

      loading!.style.display = 'none';
      downloadLink!.style.display = 'block';
    } catch (error) {
      loading!.style.display = 'none';
  
      let errorMessage = 'An unexpected error occurred.';
  
      // Check if the error is an instance of Error
      if (error instanceof Error) {
          errorMessage = error.message;
      }
  
      alert(errorMessage);
  }
  }
}
