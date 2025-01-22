import { Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';

export const routes: Routes = [
    { path: '', component: HomeComponent }, // Default route to HomeComponent
    { path: '**', redirectTo: '' } // Redirect unknown routes to home
];
