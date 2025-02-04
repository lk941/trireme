import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ApiService {
  private apiUrl = 'http://127.0.0.1:8000';

  constructor(private http: HttpClient) {}

  getItems() {
    return this.http.get(`${this.apiUrl}/items`);
  }

  // // Sends the file to the backend to generate test cases
  // generateTestCases(file: File): Observable<any> {
  //   const formData = new FormData();
  //   formData.append('file', file);
  //   return this.http.post(`${this.apiUrl}/generate-test-cases`, formData);
  // }

  // // Sends the edited test cases to the backend to generate an Excel file
  // generateExcel(testCases: any[]): Observable<any> {
  //   return this.http.post(`${this.apiUrl}/generate-excel`, { test_cases: testCases }, { responseType: 'blob' });
  // }
}
