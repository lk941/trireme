import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class NavbarService {
  private breadcrumbSource = new BehaviorSubject<{ projectName: string; module: string }>({
    projectName: '',
    module: '',
  });
  breadcrumb$ = this.breadcrumbSource.asObservable();

  private searchQuerySource = new BehaviorSubject<string>('');
  searchQuery$ = this.searchQuerySource.asObservable();

  // Set breadcrumb data from navbar or any component
  setBreadcrumb(breadcrumb: { projectName: string; module: string }) {
    this.breadcrumbSource.next(breadcrumb);
  }

  // Set search query from navbar input
  setSearchQuery(query: string) {
    this.searchQuerySource.next(query);
  }
}
