import { Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { AppDocumentationComponent } from './app-documentation/app-documentation.component';
import { PreviewComponent } from './preview/preview.component';
import { ProjectPageComponent } from './project-page/project-page.component';
import { AutomationSetupComponent } from './automation-setup/automation-setup.component';
import { ModuleMandatoryComponent } from './module-mandatory/module-mandatory.component';

export const routes: Routes = [
    { path: '', component: HomeComponent }, // Default route to HomeComponent
    { path: 'app-documentation', component: AppDocumentationComponent },
    { path: 'project-page/:projectName/:pid', component: ProjectPageComponent },
    { path: 'preview/:projectName/:pid/:moduleName/:mid', component: PreviewComponent },
    { path: 'module-mandatory/:projectName/:pid/:moduleName/:mid', component: ModuleMandatoryComponent },
    { path: 'automation-setup/:projectName/:pid/:moduleName/:mid', component: AutomationSetupComponent },
    { path: '**', redirectTo: '' }, // Redirect unknown routes to home
];
