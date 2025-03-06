import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router, NavigationEnd } from '@angular/router';
import { filter } from 'rxjs/operators';
import { NavbarService } from '../../services/navbar.service';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-navbar',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './navbar.component.html',
  styleUrl: './navbar.component.css'
})

export class NavbarComponent implements OnInit {
  breadcrumb = { projectName: '', module: '' };
  searchQuery: string = '';

  constructor(private navbarService: NavbarService, private router: Router, private route: ActivatedRoute) {}

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

    // Update the service so other components can access this data
    this.navbarService.setBreadcrumb(this.breadcrumb);
  }

  onSearch(event: any) {
    this.searchQuery = event.target.value;
    console.log('Search:', this.searchQuery);
  }

  navigateToHome(): void {
    this.router.navigate(['/']);
  }
}