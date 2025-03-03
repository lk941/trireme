import { Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { PreviewComponent } from './preview/preview.component';
import { ProjectPageComponent } from './project-page/project-page.component';
import { AutomationSetupComponent } from './automation-setup/automation-setup.component';


export const routes: Routes = [
    { path: '', component: HomeComponent }, // Default route to HomeComponent
    { path: 'project-page/:id', component: ProjectPageComponent }, // Default route to HomeComponent
    { path: 'preview/:id/:id', component: PreviewComponent },
    { path: 'automation-setup/:id/:id', component: AutomationSetupComponent },
    { path: '**', redirectTo: '' }, // Redirect unknown routes to home
];
