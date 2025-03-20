import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router, NavigationEnd } from '@angular/router';
import { catchError, filter } from 'rxjs/operators';
import { NavbarService } from '../../services/navbar.service';
import { CommonModule } from '@angular/common';
import { debounceTime, distinctUntilChanged, switchMap } from 'rxjs/operators';
import { Observable, of, Subject } from 'rxjs';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.scss'
})

export class NavbarComponent implements OnInit {
  breadcrumb = { projectName: '', module: '' };
  searchQuery = new Subject<string>();
  searchResults: any[] = [];
  projectId: String | null = null;
  moduleId: number | null = null;

  constructor(private navbarService: NavbarService, private http: HttpClient, private router: Router, private route: ActivatedRoute) {
      this.searchQuery.pipe(
        debounceTime(300), 
        distinctUntilChanged(), 
        switchMap(term => this.search(term))
      ).subscribe(results => {
        this.searchResults = results;
      });
  }

  ngOnInit() {
    this.router.events.pipe(filter((event) => event instanceof NavigationEnd)).subscribe(() => {
      this.updateBreadcrumb();
    });

    this.updateBreadcrumb();
  }

  updateBreadcrumb() {
    const snapshot = this.route.root.firstChild?.snapshot;
    this.breadcrumb.projectName = snapshot?.paramMap.get('projectName') || '';
    this.breadcrumb.module = snapshot?.paramMap.get('moduleName') || '';

    this.projectId = snapshot?.paramMap.get('pid') || null;

    // Update the service so other components can access this data
    this.navbarService.setBreadcrumb(this.breadcrumb);
  }

  onSearch(event: any) {
    const query = event.target.value.trim();
    this.searchQuery.next(query); // Trigger search
  }

  search(query: string): Observable<any[]> {
    if (!query) return of([]); // Prevent empty API calls
  
    return this.http.get<any[]>(`http://localhost:8000/search?query=${query}`).pipe(
      catchError(error => {
        console.error('Search API Error:', error);
        return of([]); // Return empty array on error
      })
    );
  }

  navigateTo(link: string) {
    this.router.navigateByUrl(link);
  }

  navigateToHome(): void {
    this.router.navigate(['/']);
  }

  navigateToProject(): void {
    this.router.navigate(['/project-page', this.breadcrumb.projectName, this.projectId]);
  }

  navigateToDocumentation(): void {
    this.router.navigate(['/app-documentation']);
  }
}