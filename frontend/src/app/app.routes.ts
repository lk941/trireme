import { Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { PreviewComponent } from './preview/preview.component';
import { AutomationSetupComponent } from './automation-setup/automation-setup.component';


export const routes: Routes = [
    { path: '', component: HomeComponent }, // Default route to HomeComponent
    { path: 'preview', component: PreviewComponent },
    { path: 'automation-setup', component: AutomationSetupComponent },
    { path: '**', redirectTo: '' }, // Redirect unknown routes to home
];
