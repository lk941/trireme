import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-automation-setup',
  standalone: true,
  imports: [FormsModule, HttpClientModule, CommonModule],
  templateUrl: './automation-setup.component.html',
  styleUrl: './automation-setup.component.css'
})
export class AutomationSetupComponent {
  selectedSuite: string = 'Ranorex';
  projectName: string = '';
  websiteUrl: string = '';
  selectedBrowser: string = 'chrome';

  constructor(private http: HttpClient, private router: Router) {}

  generateRanorexSolution(): void {
    const automationData = {
      suite: this.selectedSuite,
      projectName: this.projectName,
      websiteUrl: this.websiteUrl,
      browser: this.selectedBrowser
    };

  console.log('Generating Ranorex Solution with the following data:', automationData);
}

  goBackToUpload() {
    this.router.navigate(['/preview'], {
      state: { editedTestCases: history.state.editedTestCases, file: history.state.file}
    });
  }

}
